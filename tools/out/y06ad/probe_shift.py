"""pick the smallest-|d| clean donor shift, then build the repaired art."""
import numpy as np
from PIL import Image, ImageFilter

im = Image.open('/tmp/y06ad/back_art.png').convert('L')
a = np.asarray(im).astype(np.float32)
H, W = a.shape
white = a > 248
mask = np.asarray(Image.fromarray((white * 255).astype(np.uint8))
                  .filter(ImageFilter.MaxFilter(5))) > 0
cand = []
for d in range(-(H - 1), H):
    if int((mask & np.roll(mask, d, axis=0)).sum()) == 0:
        cand.append(d)
cand.sort(key=abs)
for d in cand[:6]:
    src = np.roll(a, d, axis=0)
    print('d=%4d donor mean %.1f std %.2f' % (d, src[mask].mean(), src[mask].std()))