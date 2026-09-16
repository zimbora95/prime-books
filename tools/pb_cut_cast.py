#!/usr/bin/env python3
"""Cut the approved cast portraits out of their cream background.

The six portraits are sliced from the character sheet the teacher approved, so
regenerating them would risk drift. Their background is EXACTLY one colour
(249,243,230 - zero variance around the whole border of all six), so the cut is
deterministic:

  1. flood-fill that colour inward from every border pixel (PIL's fill with a
     tolerance), so cream INSIDE a character - an owl's face, a pale apron - is
     never punched out, only the background that touches the outside;
  2. alpha from the fill, feathered 1 px so the silhouette keeps its soft edge;
  3. trim to the figure and scale all six to one common height, so the row sits
     on a single baseline instead of six different sizes.

    .venv/bin/python cut_cast.py            # writes art/cast-N-*.png (RGBA)
    .venv/bin/python cut_cast.py --check    # writes art/cast-cut-check.png
"""
import glob
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

WORK = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(WORK, "art")
BG = (249, 243, 230)          # measured: the sheet's exact background
MARK = (255, 0, 255)
# the background is uniform; a tight tolerance keeps pale fur from being eaten.
# Raised from the command line (CUT_THRESH=26) when a figure's fine detail - a
# hedgehog's spines - leaves paper in the gaps the fill cannot reach.
THRESH = float(os.environ.get("CUT_THRESH", "12"))
TARGET_H = 900                # common figure height, for one baseline
PAD = 6


def defringe(out, tol=60.0):
    """Unmix the paper out of the antialiased silhouette edge.

    The flood fill leaves the blend between figure and paper opaque: those
    pixels are (paper * (1-a) + figure * a) for the coverage a. Over cream paper
    they disappear; over WHITE they read as a pale box, which is exactly the
    defect the teacher's eye catches. Recovering the figure's own colour from
    the blend removes the paper from the edge, so the cut is clean on any
    background - the panel can then be white, as asked.
    """
    px = out.load()
    w, h = out.size
    fixed = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if min(px[x + dx, y + dy][3]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) == 255:
                continue                     # interior: nothing to unmix
            # only touch pixels that are plausibly a paper blend
            if max(abs(r - BG[0]), abs(g - BG[1]), abs(b - BG[2])) > tol:
                continue
            af = a / 255.0
            if af <= 0.05:
                px[x, y] = (0, 0, 0, 0)
                fixed += 1
                continue
            px[x, y] = tuple(
                min(255, max(0, round((c - (1 - af) * bgc) / af)))
                for c, bgc in zip((r, g, b), BG)) + (a,)
            fixed += 1
    return fixed


def cut(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    work = im.copy()
    # seed from all four corners and the edge midpoints: one seed is enough for a
    # connected background, but the corners are not guaranteed to be outside a
    # figure that bleeds off the crop.
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
                 (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if work.getpixel(seed) != MARK:
            ImageDraw.floodfill(work, seed, MARK, thresh=THRESH)
    mask = Image.new("L", (w, h), 255)
    mp = mask.load()
    wp = work.load()
    for y in range(h):
        for x in range(w):
            if wp[x, y] == MARK:
                mp[x, y] = 0
    # The fill leaves the antialiased blend between figure and paper opaque, and
    # over a tint that reads as a pale fringe - the "faint box" the teacher's
    # eye catches. Erode the mask by two pixels so that ring is cut away (at
    # 900 px tall that is ~0.7 pt in print, invisible), then soften the edge.
    mask = mask.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.6))
    out = im.convert("RGBA")
    out.putalpha(mask)
    removed = defringe(out)
    bbox = out.getbbox()
    if not bbox:
        raise SystemExit(f"{path}: nothing left after the cut")
    out = out.crop(bbox)
    print(f"  defringe: {removed} edge pixels unmixed in {os.path.basename(path)}")
    return out, bbox


def main():
    check = "--check" in sys.argv
    files = sorted(glob.glob(os.path.join(ART, "cast-[0-9]-*.png")))
    files = [f for f in files if "-cut" not in f]
    if not files:
        raise SystemExit("no art/cast-N-*.png to cut")
    cut_files, sizes = [], []
    for f in files:
        out, bbox = cut(f)
        sizes.append((os.path.basename(f), out.size, bbox))
        cut_files.append((f, out))
    # ONE common factor, not a common height: a hare is tall and a hedgehog is
    # small, and normalising height would inflate the hedgehog past the badger.
    # Preserving the drawn proportions is what keeps the six looking like
    # themselves; they are then bottom-aligned by the page, not by the crop.
    factor = TARGET_H / max(out.height for _, out in cut_files)
    frak = {}
    for f, out in cut_files:
        nw, nh = max(1, round(out.width * factor)), max(1, round(out.height * factor))
        small = out.resize((nw, nh), Image.LANCZOS)
        dest = f.replace(".png", "-cut.png")
        # a TIGHT card - the figure and a hair of padding, no air above it. The
        # page then sets each figure's drawn height itself, which is how the six
        # keep their drawn proportions while the shortest stops floating.
        canvas = Image.new("RGBA", (nw + PAD * 2, nh + PAD * 2), (0, 0, 0, 0))
        canvas.alpha_composite(small, (PAD, PAD))
        canvas.save(dest)
        frak[os.path.basename(dest)] = nh / max(out.height * factor for _, out in cut_files)
        print(f"  {os.path.basename(dest)} {canvas.size}  figure {nw}x{nh}  "
              f"frac {frak[os.path.basename(dest)]:.3f}")

    # the page needs to know how tall each figure is relative to the tallest
    castpath = os.path.join(ART, "cast.json")
    cast = json.load(open(castpath))
    for c in cast["cast"]:
        c["frac"] = round(frak.get(c["file"], 1.0), 4)
    cast["proportions"] = ("frac is this figure's drawn height divided by the tallest, "
                           "measured from the approved sheet; the welcome page draws "
                           "each at (frac ** 0.45) of the row height, so the hare stays "
                           "tallest and the hedgehog stops floating")
    json.dump(cast, open(castpath, "w"), indent=1)

    if check:
        # contact sheet on WHITE - the panel is white now, and white is where a
        # surviving thread of cream paper shows
        band = Image.new("RGB", (sum(Image.open(f.replace('.png', '-cut.png')).width
                                     for f, _ in cut_files) + 40, TARGET_H + 80),
                         (255, 255, 255))
        x = 20
        for f, _ in cut_files:
            im = Image.open(f.replace(".png", "-cut.png"))
            band.paste(im, (x, 40), im)
            x += im.width
        out = os.path.join(ART, "cast-cut-check.png")
        band.save(out)
        print("contact sheet:", out, band.size)
    for name, size, bbox in sizes:
        print(f"  {name}: {size} bbox {bbox}")


if __name__ == "__main__":
    main()
