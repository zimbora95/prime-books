#!/usr/bin/env python3
"""Before/after evidence for one book's BookVault spine, from real pack pixels.

Usage: .venv/bin/python tools/out/y09ad/spine_before_after.py <slug> <before.png> [before-build.json]

Cuts the spine band (the spine plus 12 mm of each neighbour) out of the before
and the after cover file at full 300 DPI, rotates it so the spine line reads
normally, and stacks the two labelled strips into one landscape sheet. The
teacher sees the actual pixels of the uploaded cover files, not a screenshot.
"""
import pathlib
import json
import sys

from PIL import Image, ImageDraw, ImageFont

REPO = pathlib.Path("/root/prime-books")
LIB = REPO / "public" / "library"
FONTS = REPO / "public" / "Resources" / "Fonts"
DPI = 300
MM = DPI / 25.4
CAP = 76            # caption strip height, px
CROP_H = 1500       # vertical slice of the spine, px (text sits in the middle)


def font(size):
    return ImageFont.truetype(str(FONTS / "Sora.dl"), size)


def band(png, build):
    b = json.loads(pathlib.Path(build).read_text())
    cov = b["cover"]
    spine_mm, trim_w = cov["spine_mm"], cov["trim_mm"][0]
    im = Image.open(png).convert("RGB")
    W, H = im.size
    back_mm = 3.0 + trim_w
    x0 = max(0, int((back_mm - 12.0) * MM))
    x1 = min(W, int((back_mm + spine_mm + 12.0) * MM))
    y0 = H // 2 - CROP_H // 2
    strip = im.crop((x0, y0, x1, y0 + CROP_H))
    return strip.transpose(Image.ROTATE_90), spine_mm, bool(cov.get("spine_text")), \
        cov.get("spine_text_pt")


def main():
    slug = sys.argv[1]
    before_png = sys.argv[2]
    before_build = sys.argv[3] if len(sys.argv) > 3 else None
    pack = LIB / slug / "bookvault"
    if not before_build:
        before_build = pathlib.Path("/tmp") / f"{slug}-build-before.json"

    rows = []
    for tag, png, build in (("BEFORE", before_png, before_build),
                            ("AFTER", pack / f"{slug}-cover-file.png", pack / "build.json")):
        strip, mm, has, pt = band(png, build)
        rows.append((tag, strip, mm, has, pt))

    W = max(r[1].width for r in rows)
    H = sum(CAP + r[1].height for r in rows)
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    f, fs = font(38), font(30)
    y = 0
    for tag, strip, mm, has, pt in rows:
        d.rectangle([0, y, W, y + CAP], fill=(24, 28, 34))
        line = (f"spine {has and 'CARRIES' or 'PLAIN - no'} "
                f"{has and 'the standard line (subject - year / imprint)' or 'standard line'}"
                f"   -   spine {mm:g} mm, type {pt or 0:g} pt   -   {slug}")
        d.text((20, y + 20), line, font=f if len(line) < 78 else fs,
               fill=(246, 241, 230))
        y += CAP
        sheet.paste(strip, (0, y))
        y += strip.height
    out = REPO / "tools" / "out" / "y09ad" / f"{slug}-spine-before-after.png"
    sheet.save(out, "PNG", optimize=True)
    print(out, sheet.size)

    # a plain zoom of the AFTER spine for the vision check
    after = Image.open(pack / f"{slug}-cover-file.png").convert("RGB")
    W2, H2 = after.size
    b = json.loads((pack / "build.json").read_text())["cover"]
    x0 = int((3.0 + b["trim_mm"][0]) * MM) - 10
    x1 = x0 + round(b["spine_mm"] * MM) + 20
    zoom = after.crop((x0, H2 // 2 - 700, x1, H2 // 2 + 700))
    zoom.transpose(Image.ROTATE_90).save("/tmp/%s-spine-after.png" % slug)
    print("zoom:", zoom.width, "x", zoom.height)


if __name__ == "__main__":
    main()
