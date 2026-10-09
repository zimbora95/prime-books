#!/usr/bin/env python3
"""Final assembly: swap in the house front and back covers.

The owner asked for the front and back covers of the Prime Books master of the same
title (public/library/y04-portuguese/book.pdf, pages 1 and last). Those pages are US
Letter (612 x 792 pt); this book is 595 x 842 pt, so each cover is re-composed from
its own parts, never stretched and never cropped through type:

Front  - flat cream ground and the flush green band drawn at full height; the top
         part of the cover (logo + title block) placed at 0.972 scale; the artwork
         part placed at the same scale anchored to the bottom edge, so the art keeps
         bleeding off the bottom and right exactly as on the master. The extra
         height becomes cream above the title and between the title and the art.
Back   - the full-page sketch taken out of the master and redrawn cover-fit on the
         taller page (cropped only at the sides, where it is pale paper); every
         vector element and all type placed on top at 0.972 scale, centred; the
         green band redrawn at full height.

(Stretching an edge row into the extra height read as vertical stripes, and a
mirrored band duplicated artwork and flipped the web address, so neither is used.)

usage: finalize.py [in.pdf] [out.pdf]
"""
import sys, pathlib
import pymupdf

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parents[2] / 'public/library/y04-portuguese/book.pdf'
inp = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'unit1.pdf'
out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / 'book-final.pdf'
SPLIT_Y = 300  # front cover: above is the title block, below is the art (art starts at y 315)

def flat(page, rect, rgb):
    page.draw_rect(rect, color=None, fill=rgb, width=0)

def page_fill_and_band(sp):
    """The master's full-page ground colour and its flush left band (width, colour)."""
    ground, band = None, None
    for d in sp.get_drawings():
        r, f = d['rect'], d.get('fill')
        if f is None: continue
        if r.x0 <= 0.5 and r.y0 <= 0.5 and r.y1 >= sp.rect.y1 - 0.5:
            if r.x1 >= sp.rect.x1 - 0.5: ground = f
            elif r.width < 80: band = (r.width, f)
    return ground, band

def front(res, src, W, H):
    sp = src[0]
    s = W / sp.rect.width
    extra = H - sp.rect.height * s
    ground, (bw, bf) = page_fill_and_band(sp)
    page = res.new_page(width=W, height=H)
    flat(page, page.rect, ground)
    top_clip = pymupdf.Rect(0, 0, sp.rect.width, SPLIT_Y)
    bot_clip = pymupdf.Rect(0, SPLIT_Y, sp.rect.width, sp.rect.height)
    ytop = extra / 2
    page.show_pdf_page(pymupdf.Rect(0, ytop, W, ytop + SPLIT_Y * s), src, 0, clip=top_clip)
    page.show_pdf_page(pymupdf.Rect(0, H - bot_clip.height * s, W, H), src, 0, clip=bot_clip)
    flat(page, pymupdf.Rect(0, 0, bw * s, H), bf)

def back(res, src, W, H):
    last = src.page_count - 1
    work = pymupdf.open(); work.insert_pdf(src, from_page=last, to_page=last)
    sp = work[0]
    s = W / sp.rect.width
    infos = [i for i in sp.get_image_info(xrefs=True) if i['bbox'][2] - i['bbox'][0] > sp.rect.width * .9]
    assert len(infos) == 1, infos
    xref = infos[0]['xref']
    img = work.extract_image(xref)
    iw, ih = img['width'], img['height']
    ground, (bw, bf) = page_fill_and_band(sp)
    sp.delete_image(xref)  # the vector layer and the type stay; the sketch is redrawn below
    page = res.new_page(width=W, height=H)
    ww = H * iw / ih  # cover-fit on the taller page: scale to height, centre, crop the sides
    page.insert_image(pymupdf.Rect((W - ww) / 2, 0, (W + ww) / 2, H), stream=img['image'], keep_proportion=False)
    y = (H - sp.rect.height * s) / 2
    page.show_pdf_page(pymupdf.Rect(0, y, W, y + sp.rect.height * s), work, 0)
    flat(page, pymupdf.Rect(0, 0, bw * s, H), bf)

book = pymupdf.open(inp)
src = pymupdf.open(SRC)
W, H = book[0].rect.width, book[0].rect.height
n = book.page_count
res = pymupdf.open()
same = abs(W - src[0].rect.width) < 1 and abs(H - src[0].rect.height) < 1
if same:  # US Letter book: the house covers go in exactly as they are
    res.insert_pdf(src, from_page=0, to_page=0)
else:
    front(res, src, W, H)
res.insert_pdf(book, from_page=1, to_page=n - 2)
if same:
    res.insert_pdf(src, from_page=src.page_count - 1, to_page=src.page_count - 1)
else:
    back(res, src, W, H)
assert res.page_count == n, (res.page_count, n)
res.save(out, garbage=3, deflate=True)
print('wrote', out, res.page_count, 'pages')
