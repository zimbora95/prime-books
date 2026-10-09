#!/usr/bin/env python3
"""Verify every BookVault wrap against the book it is cut from.

For each pack: the recorded spine colour must be the book's own stripe (or the
year ladder when the book has no stripe), the wrap PNG's spine pixel must be
that colour, and the cover file must be newer than the master. Read-only.

    .venv/bin/python tools/out/backfix/verify_wraps.py
"""
import glob
import json
import os
import sys

import pymupdf
from PIL import Image

REPO = '/root/prime-books'
sys.path.insert(0, REPO + '/tools')
import make_wrap_cover as mwc  # noqa: E402

rows = {r['slug']: r for r in json.load(open(REPO + '/public/library.json'))}
bad, good, skip = [], [], []
for png in sorted(glob.glob(REPO + '/public/library/*/bookvault/*-cover-file.png')):
    slug = os.path.basename(os.path.dirname(os.path.dirname(png)))
    master = '%s/public/library/%s/book.pdf' % (REPO, slug)
    if slug not in rows:
        skip.append((slug, 'not in library.json'))
        continue
    rec = os.path.dirname(png) + '/build.json'
    if not os.path.isfile(rec):
        skip.append((slug, 'no build.json (full pack build needed)'))
        continue
    d = json.load(open(rec))
    cover = d.get('cover', {})
    own = mwc.book_stripe_colour(master)
    want = own or mwc.spine_colour(int(rows[slug]['year']))
    got = cover.get('spine_colour')
    try:
        im = Image.open(png).convert('RGB')
        W, H = im.size
        # the spine strip's solid colour, not the ink of the spine line that is
        # set across it: the MODE of a column, where the glyphs are the minority
        col = [im.getpixel((W // 2, y)) for y in range(0, H, 7)]
        px = max(set(col), key=col.count)
    except Exception as exc:            # a worker mid-write: skip this pass
        skip.append((slug, 'unreadable right now (%s)' % type(exc).__name__))
        continue
    fresh = os.path.getmtime(png) >= os.path.getmtime(master)
    problems = []
    if got is None:
        problems.append('no spine_colour recorded (pre-fix pack)')
    elif tuple(got) != tuple(want):
        problems.append('recorded %s != wanted %s' % (got, list(want)))
    if tuple(px) != tuple(want):
        problems.append('wire pixel %s != wanted %s' % (px, list(want)))
    if not fresh:
        problems.append('cover older than the master')
    (good if not problems else bad).append((slug, problems))

print('packs verified: %d ok, %d with findings, %d without a build record'
      % (len(good), len(bad), len(skip)))
for slug, probs in bad:
    print('  FINDING %-34s %s' % (slug, '; '.join(probs)))
for slug, why in skip:
    print('  SKIP    %-34s %s' % (slug, why))