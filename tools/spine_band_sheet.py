#!/usr/bin/env python3
"""Build one proof sheet: for each book, the real spine pixels beside the real
front-cover left-band pixels, plus the colour swatch, straight out of the file
that gets uploaded to BookVault. No invented colours, no UI screenshots."""
import json
import os

from PIL import Image, ImageDraw, ImageFont

LIB = "/root/prime-books/public/library"
DPI = 300.0
MM = DPI / 25.4
OUT = "/tmp/spine-vs-frontband-sheet.png"

BOOKS = [
    ("y07-humanities", "Year 7 Humanities"),
    ("y08-humanities", "Year 8 Humanities"),
    ("y09-humanities", "Year 9 Humanities"),
    ("y07-art-and-design", "Year 7 Art & Design"),
    ("y08-art-and-design", "Year 8 Art & Design"),
    ("y09-art-and-design", "Year 9 Art & Design"),
]

try:
    f_label = ImageFont.load_default(size=30)
    f_big = ImageFont.load_default(size=34)
    f_hex = ImageFont.load_default(size=28)
except Exception:
    f_label = f_big = f_hex = ImageFont.load_default()

ROW_H = 300
THUMB_H = 230
STRIP_W = 150
SWATCH_W = 210
PAD = 18


def load(slug):
    png = os.path.join(LIB, slug, "bookvault", "%s-cover-file.png" % slug)
    bj = json.load(open(os.path.join(LIB, slug, "bookvault", "build.json")))
    cov = bj.get("cover", {})
    im = Image.open(png).convert("RGB")
    return im, cov


def strip(im, x0_mm, x1_mm):
    W, H = im.size
    box = (int(x0_mm * MM), int(H * 0.22), int(x1_mm * MM), int(H * 0.78))
    return im.crop(box)


def dominant(im):
    from collections import Counter
    c = Counter(im.getdata())
    return c.most_common(1)[0][0]


rows = []
for slug, name in BOOKS:
    im, cov = load(slug)
    W, H = im.size
    total_mm = W / MM
    spine = cov["spine_mm"]
    back_mm = 3.0 + cov["trim_mm"][0]
    sp = strip(im, back_mm, back_mm + spine)
    fb = strip(im, back_mm + spine, back_mm + spine + 12.5)
    rows.append((name, im, sp, fb, dominant(sp), dominant(fb), spine, cov["spine_colour"]))

WIDTH = PAD + THUMB_H * 1.49 + PAD * 2 + STRIP_W + SWATCH_W + STRIP_W + PAD + 460
HEIGHT = PAD + len(rows) * (ROW_H + PAD) + 70
canvas = Image.new("RGB", (int(WIDTH), int(HEIGHT)), (255, 255, 255))
d = ImageDraw.Draw(canvas)

d.text((PAD, 14), "BookVault files as uploaded: spine band vs the front cover's left vertical band",
       fill=(20, 20, 20), font=f_big)

y = 70
for name, im, sp, fb, c_sp, c_fb, spine_mm, expected in rows:
    tw = int(THUMB_H * (im.size[0] / im.size[1]))
    canvas.paste(im.resize((tw, THUMB_H), Image.LANCZOS), (PAD, y + 30))
    x = PAD + tw + PAD * 2
    canvas.paste(sp.resize((STRIP_W, ROW_H - 20), Image.LANCZOS), (x, y))
    d.text((x, y + ROW_H - 16), "spine", fill=(60, 60, 60), font=f_hex)
    x += STRIP_W + PAD
    d.rectangle([x, y, x + SWATCH_W - 30, y + ROW_H - 30], fill=c_sp, outline=(0, 0, 0))
    d.text((x + 8, y + 10), "#%02X%02X%02X" % c_sp, fill=(255, 255, 255), font=f_hex)
    x += SWATCH_W + PAD
    canvas.paste(fb.resize((STRIP_W, ROW_H - 20), Image.LANCZOS), (x, y))
    d.text((x, y + ROW_H - 16), "front band", fill=(60, 60, 60), font=f_hex)
    x += STRIP_W + PAD
    verdict = "identical" if c_sp == c_fb else "MISMATCH"
    d.text((x, y + 40), name, fill=(20, 20, 20), font=f_big)
    d.text((x, y + 90), "spine %.1f mm" % spine_mm, fill=(60, 60, 60), font=f_label)
    d.text((x, y + 130), "spine #%02X%02X%02X" % c_sp, fill=(60, 60, 60), font=f_label)
    d.text((x, y + 170), "front #%02X%02X%02X   %s" % (c_fb[0], c_fb[1], c_fb[2], verdict),
           fill=(0, 110, 0) if c_sp == c_fb else (190, 0, 0), font=f_label)
    y += ROW_H + PAD

canvas.save(OUT)
print("saved", OUT, canvas.size)
for name, im, sp, fb, c_sp, c_fb, spine_mm, expected in rows:
    print("%-20s spine #%02X%02X%02X  front #%02X%02X%02X  %s" % (
        name, c_sp[0], c_sp[1], c_sp[2], c_fb[0], c_fb[1], c_fb[2],
        "identical" if c_sp == c_fb else "MISMATCH"))
