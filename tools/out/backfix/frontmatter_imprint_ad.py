#!/usr/bin/env python3
"""Rebuild the front matter of a Year 7-9 Art & Design book.

The book's physical page 2 currently carries BOTH the old *Imprint* block and the
*Welcome* text.  This tool:

  * writes the house standard imprint page (tools/std_imprint_lib.py) as physical
    page 2;
  * re-draws the old page 2 *without* its Imprint block (heading, body and the
    leftover tinted panel) as physical page 3, everything else kept in place,
    moved up so the page starts at the top of the text area -- same fonts, same
    sizes, same table;
  * shifts every following page by one, dropping the blank filler page that the
    even-page rule had inserted before the back cover, so the book keeps its even
    page count and the back cover still stands alone;
  * renumbers every printed page number to its new physical page -- the "Page n"
    folio on each page and each entry of the Contents list (both were one page
    lower after the insert).

Usage:
  .venv/bin/python tools/out/backfix/frontmatter_imprint_ad.py <slug> \
      --spec tools/out/backfix/imprint_specs/<slug>.json [--dry-run]
"""
import argparse
import os
import re
import sys
import tempfile

import pymupdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import std_imprint_lib as si  # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FOLIO_RIGHT = 570.2          # right edge the book's own folios align to
TOP_TEXT_Y = 50.0            # where content starts on the book's other pages
HEADER_RE = re.compile(r"^Year \d+ Art & Design\s+·")
FOOTER_LEFT_RE = re.compile(r"^Prime Books\s+·\s+Cambridge Lower Secondary$")


# ----------------------------------------------------------------- furniture --
def is_header(sp):
    return HEADER_RE.match(sp["text"].strip()) is not None


def is_footer_left(sp):
    return FOOTER_LEFT_RE.match(sp["text"].strip()) is not None


def is_folio_label(sp):
    return sp["text"].strip() == "Page"


def is_folio_combined(sp):
    return re.match(r"^Page\s+\d+$", sp["text"].strip()) is not None


def is_folio_number(sp, h):
    t = sp["text"].strip()
    return (t.isdigit() and sp["size"] >= 10.5
            and sp["bbox"][1] > h - 90 and sp["bbox"][0] > 480)


def page_spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for line in b["lines"]:
            for sp in line["spans"]:
                if sp["text"].strip():
                    out.append(sp)
    return out


def span_font(sp):
    """(fontname for insert_text, fontfile or None)."""
    name = sp["font"]
    if "DejaVuSans-Bold" in name:
        return "dv-bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
    if "DejaVuSans" in name:
        return "dv", os.path.join(FONT_DIR, "DejaVuSans.ttf")
    if "Bold" in name:
        return "hebo", None
    return "helv", None


def text_width(sp, text=None):
    text = sp["text"] if text is None else text
    if sp["font"].startswith("AAAAAA+"):        # DejaVu
        fn = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"
                          if "Bold" in sp["font"] else "DejaVuSans.ttf")
        f = pymupdf.Font(fontfile=fn)
    else:
        f = pymupdf.Font("hebo" if "Bold" in sp["font"] else "helv")
    return f.text_length(text, fontsize=sp["size"]), f


def draw_text(page, x, y, text, sp, right=None):
    name, path = span_font(sp)
    f = pymupdf.Font(fontfile=path) if path else pymupdf.Font(name)
    if right is not None:
        x = right - f.text_length(text, fontsize=sp["size"])
    col = sp["color"]
    if isinstance(col, int):
        col = ((col >> 16 & 255) / 255, (col >> 8 & 255) / 255, (col & 255) / 255)
    page.insert_text((x, y), text, fontsize=sp["size"], fontname=name,
                     fontfile=path, color=col)


