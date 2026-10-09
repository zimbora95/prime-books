"""Strict read-only scan for the y06-art-and-design damage signature.

A knockout bar is a FLAT, EXACTLY-white rectangle >= 80pt wide and >= 10pt tall
inside the back page's header/blurb band: the raster's own texture is gone, which
is what a redaction's white fill looks like once it is baked into an image.
"""
import glob
import io

import numpy as np
import pymupdf
from PIL import Image

BOOKS = sorted(glob.glob('/root/prime-books/public/library/y0[1-6]-*/book.pdf'))
print('scanning %d Year 1-6 books' % len(BOOKS))
for path in BOOKS:
    slug = path.split('/')[-2]
    try:
        d = pymupdf.open(path)
        p = d[-1]
        ims = p.get_images(full=True)
        if not ims:
            d.close()
            continue
        r = p.get_image_rects(ims[0][0])
        if not (r and r[0].width > 500 and r[0].height > 700):
            d.close()
            continue
        a = np.asarray(Image.open(io.BytesIO(d.extract_image(ims[0][0])['image']))
                       .convert('L')).astype(np.uint8)
        sc = a.shape[1] / 612.0
        band = a[int(100 * sc):int(310 * sc)]
        flat = band >= 254
        rows = flat.sum(axis=1)
        # longest exactly-white run per row
        long_rows = []
        for y in range(flat.shape[0]):
            best = cur = 0
            for v in flat[y]:
                cur = cur + 1 if v else 0
                if cur > best:
                    best = cur
            if best >= 80 * sc:
                long_rows.append((y, best / sc))
        if len(long_rows) >= 10 * sc:
            ys = [y for y, _ in long_rows]
            print('  DAMAGED? %-28s %d flat rows, longest %.0f pt, page y %.0f-%.0f'
                  % (slug, len(long_rows), max(w for _, w in long_rows),
                     (ys[0] + 100 * sc) / sc, (ys[-1] + 100 * sc) / sc))
        d.close()
    except Exception as e:
        print('  SKIP', slug, e)