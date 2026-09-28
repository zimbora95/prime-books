"""Art helpers for Unit 3: split a 2x2 spot-art sheet into panels by white gutters, trim, save.
    python tools_art.py split art/sheet1.png desk,vento,chuva,livro
"""
import sys, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def trim(im, thr=242, pad=14):
    a = np.asarray(im.convert("L"))
    ys, xs = np.where(a < thr)
    if not len(xs):
        return im
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def gutter(prof, lo, hi):
    """longest run of near-white lines between lo and hi -> its centre"""
    best, cur, start, bs = 0, 0, 0, (lo + hi) // 2
    for i in range(lo, hi):
        if prof[i]:
            if cur == 0:
                start = i
            cur += 1
            if cur > best:
                best, bs = cur, start + cur // 2
        else:
            cur = 0
    return bs


def split(path, names):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im.convert("L")) > 238
    W, H = im.size
    cx = gutter(a.mean(0) > 0.985, int(W * .3), int(W * .7))
    cy = gutter(a.mean(1) > 0.985, int(H * .3), int(H * .7))
    boxes = [(0, 0, cx, cy), (cx, 0, W, cy), (0, cy, cx, H), (cx, cy, W, H)]
    for n, b in zip(names, boxes):
        if n == "-":
            continue
        p = trim(im.crop(b))
        # force pure white paper around the vignette
        arr = np.asarray(p).astype(np.int16)
        m = arr.min(2) > 236
        arr[m] = 255
        Image.fromarray(arr.astype(np.uint8)).save(os.path.join(HERE, "art", n + ".png"))
        print(n, b, p.size)


def blobs(path, names, thr=236, k=25):
    """split by connected ink blobs (robust when vignettes overlap the grid lines).
    names are assigned in reading order (top-left, top-right, bottom-left, bottom-right)."""
    import cv2
    im = Image.open(path).convert("RGB")
    g = np.asarray(im.convert("L"))
    ink = (g < thr).astype(np.uint8)
    ink = cv2.dilate(ink, np.ones((k, k), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink)
    comps = sorted([st[i] for i in range(1, n)], key=lambda s: -s[4])[:len(names)]
    H = im.height
    comps.sort(key=lambda s: (round((s[1] + s[3] / 2) / (H / 2.2)), s[0]))
    for nm, (x, y, w, h, a) in zip(names, comps):
        if nm == "-":
            continue
        crop = im.crop((max(0, x - 4), max(0, y - 4), min(im.width, x + w + 4), min(H, y + h + 4)))
        arr = np.asarray(crop).astype(np.int16)
        arr[arr.min(2) > 236] = 255
        Image.fromarray(arr.astype(np.uint8)).save(os.path.join(HERE, "art", nm + ".png"))
        print(nm, (x, y, w, h), "touches edge" if x < 3 or y < 3 or x + w > im.width - 3 or y + h > H - 3 else "")


if __name__ == "__main__":
    if sys.argv[1] == "split":
        split(sys.argv[2], sys.argv[3].split(","))
    elif sys.argv[1] == "blobs":
        blobs(sys.argv[2], sys.argv[3].split(","))
