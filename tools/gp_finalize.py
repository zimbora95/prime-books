#!/usr/bin/env python
"""Finalize the two Global Perspectives books once webopt + BookVault packs land.

Steps per slug:
  1. book.web.pdf -> book.pdf           (the SERVED copy; full masters stay in work/gp-print/)
  2. render the /finished previews      (tools/finished_previews.render -> preview/01|02|last.webp)
  3. refresh `mb` + `preview` on the two library.json rows,
     keeping library.json's on-disk format: indent=1, ensure_ascii=False, no trailing newline.

Run:  .venv/bin/python gp_finalize.py [--dry]
"""
import json
import os
import sys

sys.path.insert(0, '/root/prime-books/tools')
import finished_previews as fp  # noqa: E402

REPO = '/root/prime-books'
SLUGS = ['y08-global-perspectives', 'y09-global-perspectives']
DRY = '--dry' in sys.argv

summary = {}
for slug in SLUGS:
    d = os.path.join(REPO, 'public/library', slug)
    web, pdf, pack = (os.path.join(d, f) for f in ('book.web.pdf', 'book.pdf', 'bookvault/build.json'))
    have = {'web': os.path.exists(web), 'pdf': os.path.exists(pdf), 'pack': os.path.exists(pack)}
    print(slug, have)
    if DRY:
        continue
    if not have['pack']:
        print('  SKIP: BookVault pack not finished yet')
        continue
    if have['web']:
        os.replace(web, pdf)
        print('  book.web.pdf -> book.pdf')
    prev = fp.render(slug, pdf)
    mb = round(os.path.getsize(pdf) / 1e6, 2)
    summary[slug] = {'mb': mb, 'preview': prev}
    print('  mb=%s preview=%s' % (mb, prev))

if summary and not DRY:
    lp = os.path.join(REPO, 'public/library.json')
    rows = json.load(open(lp, encoding='utf-8'))
    for r in rows:
        if r.get('slug') in summary:
            r['mb'] = summary[r['slug']]['mb']
            r['preview'] = summary[r['slug']]['preview']
            print('library.json: refreshed', r['slug'], r['mb'])
    open(lp, 'w', encoding='utf-8').write(json.dumps(rows, ensure_ascii=False, indent=1))
    print('done.')
