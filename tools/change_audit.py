#!/usr/bin/env python3
"""Audit what the standardise pass actually did, per book.

Pixel bytes always differ (new embedded fonts rasterise slightly differently), so
compare STRUCTURE instead: page text, vector drawing count, image count, and which
fonts are embedded. A book whose only deltas are fonts did not visibly change.

    .venv/bin/python tools/change_audit.py [slug ...]
"""
import subprocess
import sys
from pathlib import Path

import pymupdf

REPO = Path("/root/prime-books")
BASE14 = {"helvetica", "helvetica-bold", "helvetica-oblique", "helvetica-boldoblique",
          "times-roman", "times-bold", "times-italic", "times-bolditalic",
          "courier", "courier-bold", "courier-oblique", "courier-boldoblique",
          "symbol", "zapfdingbats"}


def gitb(*a):
    return subprocess.run(["git", "-C", str(REPO), *a], capture_output=True).stdout


def fonts(doc):
    names, base14 = set(), 0
    for p in doc:
        for f in p.get_fonts():
            base = (f[3] or "").split("+")[-1].split("-")[0].lower()
            full = (f[3] or "").lower()
            names.add(full)
            if full in BASE14 or base in {"helvetica", "times", "courier"}:
                base14 += 1
    return names, base14


def audit(slug):
    rel = f"public/library/{slug}/book.pdf"
    c = subprocess.run(["git", "-C", str(REPO), "log", "--format=%H", "-1", "--", rel],
                       capture_output=True, text=True).stdout.strip()
    oldp = Path(f"/tmp/audit_{slug}_old.pdf")
    oldp.write_bytes(gitb("show", f"{c}^:{rel}"))
    o, n = pymupdf.open(oldp), pymupdf.open(REPO / rel)
    txt = vec = img = 0
    for i in range(min(len(o), len(n))):
        if o[i].get_text("text") != n[i].get_text("text"):
            txt += 1
        if len(o[i].get_drawings()) != len(n[i].get_drawings()):
            vec += 1
        if len(o[i].get_images()) != len(n[i].get_images()):
            img += 1
    fo, bo = fonts(o)
    fn, bn = fonts(n)
    verdict = "VISIBLE" if (txt or vec or img) else "fonts only (invisible)"
    return (f"{slug:30} pp {len(o):>3}->{len(n):<3} text-diff {txt:>3} vector-diff {vec:>3} "
            f"image-diff {img:>3} base14 {bo}->{bn}  {verdict}")


slugs = sys.argv[1:]
if not slugs:
    print("usage: change_audit.py <slug> ...")
    sys.exit(1)
for s in slugs:
    try:
        print(audit(s))
    except Exception as e:
        print(f"{s:30} ERROR {e}")