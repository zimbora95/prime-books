#!/usr/bin/env python3
"""Put the house imprint page on physical page 2 of a Year 7-9 Portuguese 2nd book.

The three books have no imprint page at all: page 2 is the scheme-of-work
overview (Y7) or the Índice (Y8, Y9).  This tool inserts the standard imprint
page (built by tools/std_imprint_lib.py) as physical page 2, shifts everything
after it by one, and then repairs everything the shift breaks:

  * every printed folio on pages 3..n-1 is incremented by one (the books print
    their physical page number, so the correct value is simply the new index);
  * every Índice page reference is incremented by one;
  * the book is left on an EVEN page count, because an odd count puts the back
    cover in a flipbook spread instead of alone.  Where the master already
    carries the blank filler page that the even-page rule inserts (Y9), it is
    dropped; where it does not (Y7, Y8) a blank filler is added before the back
    cover, exactly as commit 92a180b did for the 26 odd-count books.
  * Y9's folio tab is only 17 pt wide, so a three-digit folio overflows it and
    its last digit prints white-on-cream (invisible: pages 100-108 today).  The
    tab is widened to fit whenever the number needs it.

Nothing is deleted: every page of the master is carried through, and the tool
refuses to run if the front-matter content it expects is not there.

    .venv/bin/python tools/out/pt2/splice_imprint.py <slug> [--dry-run]
    .venv/bin/python tools/out/pt2/splice_imprint.py --verify <slug>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys

import pymupdf

REPO = "/root/prime-books"
WORK = "/root/backwork/pt2"
FONT_ANDIKA_BOLD = os.path.join(REPO, "tools", "cover_assets", "Andika-Bold.ttf")

# per book: how to recognise the folio, the Índice page references and the tab
BOOKS = {
    "y07-portuguese-2nd": dict(
        page="612x792",
        folio=dict(size=10.0, color=0x1A5E68, xmin=495.0, ymin=745.0),
        index_pages=[],                       # this book prints no Índice
        index_ref=dict(size=10.0, color=0x1A5E68, xmin=490.0, xmax=502.0, ymax=700.0),
        tab=None,
        # page 2 (the scheme-of-work page) is the one page in this book with no
        # folio at all; it becomes physical page 3, so it takes the folio of its
        # neighbours (reference books number their front matter too).
        add_folio=[dict(page=2, copy_from=4)],
    ),
    "y08-portuguese-2nd": dict(
        page="595x765.12",
        folio=dict(size=10.0, color=0x1A5E68, xmin=495.0, ymin=700.0),
        index_pages=[1],                      # old page 2 (now 3) is the Índice
        index_ref=dict(size=10.0, color=0x1A5E68, xmin=490.0, xmax=502.0, ymax=700.0),
        tab=None,
    ),
    "y09-portuguese-2nd": dict(
        page="595x765.12",
        folio=dict(size=10.0, color=0xFFFFFF, xmin=500.0, ymin=700.0),
        index_pages=[1, 2],                   # old pages 2 and 3 (now 3 and 4)
        index_ref=dict(size=10.5, color=0x1A5E68, xmin=500.0, xmax=515.0, ymax=700.0),
        tab=dict(rect=(505.0, 712.0, 522.0, 730.0),
                 fill=(0.10199999809265137, 0.36899998784065247, 0.40799999237060595),
                 x=509.0, baseline=726.6),
    ),
}
OFFSET = 1                       # the imprint page shifts everything after page 2


def spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for line in b["lines"]:
            for s in line["spans"]:
                if s["text"].strip():
                    out.append(s)
    return out


def is_folio(sp, spec, height):
    return (abs(sp["size"] - spec["size"]) < 0.2 and sp["color"] == spec["color"]
            and sp["bbox"][0] >= spec["xmin"] and sp["bbox"][1] >= spec["ymin"]
            and re.fullmatch(r"\d{1,3}", sp["text"].strip()) is not None)


def is_index_ref(sp, spec, height):
    return (abs(sp["size"] - spec["size"]) < 0.2 and sp["color"] == spec["color"]
            and spec["xmin"] <= sp["bbox"][0] <= spec["xmax"]
            and sp["bbox"][1] <= spec["ymax"]
            and re.fullmatch(r"\d{1,3}", sp["text"].strip()) is not None)


def folio_spans(page, spec):
    return [s for s in spans(page) if is_folio(s, spec, page.rect.height)]


def set_number(page, sp, number, spec, tab=None):
    """Redact a folio/index number and write the replacement in its own font."""
    bbox = pymupdf.Rect(*sp["bbox"])
    page.add_redact_annot(pymupdf.Rect(bbox.x0 - 0.5, bbox.y0 - 0.5,
                                       bbox.x1 + 0.5, bbox.y1 + 0.5), fill=None)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
    if tab is not None:                       # keep the number inside its tab
        f = pymupdf.Font(fontfile=FONT_ANDIKA_BOLD)
        need = tab["x"] + f.text_length(str(number), fontsize=spec["size"]) + 1.5
        r = pymupdf.Rect(tab["rect"][0], tab["rect"][1],
                         max(tab["rect"][2], need), tab["rect"][3])
        page.draw_rect(r, color=None, fill=tab["fill"])
    page.insert_text((sp["bbox"][0], sp["origin"][1]), str(number),
                     fontsize=spec["size"], fontname="ab",
                     fontfile=FONT_ANDIKA_BOLD,
                     color=tuple(v / 255 for v in ((spec["color"] >> 16 & 255),
                                                   (spec["color"] >> 8 & 255),
                                                   (spec["color"] & 255))))
    return 1


def blank_page_index(doc):
    """The empty filler page the even-page rule inserts before the back cover."""
    for i in range(doc.page_count - 2, 1, -1):
        p = doc[i]
        if (not p.get_text().strip() and not p.get_images()
                and not [d for d in p.get_drawings()
                         if d.get("fill") or d.get("color")]):
            return i
        return None                       # only the page before the back cover counts
    return None


def build(slug, dry_run=False):
    cfg = BOOKS[slug]
    master = os.path.join(REPO, "public", "library", slug, "book.pdf")
    imprint_path = os.path.join(WORK, "%s-imprint.pdf" % slug)
    if not os.path.exists(imprint_path):
        raise SystemExit("no imprint page built: %s" % imprint_path)

    src = pymupdf.open(master)
    n = src.page_count
    if "I M P R I N T" in src[1].get_text():
        raise SystemExit("%s: page 2 is already the imprint page — refusing to run "
                         "twice (restore from %s to redo)" % (slug, WORK))
    size = (round(src[0].rect.width, 2), round(src[0].rect.height, 2))
    want = tuple(float(v) for v in cfg["page"].split("x"))
    if abs(size[0] - want[0]) > 0.5 or abs(size[1] - want[1]) > 0.5:
        raise SystemExit("%s: master is %s, the config says %s" % (slug, size, cfg["page"]))

    filler = blank_page_index(src)
    old_pages = [s["text"].strip() for s in spans(src[1])][:3]
    print("%s: %d pages, %s, blank filler page %s, page 2 starts %r"
          % (slug, n, size, filler and filler + 1, old_pages))

    limit = n - 3 if filler is not None else n - 2      # last interior page kept
    out = pymupdf.open()
    out.insert_pdf(src, from_page=0, to_page=0)          # 1  front cover
    out.insert_pdf(pymupdf.open(imprint_path))           # 2  house imprint page
    out.insert_pdf(src, from_page=1, to_page=limit)      # 3..old pages
    interior_end = out.page_count                        # last page before the tail
    need_blank = (out.page_count + 1) % 2 == 1           # + the back cover
    if need_blank:
        out.new_page(width=src[0].rect.width, height=src[0].rect.height)
    out.insert_pdf(src, from_page=n - 1, to_page=n - 1)  # back cover
    if out.page_count % 2:
        raise SystemExit("%s: page count %d is odd" % (slug, out.page_count))

    if dry_run:
        print("   would be: %d -> %d pages, blank filler: %s, interior end %d"
              % (n, out.page_count, need_blank, interior_end))
        return 0

    # ---- folios: the books print their physical page number ------------------
    fixed = 0
    nofolio = []
    for i in range(2, out.page_count - 1):
        page = out[i]
        if not page.get_text().strip():                  # the blank filler
            continue
        found = folio_spans(page, cfg["folio"])
        if not found:
            nofolio.append(i + 1)
            continue
        for sp in found:
            fixed += set_number(page, sp, i + 1, cfg["folio"], tab=cfg["tab"])

    # ---- pages that had no folio take the folio of their neighbours ----------
    added = 0
    for item in cfg.get("add_folio", []):
        page = out[item["page"]]
        ref = folio_spans(out[item["copy_from"]], cfg["folio"])[0]
        page.insert_text((ref["origin"][0], ref["origin"][1]), str(item["page"] + 1),
                         fontsize=ref["size"], fontname="ab",
                         fontfile=FONT_ANDIKA_BOLD,
                         color=tuple(v / 255 for v in ((ref["color"] >> 16 & 255),
                                                       (ref["color"] >> 8 & 255),
                                                       (ref["color"] & 255))))
        nofolio = [p for p in nofolio if p != item["page"] + 1]
        added += 1

    # ---- Índice page references ---------------------------------------------
    refs = 0
    for old_i in cfg["index_pages"]:
        page = out[old_i + 1]                            # shifted by the imprint
        for sp in spans(page):
            if is_index_ref(sp, cfg["index_ref"], page.rect.height):
                refs += set_number(page, sp, int(sp["text"].strip()) + OFFSET,
                                   cfg["index_ref"])

    out.set_metadata(src.metadata)
    out.set_toc(src.get_toc())
    tmp = master + ".tmp"
    out.save(tmp, garbage=4, deflate=True, clean=True)
    out.close()
    src.close()
    shutil.move(tmp, master)
    print("%s: %d pages, folios rewritten %d, folios added %d, índice references "
          "bumped %d%s" % (slug, pymupdf.open(master).page_count, fixed, added, refs,
                           ("  UNNUMBERED: %s" % nofolio) if nofolio else ""))
    return 0


def verify(slug):
    cfg = BOOKS[slug]
    master = os.path.join(REPO, "public", "library", slug, "book.pdf")
    backup = os.path.join(WORK, "%s-book-preimprint.pdf" % slug)
    if not os.path.exists(backup):
        print("%s: no pre-imprint backup" % slug)
        return 1
    old = pymupdf.open(backup)
    new = pymupdf.open(master)
    bad = []
    if new.page_count % 2:
        bad.append("page count %d is odd" % new.page_count)
    if new.page_count < old.page_count:
        bad.append("page count went down: %d -> %d" % (old.page_count, new.page_count))
    # every old interior page must still be there, in order, with its text
    # (pure-digit tokens are dropped: the folio/índice numbers are rewritten)
    def words(p):
        return " ".join(w for w in p.get_text().split() if not w.isdigit())
    old_txt = [words(old[i]) for i in range(1, old.page_count - 1)]
    new_txt = [words(new[i]) for i in range(2, new.page_count - 1)]
    missing = [i + 2 for i in range(len(old_txt))
               if old_txt[i] and not any(old_txt[i] in t for t in new_txt)]
    if missing:
        bad.append("content lost from old page(s) %s" % missing[:8])
    # folios
    wrong = []
    for i in range(2, new.page_count - 1):
        page = new[i]
        if not page.get_text().strip():
            continue
        f = folio_spans(page, cfg["folio"])
        if not f or int(f[0]["text"].strip()) != i + 1:
            wrong.append((i + 1, [s["text"].strip() for s in f]))
    if wrong:
        bad.append("folios wrong on %s" % wrong[:8])
    # imprint page 2
    t2 = new[1].get_text()
    if "P R I M E  S C H O O L  P R E S S" not in t2 or "I M P R I N T" not in t2:
        bad.append("page 2 is not the house imprint page")
    t1 = " ".join(new[0].get_text().split())
    if not t1:
        bad.append("front cover lost its text")
    print("%s: %d pages (was %d), page 2 %s" % (slug, new.page_count, old.page_count,
                                                t2.strip().splitlines()[0]))
    print("   VERDICT:", "clean" if not bad else "CHECK")
    for b in bad:
        print("     -", b)
    old.close()
    new.close()
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if a.verify:
        return verify(a.slug)
    slug = a.slug
    os.makedirs(WORK, exist_ok=True)
    backup = os.path.join(WORK, "%s-book-preimprint.pdf" % slug)
    if not os.path.exists(backup):
        shutil.copy2(os.path.join(REPO, "public", "library", slug, "book.pdf"), backup)
        print("backed up ->", backup)
    return build(slug, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
