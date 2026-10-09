#!/usr/bin/env python3
"""Evidence renders for the Year 7-9 Portuguese 2nd front-matter/back-cover job.

Per book: page 2 before (pre-edit master) beside page 2 after, and the back
cover before beside the back cover after. Plus the new Year 7 back beside the
house reference back (y07-art-and-design, the standard).

    .venv/bin/python tools/out/pt2/evidence.py
"""
import os

import pymupdf
from PIL import Image, ImageDraw

REPO = '/root/prime-books'
WORK = '/root/backwork/pt2'
OUT = '/root/backwork/pt2/renders'
W = 620


def page_png(path, index, out):
    d = pymupdf.open(path)
    idx = index if index >= 0 else d.page_count + index
    p = d[idx]
    z = W / p.rect.width
    pix = p.get_pixmap(matrix=pymupdf.Matrix(z, z))
    Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(out)
    d.close()
    return Image.open(out)


def pair(left, right, lab_l, lab_r, out, note):
    ims = [left, right]
    h = max(i.height for i in ims)
    pad, bar, gap = 12, 26, 16
    canvas = Image.new('RGB', (pad * 2 + left.width + right.width + gap, h + bar + pad), 'white')
    dr = ImageDraw.Draw(canvas)
    x = pad
    for im, lab in zip(ims, (lab_l, lab_r)):
        dr.text((x + 4, 8), lab, fill=(180, 0, 0))
        canvas.paste(im, (x, bar))
        x += im.width + gap
    dr.text((pad + 4, h + bar + 6), note, fill=(60, 60, 60))
    canvas.save(out)
    print('wrote', out, canvas.size)


def main():
    os.makedirs(OUT, exist_ok=True)
    ref = page_png(os.path.join(REPO, 'public/library/y07-art-and-design/book.pdf'),
                   -1, OUT + '/_ref.png')
    for slug in ['y07-portuguese-2nd', 'y08-portuguese-2nd', 'y09-portuguese-2nd']:
        pre = os.path.join(WORK, '%s-book-preimprint.pdf' % slug)
        now = os.path.join(REPO, 'public/library/%s/book.pdf' % slug)
        b2 = page_png(pre, 1, OUT + '/_b2.png')
        a2 = page_png(now, 1, OUT + '/_a2.png')
        pair(b2, a2, '%s - page 2 BEFORE (no imprint page)' % slug,
             'AFTER (house imprint standard)', '%s/%s-page2-before-after.png' % (OUT, slug),
             'inserted as physical page 2; every page after it renumbered; '
             'nothing removed from the book')
        bb = page_png(pre, -1, OUT + '/_bb.png')
        ab = page_png(now, -1, OUT + '/_ab.png')
        pair(bb, ab, 'back cover BEFORE (sweep damage)',
             'AFTER (house back-cover standard)',
             '%s/%s-back-before-after.png' % (OUT, slug),
             'PRIME SCHOOL PRESS imprint, standard geometry, the pre-sweep art '
             'restored 1:1, the book\'s own hook/blurb/bullets')
        if slug == 'y07-portuguese-2nd':
            pair(ref, ab, 'REFERENCE: y07-art-and-design back (house standard)',
                 'y07-portuguese-2nd NEW back',
                 '%s/%s-back-vs-reference.png' % (OUT, slug),
                 'measured: imprint 67.9, title 93.4, accent 166-169, subtitle '
                 '174.6, hook 200.1, blurb 224.3+17.2, card 364.3-512.3, footer H-74.5/-60/-42.5')


if __name__ == '__main__':
    main()
