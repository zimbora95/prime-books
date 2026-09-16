#!/usr/bin/env python3
"""Render the three pages the /finished shelf shows for every Prime Book.

The shelf shows a book by its front cover, its page 2 and its back cover, so a
teacher can see at a glance what a title actually looks like inside. Those three
pages are rendered here, once, into

    public/library/<slug>/preview/01.webp     the front cover
    public/library/<slug>/preview/02.webp     the second page
    public/library/<slug>/preview/last.webp   the back cover

and the paths are written onto each manifest row as `preview`, so the page is a
data read rather than a guess and a book without previews simply falls back to
its cover.

Rendering is incremental: a preview older than its PDF is re-rendered, a current
one is left alone, so a rebuild after one book changes costs one book.

    .venv/bin/python tools/finished_previews.py            # everything stale
    .venv/bin/python tools/finished_previews.py y08-humanities
"""
import json
import os
import sys

import pymupdf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO, "public", "library.json")
WIDTH = 420                     # what a shelf tile needs on a laptop


def render(slug, pdf_path):
    """Page 1, page 2 and the last page of one book, as webp tiles."""
    outdir = os.path.join(REPO, "public", "library", slug, "preview")
    os.makedirs(outdir, exist_ok=True)
    wants = {"01": 1, "02": 2, "last": None}
    made = {}
    doc = pymupdf.open(pdf_path)
    try:
        for name, number in wants.items():
            page = doc[0] if number is None else doc[min(number, doc.page_count) - 1]
            if number is None:
                page = doc[doc.page_count - 1]
            dst = os.path.join(outdir, f"{name}.webp")
            if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(pdf_path):
                made[name] = f"/library/{slug}/preview/{name}.webp"
                continue
            scale = WIDTH / page.rect.width
            pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
            from PIL import Image
            Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(
                dst, "WEBP", quality=82, method=6)
            made[name] = f"/library/{slug}/preview/{name}.webp"
    finally:
        doc.close()
    return [made["01"], made["02"], made["last"]]


def main(argv):
    only = [a for a in argv[1:] if not a.startswith("-")]
    rows = json.load(open(MANIFEST))
    done = skipped = failed = 0
    for r in rows:
        slug = r.get("slug")
        if not slug or (only and slug not in only):
            continue
        pdf = os.path.join(REPO, "public", r.get("pdf", "").lstrip("/"))
        if not os.path.exists(pdf):
            print(f"  ! {slug}: no pdf at {r.get('pdf')}")
            failed += 1
            continue
        fresh = all(
            os.path.exists(os.path.join(REPO, "public", "library", slug, "preview", f)) and
            os.path.getmtime(os.path.join(REPO, "public", "library", slug, "preview", f))
            >= os.path.getmtime(pdf)
            for f in ("01.webp", "02.webp", "last.webp"))
        r["preview"] = render(slug, pdf)
        if fresh:
            skipped += 1
        else:
            done += 1
            print(f"  rendered {slug}")
    json.dump(rows, open(MANIFEST, "w"), indent=2)      # the house format: indent 2
    print(f"previews: {done} rendered, {skipped} already current, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
