#!/usr/bin/env python3
"""Contact sheet: the spine band of the four books that now carry the line.

Cuts the spine (plus 6 mm of each neighbour) out of each pack's current cover
file at 300 DPI, rotates it to read normally, and stacks the four labelled
strips. Real pixels from the uploaded cover files.
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

REPO = pathlib.Path("/root/prime-books")
LIB = REPO / "public" / "library"
FONTS = REPO / "public" / "Resources" / "Fonts"
DPI = 300
MM = DPI / 25.4
SLUGS = ["y01-english-standard", "y01-physical-education-standard",
         "y04-mathematics", "y09-art-and-design"]
CAP = 58
CROP_H = 1300


def font(s):
    return ImageFont.truetype(str(FONTS / "Sora.dl"), s)


rows = []
for slug in SLUGS:
    pack = LIB / slug / "bookvault"
    b = json.loads((pack / "build.json").read_text())["cover"]
    im = Image.open(pack / f"{slug}-cover-file.png").convert("RGB")
    W, H = im.size
    x0 = max(0, int((3.0 + b["trim_mm"][0] - 6.0) * MM))
    x1 = min(W, int((3.0 + b["trim_mm"][0] + b["spine_mm"] + 6.0) * MM))
    strip = im.crop((x0, H // 2 - CROP_H // 2, x1, H // 2 + CROP_H // 2))
    rows.append((slug, strip.transpose(Image.ROTATE_90), b))

W = max(r[1].width for r in rows)
H = sum(CAP + r[1].height for r in rows)
sheet = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(sheet)
f = font(34)
y = 0
for slug, strip, b in rows:
    d.rectangle([0, y, W, y + CAP], fill=(24, 28, 34))
    d.text((16, y + 12), f"{slug}   -   spine {b['spine_mm']:g} mm, "
           f"type {b['spine_text_pt']:g} pt, colour #{''.join('%02X' % c for c in b['spine_colour'])}",
           font=f, fill=(246, 241, 230))
    y += CAP
    sheet.paste(strip, (0, y))
    y += strip.height
out = REPO / "tools" / "out" / "y09ad" / "spine-line-4mm-books.png"
sheet.save(out, "PNG", optimize=True)
print(out, sheet.size)
