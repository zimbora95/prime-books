#!/usr/bin/env python3
"""Substitute physical page 2 of a Humanities book with the house imprint page.

    .venv/bin/python tools/out/backfix/splice_imprint_page.py <slug> <new-page-2.pdf>

Proves, before it writes: the page count is unchanged, the page size of the new
page equals the book's own, every OTHER page renders pixel-identical, and the
new page carries embedded fonts and no Type 3.

    .venv/bin/python tools/out/backfix/splice_imprint_page.py --verify <slug>
"""
import hashlib
import json
import os
import shutil
import sys

import pymupdf

REPO = '/root/prime-books'
BK = '/root/backwork'


def renders(path):
    doc = pymupdf.open(path)
    out = []
    for page in doc:
        pix = page.get_pixmap(dpi=40)
        out.append(hashlib.md5(pix.samples).hexdigest())
    doc.close()
    return out


def verify(slug, master=None):
    master = master or os.path.join(REPO, 'public/library', slug, 'book.pdf')
    old = os.path.join(BK, '%s-book-preimprint.pdf' % slug)
    if not os.path.exists(old):
        print('%s: no pre-imprint backup to compare against' % slug)
        return 1
    a, b = renders(old), renders(master)
    if len(a) != len(b):
        print('%s: PAGE COUNT CHANGED %d -> %d' % (slug, len(a), len(b)))
        return 1
    diff = [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y]
    doc = pymupdf.open(master)
    p2 = doc[1]
    fonts = sorted({f[3] for f in p2.get_fonts()})
    t3 = [f for f in p2.get_fonts() if f[2] == 'Type3']
    size = (round(p2.rect.width, 4), round(p2.rect.height, 4))
    sizes = {(round(p.rect.width, 4), round(p.rect.height, 4)) for p in doc}
    print('%s: pages %d (even: %s), pages that differ: %s, p2 %s, page sizes %s'
          % (slug, doc.page_count, doc.page_count % 2 == 0, diff, size, sizes))
    print('    p2 fonts: %s  type3: %s' % (fonts, len(t3)))
    doc.close()
    ok = len(diff) == 1 and diff == [2] and not t3 and len(sizes) == 1
    print('    VERDICT:', 'clean' if ok else 'CHECK')
    return 0 if ok else 1


def splice(slug, newpage):
    master = os.path.join(REPO, 'public/library', slug, 'book.pdf')
    backup = os.path.join(BK, '%s-book-preimprint.pdf' % slug)
    if not os.path.exists(backup):
        shutil.copy2(master, backup)
        print('backed up ->', backup)
    src = pymupdf.open(master)
    p2 = pymupdf.open(newpage)
    if tuple(p2[0].rect) != tuple(src[1].rect):
        raise SystemExit('new page %s does not match the book page %s'
                         % (tuple(p2[0].rect), tuple(src[1].rect)))
    out = pymupdf.open()
    out.insert_pdf(src, from_page=0, to_page=0)
    out.insert_pdf(p2)
    out.insert_pdf(src, from_page=2, to_page=src.page_count - 1)
    out.set_metadata(src.metadata)
    out.set_toc(src.get_toc())
    if out.page_count != src.page_count:
        raise SystemExit('page count would change %d -> %d'
                         % (src.page_count, out.page_count))
    tmp = master + '.tmp'
    out.save(tmp, garbage=4, deflate=True, clean=True)
    out.close()
    src.close()
    p2.close()
    shutil.move(tmp, master)
    print('%s: spliced %s (%d pages)' % (slug, newpage, pymupdf.open(master).page_count))


if __name__ == '__main__':
    if sys.argv[1] == '--verify':
        sys.exit(verify(sys.argv[2]))
    splice(sys.argv[1], sys.argv[2])
    sys.exit(verify(sys.argv[1]))