#!/usr/bin/env python3
"""Measure the spine band and the front-cover left band of every BookVault wrap PNG.

Reports, per book: spine width from build.json, the expected spine colour, the
colour actually painted at the spine centre, and the colour painted on the
front cover's left vertical band. They must be the same colour.
"""
import glob
import json
import os
import sys

from PIL import Image

LIB = "/root/prime-books/public/library"
DPI = 300.0
MM = DPI / 25.4


def hexs(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


def med(im, x, y0, y1):
    """Median colour of a 3px-wide column strip at x, between y0..y1."""
    px = []
    for xx in (x - 1, x, x + 1):
        for yy in range(y0, y1, 7):
            px.append(im.getpixel((xx, yy)))
    px.sort(key=lambda c: sum(c))
    return px[len(px) // 2]


def probe(slug):
    png = os.path.join(LIB, slug, "bookvault", "%s-cover-file.png" % slug)
    if not os.path.exists(png):
        return None
    bj = os.path.join(LIB, slug, "bookvault", "build.json")
    spine = trim_w = None
    if os.path.exists(bj):
        try:
            cov = json.load(open(bj)).get("cover", {})
            spine = cov.get("spine_mm")
            trim_w = (cov.get("trim_mm") or [None])[0]
        except Exception:
            pass
    im = Image.open(png).convert("RGB")
    W, H = im.size
    total_mm = W / MM
    if not spine:
        return None
    back_mm = 3.0 + (trim_w or (total_mm - spine - 6.0 - 3.0))
    y0, y1 = int(H * 0.25), int(H * 0.75)
    spine_x = int((back_mm + spine / 2.0) * MM)
    # front cover's left vertical band: sample 4 mm into the front panel
    front_x = int((back_mm + spine + 6.0) * MM)
    back_x = int((back_mm - 4.0) * MM)
    return {
        "slug": slug,
        "mm": round(total_mm, 1),
        "spine_mm": spine,
        "expected": json.load(open(bj))["cover"].get("spine_colour") if os.path.exists(bj) else None,
        "spine": med(im, spine_x, y0, y1),
        "front": med(im, front_x, y0, y1),
        "back": med(im, back_x, y0, y1),
    }


slugs = sys.argv[1:] or sorted(
    os.path.basename(os.path.dirname(os.path.dirname(p)))
    for p in glob.glob(os.path.join(LIB, "*", "bookvault", "*-cover-file.png"))
)

rows = []
for s in slugs:
    r = probe(s)
    if r:
        rows.append(r)

bad = 0
print("%-28s %5s %6s  %-9s %-9s %-9s %-9s %s" % (
    "slug", "mm", "spine", "expected", "SPINE", "front-band", "back-band", "verdict"))
for r in rows:
    exp = hexs(r["expected"]) if r["expected"] else "-"
    ok = r["spine"] == r["front"]
    if not ok:
        bad += 1
    print("%-28s %5.1f %6.1f  %-9s %-9s %-9s %-9s %s" % (
        r["slug"], r["mm"], r["spine_mm"], exp,
        hexs(r["spine"]), hexs(r["front"]), hexs(r["back"]),
        "same" if ok else "*** MISMATCH ***"))
print("\n%d covers measured, %d with spine != front-cover left band" % (len(rows), bad))
