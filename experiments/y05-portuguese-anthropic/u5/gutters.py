"""Find white gutters in a generated multi-panel sheet: python gutters.py img.png"""
import sys
import numpy as np
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(im).astype(int)
nonw = a.sum(2) < 735
W, H = im.size
print("size", im.size)
rows, cols = nonw.mean(1), nonw.mean(0)


def runs(v, lo, hi):
    out, s = [], None
    for i in range(lo, hi):
        if v[i] < 0.004:
            s = i if s is None else s
        elif s is not None:
            out.append((s, i - 1)); s = None
    if s is not None:
        out.append((s, hi - 1))
    return out


print("white rows", runs(rows, 0, H))
print("white cols", runs(cols, 0, W))