# ----------------------------------------------------------- adapted page 3 ---
def build_adapted(src_page, folio, spread=True, target_bottom=700.0):
    """Old page 2, Imprint block removed, moved up to the top of the text area.

    With no Imprint block the page would end high above the footer, so the space
    that frees up is given back to the gaps between the page's own blocks (never
    to line leading, heading spacing or the table), which is what "adapting the
    page" means here.  Fonts, sizes and line pitch are untouched.
    """
    h = src_page.rect.height
    spans = page_spans(src_page)
    imprint = [s for s in spans if s["text"].strip() == "Imprint"]
    if not imprint:
        raise SystemExit("no Imprint heading on page 2")
    imp_y = imprint[0]["bbox"][1]
    welcome = [s for s in spans
               if s["bbox"][1] > imp_y + 6 and "Bold" in s["font"]
               and s["size"] >= 11.5]
    if not welcome:
        raise SystemExit("no heading after Imprint on page 2")
    wel_y = min(s["bbox"][1] for s in welcome)
    delta = wel_y - TOP_TEXT_Y

    kept = sorted([s for s in spans if wel_y - 1 <= s["bbox"][1] <= 740],
                  key=lambda s: (s["bbox"][1], s["bbox"][0]))
    def is_head(sp):
        return "Bold" in sp["font"] and sp["size"] >= 11.5

    def is_small(sp):
        return sp["size"] <= 8.6

    gaps = []
    for i in range(1, len(kept)):
        a, b = kept[i - 1], kept[i]
        g = b["bbox"][1] - a["bbox"][1]              # top to top
        if g <= 14.5:                                # line pitch: leave alone
            continue
        if is_head(a) or is_small(a) or is_small(b):  # heading or table spacing
            continue
        gaps.append([i, g])
    add = {}
    if spread and gaps:
        extra = target_bottom - (kept[-1]["bbox"][3] - delta)
        share = min(extra, 1.6 * sum(g for _, g in gaps))
        if share > 0:
            add = {i: share * g / sum(g2 for _, g2 in gaps) for i, g in gaps}
    offs, run = [], 0.0
    for i in range(len(kept)):
        if i in add and i:
            run += add[i]
        offs.append(run)
    def off_for(y):
        best, bo = 0, 0.0
        for i, sp in enumerate(kept):
            if abs(sp["bbox"][1] - y) < abs(best - y):
                best, bo = sp["bbox"][1], offs[i]
        return bo

    out = pymupdf.open()
    page = out.new_page(width=src_page.rect.width, height=src_page.rect.height)

    for dr in src_page.get_drawings():
        r = dr["rect"]
        if not ((r.y0 < imp_y - 4) or (r.y1 > wel_y + 2) or r.y1 > 740):
            continue                      # the removed block's own tinted panel
        moves = wel_y - 4 <= r.y0 <= 740 and len(kept)
        shift = delta - off_for(r.y0) if moves else 0.0
        for it in dr["items"]:
            kind = it[0]
            fill, col, w = dr.get("fill"), dr.get("color"), dr.get("width") or 0
            if kind == "re":
                rr = it[1]
                if shift:
                    rr = pymupdf.Rect(rr.x0, rr.y0 - shift, rr.x1, rr.y1 - shift)
                page.draw_rect(rr, color=col, fill=fill, width=w)
            elif kind == "l":
                p1, p2 = it[1], it[2]
                if shift:
                    p1 = pymupdf.Point(p1.x, p1.y - shift)
                    p2 = pymupdf.Point(p2.x, p2.y - shift)
                page.draw_line(p1, p2, color=col, width=w)

    for i, sp in enumerate(kept):
        draw_text(page, sp["bbox"][0], sp["origin"][1] - delta + offs[i],
                  sp["text"], sp)
    for sp in spans:                      # header and footer furniture
        y = sp["bbox"][1]
        if y < imp_y - 4 or y > 740:
            draw_text(page, sp["bbox"][0], sp["origin"][1], sp["text"], sp)
    lab = [s for s in spans if is_folio_label(s)]
    if lab:
        draw_text(page, lab[0]["bbox"][0], lab[0]["origin"][1], "Page", lab[0])
    num = [s for s in spans if is_folio_number(s, h)]
    ref = num[0] if num else pick_ink(spans)
    draw_text(page, 0, ref["origin"][1], str(folio), ref, right=FOLIO_RIGHT)
    if kept:
        print("   adapted page: content %.0f -> %.0f, gaps %d, spread %.0f pt"
              % (wel_y, kept[-1]["bbox"][3] - delta + offs[-1], len(gaps),
                 sum(add.values())))
    return out


def pick_ink(spans):
    for sp in spans:
        if sp["bbox"][1] > 700:
            return sp
    return spans[0]


