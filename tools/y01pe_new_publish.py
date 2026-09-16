#!/usr/bin/env python3
"""Publish the rebuilt Physical Education Year 1 as the standard edition.

This is not the master with two pages patched: it is a book built from scratch to
Standard A-2.3-Y1-4 - the seven front-matter pages, six teaching units of nine
pages each and the twelve back-matter pages, 71 pages, every page carrying the
standard's band, folio badge, palette rung and ladder type sizes.

The previous standard-edition build is MOVED to archive/ inside the book's own
folder, so the bytes survive and the move is disclosed. Nothing is deleted.

The manifest row is updated in place: page count, the full shell (a finished book
shows every page in the /finished reader) and the standard it was built to.

    .venv/bin/python tools/y01pe_new_publish.py --dry-run
    .venv/bin/python tools/y01pe_new_publish.py
"""
import json
import os
import shutil
import sys

import pymupdf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "work/y01-pe-book/y01-pe-new.pdf")
DEST_DIR = os.path.join(REPO, "public/library/y01-physical-education-standard")
DEST_PDF = os.path.join(DEST_DIR, "book.pdf")
DEST_COVER = os.path.join(DEST_DIR, "cover.webp")
ARCHIVE = os.path.join(DEST_DIR, "archive")
MANIFEST = os.path.join(REPO, "public/library.json")
SLUG = "y01-physical-education-standard"


def main():
    dry = "--dry-run" in sys.argv
    if not os.path.exists(SRC):
        raise SystemExit(f"no built book at {SRC}")
    book = pymupdf.open(SRC)
    pages = book.page_count
    if pages % 2 == 0 or (pages + 1) % 12:
        print(f"warning: {pages} pages is not a BookVault legal count "
              f"(12n - 1); the pack builder will report it")
    shell = list(range(1, pages + 1))
    print(f"built book: {pages} pages; shell = every page ({shell[0]}-{shell[-1]})")
    if dry:
        print("dry run: nothing written")
        return

    os.makedirs(ARCHIVE, exist_ok=True)
    if os.path.exists(DEST_PDF):
        import hashlib
        same = hashlib.md5(open(DEST_PDF, "rb").read()).hexdigest() == \
               hashlib.md5(open(SRC, "rb").read()).hexdigest()
        if same:
            print("the published build is already this build: nothing to archive")
        else:
            n = os.path.getsize(DEST_PDF)
            prev = pymupdf.open(DEST_PDF)
            stamp = f"book-{prev.page_count}pp-{int(os.path.getmtime(DEST_PDF))}.pdf"
            prev.close()
            moved = os.path.join(ARCHIVE, stamp)
            shutil.move(DEST_PDF, moved)
            print(f"moved the previous build ({n/1e6:.1f} MB) to "
                  f"{os.path.relpath(moved, REPO)}")
    os.makedirs(DEST_DIR, exist_ok=True)
    book.save(DEST_PDF, deflate=True, deflate_images=True, garbage=4)
    print("wrote", os.path.relpath(DEST_PDF, REPO),
          f"{os.path.getsize(DEST_PDF)/1e6:.2f} MB")

    # the catalogue card's cover: the book's own page 1, rendered flat
    pix = book[0].get_pixmap(matrix=pymupdf.Matrix(150 / 72, 150 / 72))
    from PIL import Image
    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(
        DEST_COVER, "WEBP", quality=86, method=6)
    print("wrote", os.path.relpath(DEST_COVER, REPO),
          f"{os.path.getsize(DEST_COVER)/1e6:.2f} MB", pix.width, "x", pix.height)

    rows = json.load(open(MANIFEST))
    changed = 0
    for r in rows:
        if r.get("slug") == SLUG:
            r["pages"] = pages
            r["shell_pages"] = shell
            r["standard"] = "A-2.3-Y1-4"
            r["shell_built"] = ["cover", "imprint", "contents", "welcome",
                                "front matter", "units 1-6", "back matter"]
            r["built_from_scratch"] = True
            changed += 1
    if not changed:
        raise SystemExit(f"no manifest row for {SLUG} - refusing to guess")
    json.dump(rows, open(MANIFEST, "w"), indent=2)   # the house format: indent 2
    print(f"manifest row for {SLUG} updated: pages {pages}, "
          f"shell_pages 1-{pages}, standard A-2.3-Y1-4")
    book.close()


if __name__ == "__main__":
    main()
