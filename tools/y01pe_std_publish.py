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


def main():
    dry = "--dry-run" in sys.argv
    master = pymupdf.open(MASTER)
    shell = pymupdf.open(SHELL_PAGES)
    if shell.page_count != len(REPLACE):
        raise SystemExit(f"shell has {shell.page_count} pages, expected {len(REPLACE)}")

    out = pymupdf.open()
    for i in range(master.page_count):
        if i + 1 == REPLACE[0]:
            out.insert_pdf(shell)
            continue
        if i + 1 in REPLACE:
            continue
        out.insert_pdf(master, from_page=i, to_page=i)
    out.set_metadata(master.metadata)
    print(f"master {master.page_count} pp + {shell.page_count} standardised pages "
          f"= {out.page_count} pp (shell pages {list(REPLACE)} replaced)")

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