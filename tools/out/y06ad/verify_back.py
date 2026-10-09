"""Verify the rebuilt y06-art-and-design back cover against the house standard and
against the Year 3 / Year 4 Art & Design backs (the measured references)."""
import numpy as np
import pymupdf
from PIL import Image

REF = {  # y03/y04 art-and-design backs, measured
    'imprint_top': 67.9, 'imprint_size': 9.6,
    'title_top': 93.4, 'title_size': 33.0,
    'subtitle_top': 174.6, 'subtitle_size': 11.0,
    'hook_top': 200.1, 'hook_size': 11.4,
    'bullets_top': 395.7, 'card': (71.0, 364.3, 470.0, 512.3),
    'footer_tops': (717.5, 732.0, 749.5),
}

d = pymupdf.open('public/library/y06-art-and-design/book.pdf')
p = d[-1]
print('pages', d.page_count, '| back page', p.rect, '| media even:', d.page_count % 2 == 0)
spans = []
for b in p.get_text('dict')['blocks']:
    if b['type'] == 0:
        for l in b['lines']:
            for s in l['spans']:
                spans.append((round(s['bbox'][0], 1), round(s['bbox'][1], 1),
                              round(s['bbox'][2], 1), round(s['bbox'][3], 1),
                              s['font'], round(s['size'], 2), hex(s['color']), s['text']))
for s in spans:
    print(s[:7], repr(s[7]))
draws = [(tuple(dr['fill']), tuple(round(v, 1) for v in dr['rect'])) for dr in p.get_drawings()]
print('drawings:', draws)

# --- standard checks ---
imprint = [s for s in spans if s[7].startswith('P R I M E')][0]
title = [s for s in spans if abs(s[5] - 33.0) < 0.01][0]
sub = [s for s in spans if 'Student Manual' in s[7]][0]
hook = [s for s in spans if s[7].startswith('Welcome')][0]
foots = sorted([s for s in spans if s[1] > 700], key=lambda s: s[1])
ok = []
ok.append(('imprint is PRIME SCHOOL PRESS', imprint[7] == 'P R I M E  S C H O O L  P R E S S'))
ok.append(('imprint top %.1f == %.1f' % (imprint[1], REF['imprint_top']), abs(imprint[1] - REF['imprint_top']) < 0.6))
ok.append(('title top %.1f == %.1f' % (title[1], REF['title_top']), abs(title[1] - REF['title_top']) < 0.6))
ok.append(('subtitle "%s" top %.1f' % (sub[7], sub[1]), sub[7] == 'Year 6 · Prime School Press · Student Manual' and abs(sub[1] - REF['subtitle_top']) < 0.6))
ok.append(('hook top %.1f == 200.1' % hook[1], abs(hook[1] - REF['hook_top']) < 0.6))
card = [r for f, r in draws if tuple(round(c, 3) for c in f) == (0.949, 0.922, 0.863)]
ok.append(('card %s == (71, 364.3, 470, 512.3)' % (card,), card == [(71.0, 364.3, 470.0, 512.3)]))
stripe = [r for f, r in draws if tuple(round(c, 2) for c in f) == (0.51, 0.37, 0.76)]
ok.append(('stripe + accent bar in #835FC1 at (0,0,34,792)/(85,166,107,169): %s' % (stripe,),
           stripe == [(0.0, 0.0, 34.0, 792.0), (85.0, 166.0, 107.0, 169.0)]))
ok.append(('footer tops %s == %s' % (tuple(s[1] for s in foots), REF['footer_tops']),
           tuple(s[1] for s in foots) == REF['footer_tops']))
ok.append(('footer line 1 is "Prime School Press · Art & Design"', foots[0][7] == 'Prime School Press · Art & Design'))
ok.append(('no folio badge / no "Cambridge"', 'Cambridge' not in p.get_text()))
ok.append(('no PRIME BOOKS residue', 'P R I M E  B O O K S' not in p.get_text()))

# --- art: no baked white knockout anywhere in the header/blurb band ---
pix = p.get_pixmap(dpi=150)
a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
sc = 150 / 72
band = a[int(120 * sc):int(280 * sc), int(40 * sc):int(560 * sc)]
white = (band > 248).all(axis=2)
# count long pure-white runs (the knockout bars were 85-366pt wide)
rows = white.sum(axis=1)
ok.append(('longest white run in the header/blurb band: %d px (bars were ~%d px)'
           % (rows.max(), int(85 * sc)), rows.max() < 20))
print()
for name, good in ok:
    print(('PASS  ' if good else 'FAIL  ') + name)
assert all(g for _, g in ok), 'standard check failed'

# --- before / after renders for the card ---
dmg = pymupdf.open('tools/out/y06ad/book_DAMAGED_backup.pdf')
for tag, page in (('before', dmg[-1]), ('after', d[-1])):
    px = page.get_pixmap(dpi=110)
    Image.frombytes('RGB', (px.width, px.height), px.samples).save(
        '/root/prime-books/tools/out/y06ad/back_%s.png' % tag)
    print('rendered back_%s.png' % tag)