# ------------------------------------------------------------- renumbering ----
def renumber_folio(page, number):
    """Write the page's own folio number; drop duplicated furniture."""
    h = page.rect.height
    spans = page_spans(page)
    labels = [s for s in spans if is_folio_label(s)]
    nums = [s for s in spans if is_folio_number(s, h)]
    comb = [s for s in spans if is_folio_combined(s)]
    heads = [s for s in spans if is_header(s)]
    foots = [s for s in spans if is_footer_left(s)]
    drop = labels[1:] + nums + comb + heads[1:] + foots[1:]
    if not nums and not labels and not comb:
        return 0, 0
    if not drop and nums and nums[0]["text"].strip() == str(number):
        return 0, 0
    for sp in drop:
        page.add_redact_annot(pymupdf.Rect(*sp["bbox"]), fill=None)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
    if comb:
        ref = comb[0]
        wid, _ = text_width(ref)
        draw_text(page, 0, ref["origin"][1], "Page %d" % number, ref,
                  right=ref["bbox"][0] + wid)
        return len(drop), 1
    ref = nums[0] if nums else pick_ink(spans)
    draw_text(page, 0, ref["origin"][1], str(number), ref, right=FOLIO_RIGHT)
    return len(drop), 1


def book_folio_offset(src):
    """1 when the book printed folio = physical - 1 (Year 8), else 0."""
    for i, p in enumerate(src):
        if i < 3 or i > src.page_count - 3:
            continue
        h = p.rect.height
        for sp in page_spans(p):
            t = sp["text"].strip()
            if t.isdigit() and sp["size"] >= 10.5 and sp["bbox"][1] > h - 90 \
                    and sp["bbox"][0] > 480:
                return int(t) - (i + 1) == -1 and 1 or 0
    return 0


def renumber_contents(page, bump=1):
    """Bump every page reference in the Contents list by one."""
    h = page.rect.height
    spans = page_spans(page)
    targets = [s for s in spans
               if s["text"].strip().isdigit() and s["bbox"][0] > 480
               and s["bbox"][1] < h - 120]
    n = 0
    for sp in targets:
        old = int(sp["text"].strip())
        if old < 3:                       # front matter is not "page 1/2"
            continue
        wid, _ = text_width(sp)
        right = sp["bbox"][0] + wid
        page.add_redact_annot(pymupdf.Rect(*sp["bbox"]), fill=None)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
        draw_text(page, 0, sp["origin"][1], str(old + bump), sp, right=right)
        n += 1
    return n


# ------------------------------------------------------------------- driver ---
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--spec", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    src_path = os.path.join(ROOT, "public", "library", args.slug, "book.pdf")
    spec = __import__("json").load(open(args.spec))
    stripe, accent = si.year_colours(spec.get("year"))

    src = pymupdf.open(src_path)
    n = src.page_count
    blank = src[n - 2]
    if blank.get_text().strip() or blank.get_images() or blank.get_drawings():
        raise SystemExit("page %d is not blank -- refusing to drop it" % (n - 1))
    odd = [i + 1 for i, p in enumerate(src)
           if abs(p.rect.width - 612) > 1 or abs(p.rect.height - 792) > 1]
    print("%s: %d pages, blank filler at %d, non-Letter pages %s"
          % (args.slug, n, n - 1, odd))
    if args.dry_run:
        return 0

    tmp = tempfile.mkdtemp(prefix="imprint-")
    imp_path = os.path.join(tmp, "imprint.pdf")
    problems = si.audit(si.build_page(spec, stripe, accent))
    si.build_page(spec, stripe, accent).save(imp_path)
    if problems:
        raise SystemExit("imprint page audit: %s" % problems)
    imp = pymupdf.open(imp_path)
    adapted = build_adapted(src[1], 3)

    out = pymupdf.open()
    out.insert_pdf(src, from_page=0, to_page=0)          # front cover
    out.insert_pdf(imp)                                  # page 2
    out.insert_pdf(adapted)                              # page 3
    out.insert_pdf(src, from_page=2, to_page=n - 3)      # old 3 .. before blank
    out.insert_pdf(src, from_page=n - 1, to_page=n - 1)  # back cover
    if out.page_count != n:
        raise SystemExit("page count %d != %d" % (out.page_count, n))

    dedup = fixed = 0
    for i in range(1, out.page_count - 1):
        d, f = renumber_folio(out[i], i + 1)
        dedup += d
        fixed += f
    toc = renumber_contents(out[3], 1 + book_folio_offset(src))   # old Contents page

    out.set_metadata(src.metadata)
    out.save(src_path, garbage=3, deflate=True)
    print("%s: %d pages, folios rewritten %d (furniture pieces removed %d), "
          "contents entries bumped %d" % (args.slug, out.page_count, fixed, dedup, toc))
    for i in (1, 2, 3):
        print("   page %d: %r" % (i + 1, out[i].get_text()[:150]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
