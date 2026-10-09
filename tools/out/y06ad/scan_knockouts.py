"""Read-only corpus scan: which Prime Books backs carry the same damage class as
y06-art-and-design -- a full-page raster back cover with opaque WHITE knockout
bars baked into the art where the subtitle/hook/blurb used to be (residue of a
redaction with the default white fill on an image-backed page).

A knockout bar is at least 100pt of contiguous pure-white (>248) pixels inside
the header/blurb band (page y 110-300) of the back page's own raster.
"""
import glob
import io
import os

import numpy as np
import pymupdf
from PIL import Image

BOOKS = sorted(glob.glob('/root/prime-books/public/library/*/book.pdf'))
hits = []
for path in BOOKS:
    slug = path.split('/')[-2]
    try:
        d = pymupdf.open(path)
        p = d[-1]
        ims = p.get_images(full=True)
        if not ims:
            d.close()
            continue
        rects = p.get_image_rects(ims[0][0])
        full = rects and rects[0].width > 500 and rects[0].height > 700
        if not full:
            d.close()
            continue
        info = d.extract_image(ims[0][0])
        a = np.asarray(Image.open(io.BytesIO(info['image'])).convert('L')).astype(np.float32)
        sc = a.shape[1] / 612.0
        band = a[int(110 * sc):int(300 * sc)] > 248
        best = cur = 0
        for row in band:
            cur = 0
            for v in row:
                cur = cur + 1 if v else 0
                if cur > best:
                    best = cur
        best_pt = best / sc
        if best_pt >= 100:
            hits.append((slug, round(best_pt, 1), d.page_count))
        d.close()
    except Exception as e:
        print('SKIP', slug, e)
print('books with a full-page raster back:', len(BOOKS))
print('backs carrying baked white knockout bars (>=100pt run):', len(hits))
for s, w, n in sorted(hits):
    print('   %-34s longest white run %6.1f pt   %d pp' % (s, w, n))
