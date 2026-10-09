#!/usr/bin/env python3
"""Finish the y03-computing-and-robotics re-cut: re-render the unit opener with
the fitted title, splice it into the built book, publish the master and
regenerate the catalogue cover.

The opener title "Computational thinking and programming" is 489 pt at the
opener's 26 pt floor, which clipped the last letters against the page edge;
render_opener's floor is now 21 pt, so the page is re-rendered and swapped in.
"""
from __future__ import annotations

import os
import shutil
import sys

import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pb_engine as E            # noqa: E402
import y03cr_book_content as C   # noqa: E402
import y03cr_build as _B         # noqa: E402,F401  (applies the locked A-2.3 unit palette)

SLUG = "y03-computing-and-robotics"
BUILT = os.path.join(REPO, "work", "y03cr", "book_new.pdf")
OUT = "/tmp/y03cr_final.pdf"
MASTER = os.path.join(REPO, "public", "library", SLUG, "book.pdf")
COVER = os.path.join(REPO, "public", "library", SLUG, "cover.webp")

E.IMG_DIR = os.path.join(REPO, "work", "y03cr", "img")
OPENER_INDEX = 9                 # physical page 10


def main():
    spec = [p for p in C.build_pages() if p["kind"] == "opener"][0]["spec"]
    one = pymupdf.open()
    pg, bottom = E.render_opener(one, spec, OPENER_INDEX + 1)
    span = [s for b in pg.get_text("dict")["blocks"] for l in b.get("lines", [])
            for s in l["spans"] if s["text"].startswith("Computational")]
    print("opener title span:", [round(v, 1) for v in span[0]["bbox"]], "size",
          round(span[0]["size"], 1), "right edge 575 max")
    assert span and span[0]["bbox"][2] <= 575.5, span

    old = pymupdf.open(BUILT)
    assert old.page_count == 40, old.page_count
    out = pymupdf.open()
    out.insert_pdf(old, from_page=0, to_page=OPENER_INDEX - 1)
    out.insert_pdf(one)
    out.insert_pdf(old, from_page=OPENER_INDEX + 1, to_page=old.page_count - 1)
    assert out.page_count == 40, out.page_count
    out.set_metadata(old.metadata)
    out.save(OUT, deflate=True, garbage=3, clean=True)
    print("pages:", out.page_count, "size MB:",
          round(os.path.getsize(OUT) / 1e6, 2))

    chk = pymupdf.open(OUT)
    print("p1 :", chk[0].get_text().strip().replace("\n", " | ")[:70])
    print("p2 :", chk[1].get_text().strip().replace("\n", " | ")[:70])
    print("p10:", chk[9].get_text().strip().replace("\n", " | ")[:90])
    print("p40:", chk[39].get_text().strip().replace("\n", " | ")[:70])

    if "--commit" in sys.argv:
        shutil.copy(OUT, MASTER)
        master = pymupdf.open(MASTER)
        page = master[0]
        zoom = 720 / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        img.save(COVER, "WEBP", quality=88)
        print("master replaced and cover.webp regenerated:",
              round(os.path.getsize(MASTER) / 1e6, 2), "MB /",
              round(os.path.getsize(COVER) / 1e3), "KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
