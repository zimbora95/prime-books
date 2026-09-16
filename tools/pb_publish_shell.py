#!/usr/bin/env python3
"""Publish the standardised shell of y01 Physical Education Year 1.

The standard edition is the master with its two shell pages replaced by the
Standard A-2.3 pages: physical page 3 becomes the standardised CONTENTS page and
physical page 4 the standardised WELCOME page. Same extent, same teaching, so
nothing a teacher placed is lost; the pages the standard fixes are the pages the
standard now sets.

Nothing is deleted. The previous standard-edition build is MOVED to
archive/ inside the book's own folder, so the bytes survive and the move is
disclosed.

    .venv/bin/python publish_shell.py --dry-run
    .venv/bin/python publish_shell.py
"""
import json
import os
import shutil
import sys

import pymupdf

WORK = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(WORK, "..", ".."))
MASTER = os.path.join(REPO, "public/library/y01-physical-education/book.pdf")
SHELL_PAGES = os.path.join(WORK, "y01-pe-standard-pages.pdf")
DEST_DIR = os.path.join(REPO, "public/library/y01-physical-education-standard")
DEST_PDF = os.path.join(DEST_DIR, "book.pdf")
ARCHIVE = os.path.join(DEST_DIR, "archive")
MANIFEST = os.path.join(REPO, "public/library.json")
SLUG = "y01-physical-education-standard"
REPLACE = (3, 4)                    # the physical pages the standard fixes

# the standard's folio badge, from public/standards/years-1-4.json
STD = json.load(open(os.path.join(REPO, "public/standards/years-1-4.json")))
FOLIO = STD["geometry"]["folio_centre_pt"]
FOLIO_D = STD["geometry"]["folio_diameter_pt"]
AMBER = STD["year_stripes"]["1"]
INK = STD["ink"]


def _rgb(hexstr):
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def normalise_folio(page, number):
    """Replace a page's own folio badge with the standard's badge.

    The teacher caught it at once: page 2's numeral is white on a darker ochre
    while the standardised pages carry the standard's amber with the ink numeral,
    so the badge changed colour from one page to the next. The pages the standard
    does not author still belong to the edition, so their badges are brought onto
    the standard here.

    A plain overpaint is not enough: the master's badge is drawn as a masked
    group several times over, so a circle drawn on top leaves a crescent of the
    old ochre showing above it (and the gate then still reads the old badge).
    The old badge is therefore REDACTED - removed from the page, filled with the
    colour the page itself uses there - and the standard badge drawn in its
    place. Nothing else on the page is touched, and nothing is deleted from the
    master.
    """
    anchors = (pymupdf.Point(FOLIO[0], FOLIO[1]),
               pymupdf.Point(page.rect.width - FOLIO[0], FOLIO[1]))
    rects = []
    for d in page.get_drawings():
        r = d.get("rect")
        if r is None or not d.get("fill"):
            continue
        if r.y0 < 715 or not (8 < r.width < 40 and 8 < r.height < 40):
            continue
        c = pymupdf.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        if min(abs(c.x - a.x) + abs(c.y - a.y) for a in anchors) < 40:
            rects.append(r)
    if not rects:
        return False
    box = rects[0]
    for r in rects[1:]:
        box |= r
    # expanded to swallow the masked white plate the master's badge sits on (and
    # to be sure every one of the badge's repeated copies is fully inside it)
    box = pymupdf.Rect(box.x0 - 14, box.y0 - 14, box.x1 + 14, box.y1 + 14)
    # the page's own colour where the badge sits: sampled just clear of it, so
    # the patch cannot leave a rectangle of the wrong tone on a tinted page
    probe = pymupdf.Point(box.x0 - 7, box.y0 - 7)
    pix = page.get_pixmap(clip=pymupdf.Rect(probe.x, probe.y, probe.x + 1, probe.y + 1))
    bg = pix.pixel(0, 0)
    bg = tuple(v / 255 for v in bg[:3])
    page.add_redact_annot(box, fill=bg)
    # REMOVE_IF_COVERED, never IF_TOUCHED: the unit opener's flood colour is one
    # page-wide path, and 'touched' would delete the whole background of the page
    # along with the badge. Only art wholly inside the box goes.
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    cx, cy = FOLIO[0], FOLIO[1]
    page.draw_circle(pymupdf.Point(cx, cy), FOLIO_D / 2, color=None, fill=_rgb(AMBER))
    label = str(number)
    fontfile = "/root/pbfonts/Fredoka-SemiBold.ttf"
    page.insert_font(fontname="fredoka", fontfile=fontfile)
    tw = pymupdf.Font(fontfile=fontfile).text_length(label, fontsize=11)
    page.insert_text((cx - tw / 2, cy + 3.9), label, fontname="fredoka",
                     fontsize=11, color=_rgb(INK))
    return True


def main():
    dry = "--dry-run" in sys.argv
    master = pymupdf.open(MASTER)
    shell = pymupdf.open(SHELL_PAGES)
    if shell.page_count != len(REPLACE):
        raise SystemExit(f"shell has {shell.page_count} pages, expected {len(REPLACE)}")

    out = pymupdf.open()
    repainted = []
    for i in range(master.page_count):
        if i + 1 == REPLACE[0]:
            out.insert_pdf(shell)
            continue
        if i + 1 in REPLACE:
            continue
        out.insert_pdf(master, from_page=i, to_page=i)
        if normalise_folio(out[-1], i + 1):
            repainted.append(i + 1)
    out.set_metadata(master.metadata)
    print(f"master {master.page_count} pp + {shell.page_count} standardised pages "
          f"= {out.page_count} pp (shell pages {list(REPLACE)} replaced)")
    print(f"folio badges repainted onto the standard: {repainted}")

    # the shell the /finished reader shows: the standardised pages plus the pages
    # that still have to be rebuilt, in reading order
    shell_pages = [1, 2, 3, 4, out.page_count]
    print("shell_pages for the manifest:", shell_pages)

    if dry:
        print("dry run: nothing written")
        return

    os.makedirs(ARCHIVE, exist_ok=True)
    if os.path.exists(DEST_PDF):
        n = os.path.getsize(DEST_PDF)
        prev = pymupdf.open(DEST_PDF)
        stamp = f"book-{prev.page_count}pp-{int(os.path.getmtime(DEST_PDF))}.pdf"
        prev.close()
        moved = os.path.join(ARCHIVE, stamp)
        shutil.move(DEST_PDF, moved)
        print(f"moved the previous build ({n/1e6:.1f} MB) to "
              f"{os.path.relpath(moved, REPO)}")
    os.makedirs(DEST_DIR, exist_ok=True)
    out.save(DEST_PDF, deflate=True, deflate_images=True, garbage=4)
    print("wrote", os.path.relpath(DEST_PDF, REPO),
          f"{os.path.getsize(DEST_PDF)/1e6:.2f} MB")

    rows = json.load(open(MANIFEST))
    changed = 0
    for r in rows:
        if r.get("slug") == SLUG:
            r["pages"] = out.page_count
            r["shell_pages"] = shell_pages
            r["standard"] = "A-2.3-Y1-4"
            r["shell_built"] = ["contents", "welcome"]
            changed += 1
    if not changed:
        raise SystemExit(f"no manifest row for {SLUG} - refusing to guess")
    json.dump(rows, open(MANIFEST, "w"), indent=2)   # the house format: indent 2
    print(f"manifest row for {SLUG} updated: pages {out.page_count}, "
          f"shell_pages {shell_pages}")
    master.close(); out.close()


if __name__ == "__main__":
    main()