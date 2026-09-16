#!/usr/bin/env python3
"""Redraw the contents-page plate for /years-1-4 in the enhanced design.

The old plate showed six bar segments, four cards and loose back-matter rows -
it would now contradict the prose beside it. Drawn rather than generated: a flat
wireframe has to get the counts (0-7, eight cards, Unit 7 last) exactly right,
and an image model will not count.

    .venv/bin/python tools/pb_contents_mock.py
"""
import json
import os

from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = json.load(open(os.path.join(REPO, "public/standards/years-1-4.json")))
OUT = os.path.join(REPO, "public/standards/art/y1-4-contents-mock.webp")
W, H = 1024, 1536
PAPER = (251, 248, 240)
RULE = (196, 190, 178)
INK = (78, 72, 92)
MUTED = (168, 162, 156)


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


rungs = {r["unit"]: r for r in TOK["unit_palette"]["rungs"]}
keys = [0, 1, 2, 3, 4, 5, 6, 7]

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)
M = 74

# the colour bar: one segment per block, numbered 0 to the last unit
bar_y, bar_h, gap = 120, 46, 10
seg = (W - 2 * M - gap * (len(keys) - 1)) / len(keys)
for i, k in enumerate(keys):
    x = M + i * (seg + gap)
    d.rounded_rectangle([x, bar_y, x + seg, bar_y + bar_h], radius=8,
                        fill=rgb(rungs[k]["mid"]))
    d.text((x + seg / 2 - 4, bar_y + 16), str(k), fill=(255, 255, 255))

# page title placeholder
d.rounded_rectangle([M, bar_y + bar_h + 42, M + 520, bar_y + bar_h + 74], radius=6,
                    fill=(232, 228, 220))
d.rounded_rectangle([M, bar_y + bar_h + 88, M + 300, bar_y + bar_h + 108], radius=5,
                    fill=(238, 235, 228))

# eight cards, two to a row: Unit 0 opens the grid, Unit 7 closes it
grid_y = bar_y + bar_h + 150
card_w = (W - 2 * M - 26) / 2
card_h = (H - grid_y - M - 3 * 22) / 4
for i, k in enumerate(keys):
    col, row = i % 2, i // 2
    cx = M + col * (card_w + 26)
    cy = grid_y + row * (card_h + 22)
    tint = rgb(rungs[k]["tint"])
    d.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=14, fill=tint)
    d.rectangle([cx, cy, cx + 8, cy + card_h], fill=rgb(rungs[k]["mid"]))
    tx = cx + 26
    y = cy + 22
    # unit label line, then the card's name, then its summary
    d.rounded_rectangle([tx, y, tx + 130, y + 12], radius=4, fill=rgb(rungs[k]["mid"]))
    d.rounded_rectangle([tx, y + 24, tx + 260, y + 40], radius=5, fill=(210, 204, 196))
    d.rounded_rectangle([tx, y + 50, tx + 330, y + 62], radius=4, fill=(224, 219, 211))
    rows_y = y + 78
    bookend = k in (0, 7)
    for r in range(4):
        ry = rows_y + r * 22
        if ry + 12 > cy + card_h - 14:
            break
        d.rounded_rectangle([tx, ry, tx + 210, ry + 10], radius=3,
                            fill=(200, 196, 190) if not bookend else (186, 182, 176))
        d.rounded_rectangle([cx + card_w - 40, ry, cx + card_w - 26, ry + 10], radius=3,
                            fill=rgb(rungs[k]["deep"]))
        if bookend:                      # those rows are pages, so leaders
            lx = tx + 218
            while lx < cx + card_w - 48:
                d.rectangle([lx, ry + 5, lx + 5, ry + 6], fill=MUTED)
                lx += 14

# the folio badge, mirrored where the plate shows the right-hand page
d.ellipse([W - M - 26, H - M - 14, W - M + 26, H - M + 38], fill=rgb(TOK["year_stripes"]["1"]))

im.save(OUT, quality=90, method=5)
print("wrote", os.path.relpath(OUT, REPO), im.size, os.path.getsize(OUT), "bytes")