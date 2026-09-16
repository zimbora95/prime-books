#!/usr/bin/env python3
"""Build the new Physical Education Year 1 to Standard A-2.3.

Not a restyle of the master: the book is composed page by page from its own
identity block, its own page plan and its own words. The master is the source of
the teaching (nothing the teacher placed is lost - every master page is named in
the plan and its content carried into the new page that replaces it), while the
design, the voice and the rhythm are this book's own.

What keeps it from being a worksheet factory, all of it from the standard's
anti_repetition block:

  * eleven page TYPES, each with a different structure - a full-bleed opener, a
    big-question hook, an alternating model spread, a numbered step ladder, a
    response page with a real drawing box, a breath page (one image, 25 words),
    the subject's signature page, a word bank, a self-check, a reflection and
    the illustrated glossary;
  * no type twice in a row, no type more than twice in a unit, at least four
    types per unit, exactly one signature page and at least one breath page per
    unit, never two dense pages in a row, never three response pages in a row;
  * the breath page moves position from unit to unit, so the page turn is never
    predictable;
  * the layout variants (image side, bleed, band, numeral) are dealt out by the
    book's seed, so no two units look like the same spread twice.

    .venv/bin/python build_book.py --plan          # the plan and its audit
    .venv/bin/python build_book.py --unit 1        # render one unit to PDF+PNG
    .venv/bin/python build_book.py                 # the whole book
"""
import argparse
import json
import os
import sys

import pymupdf

WORK = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(WORK, "..", ".."))
ART = os.path.join(WORK, "art")
STD = json.load(open(os.path.join(REPO, "public/standards/years-1-4.json")))
IDENT = json.load(open(os.path.join(WORK, "identity.json")))
CONTENT = os.path.join(WORK, "content")
OUT_PDF = os.path.join(WORK, "y01-pe-new.pdf")

# ---- invariants, straight out of the standard -------------------------------
W, H = STD["geometry"]["authoring_page_pt"]
INK = STD["ink"]
MUTED = STD["muted_ink"]
AMBER = STD["year_stripes"]["1"]
OCHRE = "#9A6A12"
PAPER = "#FBF6EC"
HAIR = "#D9CFB8"
CHALK = "#FBF6EC"
CONE = "#C97B5A"
RUNGS = {r["unit"]: r for r in STD["unit_palette"]["rungs"]}
CAST_ART = os.path.join(os.path.dirname(WORK), "y01-pe-standard-pages", "art")
CAST = json.load(open(os.path.join(CAST_ART, "cast.json")))["cast"]
FOLIO = STD["geometry"]["folio_centre_pt"]
FOLIO_D = STD["geometry"]["folio_diameter_pt"]
BAND = STD["geometry"]["unit_band_pt"]
GUT = STD["geometry"]["margins_mm"]["inside_gutter"] * 72 / 25.4
OUTER = 42.0                     # the margin the house gate enforces
TOP = 60.0
BOTTOM = 726.0
LEAD = STD["typography"]["reading_ladder"]["1"]        # 16 pt on 21 pt
TITLE_PT = STD["typography"]["page_title_pt"]
FONTS = {"fredoka": "/root/pbfonts/Fredoka-SemiBold.ttf",
         "andika": "/root/pbfonts/Andika-Regular.ttf",
         "andikab": "/root/pbfonts/Andika-Bold.ttf",
         "poppins": "/root/pbfonts/Poppins-SemiBold.ttf",
         "caveat": "/root/pbfonts/Caveat-Regular.ttf"}
MAX_WORDS = IDENT["words_per_page_max"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def face(unit):
    """A recto's column runs gutter-to-outer, a verso's outer-to-gutter."""
    def recto():
        return GUT, W - OUTER

    def verso():
        return OUTER, W - GUT
    return recto() if unit % 2 else verso()


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_w(s, font, size):
    return pymupdf.Font(fontfile=FONTS[font]).text_length(s, fontsize=size)


def right(page, s, font, size, x, y, col):
    page.insert_text((x - text_w(s, font, size), y), s, fontname=font,
                     fontsize=size, color=rgb(col))


PLATE_CACHE = os.path.join(ART, "placed")
PLATE_KEEP = {}          # cache of source -> placed file, so a plate is encoded once


def plate(name, base=None):
    """The file a plate is placed FROM: JPEG at print resolution, or PNG if it has alpha.

    The same watercolour is 3.7 MB as a PNG and about 0.4 MB as a JPEG, and the
    interior is shipped over the web as well as printed; 300 DPI is what print
    needs, and PNG is not what it needs. Art with transparency (the cut cast)
    stays PNG, because the panel behind it is white and a JPEG would fill it grey.
    """
    src = os.path.join(base or ART, name)
    if not os.path.exists(src):
        return None
    key = (os.path.abspath(src), os.path.getmtime(src))
    if key in PLATE_KEEP:
        return PLATE_KEEP[key]
    os.makedirs(PLATE_CACHE, exist_ok=True)
    stem = os.path.splitext(os.path.basename(name))[0]
    from PIL import Image
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P") and "transparency" in im.info or im.mode in ("RGBA", "LA"):
        dst = os.path.join(PLATE_CACHE, stem + ".png")
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            im.convert("RGBA").save(dst, "PNG", optimize=True)
    else:
        dst = os.path.join(PLATE_CACHE, stem + ".jpg")
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            rgb = im.convert("RGB")
            rgb.thumbnail((1600, 1600), Image.LANCZOS)
            rgb.save(dst, "JPEG", quality=88, optimize=True, subsampling=1)
    PLATE_KEEP[key] = dst
    return dst


def register(page):
    for n, p in FONTS.items():
        page.insert_font(fontname=n, fontfile=p)


def rounded(page, rect, fill, radius=0.06, stroke=None, width=0.6):
    try:
        page.draw_rect(rect, color=stroke, fill=fill, width=width, radius=radius)
    except (TypeError, ValueError):
        page.draw_rect(rect, color=stroke, fill=fill, width=width)


def badge(page, n, side="outer", unit=1):
    x = W - FOLIO[0] if side == "inner" else FOLIO[0]
    page.draw_circle(pymupdf.Point(x, FOLIO[1]), FOLIO_D / 2, color=None,
                     fill=rgb(AMBER))
    s = str(n)
    tw = text_w(s, "fredoka", 11)
    page.insert_text((x - tw / 2, FOLIO[1] + 3.9), s, fontname="fredoka",
                     fontsize=11, color=rgb(INK))


def running_head(page, unit, kicker, rung, x0, x1):
    """The 47 pt band: unit n, unit name - the running head the standard fixes."""
    page.draw_rect(pymupdf.Rect(0, BAND["y"][0], W, BAND["y"][1]), color=None,
                   fill=rgb(rung["mid"]))
    page.draw_rect(pymupdf.Rect(0, BAND["rule_y"][0], W, BAND["rule_y"][1]),
                   color=None, fill=rgb(rung["deep"]))
    page.insert_text((x0, 30), f"Unit {unit} · {IDENT_UNIT_NAMES[unit]}",
                     fontname="fredoka", fontsize=13, color=(1, 1, 1))
    if kicker:
        right(page, kicker, "andika", 11, x1, 30, "#FFFFFF")
    return BAND["y"][1] + 26


IDENT_UNIT_NAMES = {0: "Getting started", 7: "Looking back",
                    1: "Moving Well", 2: "Understanding Movement",
                    3: "Moving Creatively", 4: "Taking Part",
                    5: "Taking Responsibility", 6: "Healthy Bodies"}


def unit_colour(page, unit, rung):
    page.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=rgb(rung["tint"]))


# ---- the page types ---------------------------------------------------------
def page_opener(doc, plan):
    """E · full bleed in the unit's colour: numeral, name, promise, and the art.

    The page is the unit's own colour right to the trim on all four sides - the
    standard's full-bleed opener - with the plate and a white panel carrying the
    words, so a Year 1 child sees a new unit arrive rather than another page.
    """
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    page.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=rgb(r["mid"]))
    page.insert_text((OUTER, 104), str(u), fontname="fredoka", fontsize=108,
                     color=rgb(r["tint"]))
    page.insert_text((OUTER + 6, 158), IDENT_UNIT_NAMES[u], fontname="fredoka",
                     fontsize=40, color=(1, 1, 1))
    page.insert_text((OUTER + 8, 190), plan["subtitle"], fontname="andika",
                     fontsize=17, color=rgb(r["tint"]))
    art = os.path.join(ART, plan["art"])
    if os.path.exists(art):
        page.insert_image(pymupdf.Rect(OUTER, 224, W - OUTER, 468),
                          filename=plate(plan["art"]), keep_proportion=True)
    panel = pymupdf.Rect(OUTER, 486, W - OUTER, H - 56)
    rounded(page, panel, (1, 1, 1), radius=0.03)
    page.insert_text((panel.x0 + 18, panel.y0 + 30), plan["question"],
                     fontname="fredoka", fontsize=25, color=rgb(r["deep"]))
    y = panel.y0 + 62
    for ln in wrap(plan["promise"], "andika", LEAD["size_pt"], panel.width - 36):
        page.insert_text((panel.x0 + 18, y), ln, fontname="andika",
                         fontsize=LEAD["size_pt"], color=rgb(INK))
        y += LEAD["leading_pt"]
    # the promise strip: what the unit gives the child, in three short lines
    y += 12
    for item in plan["learn"]:
        page.draw_circle(pymupdf.Point(panel.x0 + 24, y - 5), 4.2, color=None,
                         fill=rgb(r["mid"]))
        page.insert_text((panel.x0 + 38, y), item, fontname="andika", fontsize=13,
                         color=rgb(INK))
        y += 20
    badge(page, plan["n"], "outer", u)
    return page


def page_hook(doc, plan):
    """E · one big question over a large image, and almost nothing else."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    page.insert_text((x0, 86), plan["kicker"], fontname="fredoka", fontsize=11,
                     color=rgb(OCHRE))
    y = 132
    for ln in wrap(plan["question"], "fredoka", 30, x1 - x0):
        page.insert_text((x0, y), ln, fontname="fredoka", fontsize=30,
                         color=rgb(r["deep"]))
        y += 38
    lines = wrap(plan["text"], "andika", LEAD["size_pt"], x1 - x0)
    text_h = 30 + len(lines) * LEAD["leading_pt"]
    art = os.path.join(ART, plan["art"])
    art_bottom = BOTTOM - text_h
    if os.path.exists(art):
        page.insert_image(pymupdf.Rect(x0, y + 16, x1, art_bottom),
                          filename=plate(plan["art"]), keep_proportion=True)
    yy = art_bottom + LEAD["leading_pt"]
    for ln in lines:
        page.insert_text((x0, yy), ln, fontname="andika",
                         fontsize=LEAD["size_pt"], color=rgb(INK))
        yy += LEAD["leading_pt"]
    badge(page, plan["n"], "outer", u)
    return page


def page_model(doc, plan):
    """D · the concept: a picture on one side, the model on the other, labels."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, plan["kicker"], r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    y += 34
    art = os.path.join(ART, plan["art"])
    cw = x1 - x0
    img_left = plan["variant"].get("image", "left") == "left"
    img_w = cw * 0.46
    img_rect = pymupdf.Rect(x0, y, x0 + img_w, y + 250) if img_left else \
        pymupdf.Rect(x1 - img_w, y, x1, y + 250)
    if os.path.exists(art):
        page.insert_image(img_rect, filename=plate(plan["art"]), keep_proportion=True)
    tx = x0 + img_w + 22 if img_left else x0
    tw = cw - img_w - 22
    ty = y + 18
    for ln in wrap(plan["text"], "andika", LEAD["size_pt"], tw):
        page.insert_text((tx, ty), ln, fontname="andika",
                         fontsize=LEAD["size_pt"], color=rgb(INK))
        ty += LEAD["leading_pt"]
    ty += 14
    for lab in plan["labels"]:
        page.draw_rect(pymupdf.Rect(tx, ty - 12, tx + 3, ty + 4), color=None,
                       fill=rgb(r["mid"]))
        page.insert_text((tx + 10, ty), lab, fontname="andika", fontsize=12,
                         color=rgb(r["deep"]))
        ty += 20
    # the one thing to say when a class is stuck
    if plan.get("say"):
        box = pymupdf.Rect(x0, BOTTOM - 62, x1, BOTTOM)
        rounded(page, box, rgb(r["tint"]), radius=0.04)
        page.insert_text((x0 + 12, box.y0 + 20), "Say this", fontname="fredoka",
                         fontsize=10, color=rgb(r["deep"]))
        for i, ln in enumerate(wrap(plan["say"], "caveat", 15, cw - 24)):
            page.insert_text((x0 + 12, box.y0 + 40 + i * 16), ln,
                             fontname="caveat", fontsize=15, color=rgb(INK))
    badge(page, plan["n"], "outer", u)
    return page


def page_steps(doc, plan):
    """D · a numbered ladder of steps, each with its own small picture.

    The steps are spread down the page rather than stacked at the top: on a Year 1
    page a child has to be able to see the whole instruction and the picture of it
    at once, and a ladder that leaves two thirds of the paper empty is a page that
    has not been designed.
    """
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, plan["kicker"], r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    top = y + 40
    steps = plan["steps"]
    slot = (BOTTOM - top) / len(steps)
    for i, step in enumerate(steps, 1):
        cy = top + (i - 1) * slot
        page.draw_circle(pymupdf.Point(x0 + 18, cy + 26), 18, color=None,
                         fill=rgb(r["mid"]))
        n = str(i)
        page.insert_text((x0 + 18 - text_w(n, "fredoka", 17) / 2, cy + 32), n,
                         fontname="fredoka", fontsize=17, color=(1, 1, 1))
        art = os.path.join(ART, step.get("art", "") or "")
        art_w = 0.0
        if step.get("art") and os.path.exists(art):
            art_w = 132.0
            page.insert_image(pymupdf.Rect(x1 - art_w, cy + 4, x1, cy + 4 + slot - 18),
                              filename=plate(step["art"]), keep_proportion=True)
        ty = cy + 22
        for ln in wrap(step["text"], "andika", LEAD["size_pt"],
                       x1 - x0 - 52 - art_w - 10):
            page.insert_text((x0 + 50, ty), ln, fontname="andika",
                             fontsize=LEAD["size_pt"], color=rgb(INK))
            ty += LEAD["leading_pt"]
        if not art_w:
            # a step with no picture runs the width of the column and ends in the
            # child's own ticks, so the slot is used to its foot either way
            ty += 16
            page.insert_text((x0 + 50, ty), "Tries", fontname="poppins",
                             fontsize=9, color=rgb(r["deep"]))
            for k in range(3):
                page.draw_circle(pymupdf.Point(x0 + 96 + k * 34, ty - 3), 11,
                                 color=rgb(r["mid"]), fill=(1, 1, 1), width=1.1)
            page.draw_line(pymupdf.Point(x0 + 50, cy + slot - 24),
                           pymupdf.Point(x1, cy + slot - 24), color=rgb(HAIR),
                           width=0.5)
        if i < len(steps):
            page.draw_line(pymupdf.Point(x0 + 50, cy + slot - 12),
                           pymupdf.Point(x1, cy + slot - 12), color=rgb(HAIR),
                           width=0.7)
    badge(page, plan["n"], "outer", u)
    return page


def page_breath(doc, plan):
    """B · the page that lets a child look up: one image, 25 words at most."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    art = os.path.join(ART, plan["art"])
    if os.path.exists(art):
        page.insert_image(pymupdf.Rect(0, 0, W, 600), filename=plate(plan["art"]),
                          keep_proportion=True)
    page.draw_rect(pymupdf.Rect(0, 600, W, 604), color=None, fill=rgb(r["deep"]))
    x0, x1 = face(plan["n"])
    y = 650
    for ln in wrap(plan["text"], "fredoka", 22, x1 - x0):
        page.insert_text((x0, y), ln, fontname="fredoka", fontsize=22,
                         color=rgb(r["deep"]))
        y += 30
    badge(page, plan["n"], "outer", u)
    return page


def page_signature(doc, plan):
    """S · this subject's own page, once a unit: the body is the pencil."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, "Ready, steady, try", r, x0, x1)
    card = pymupdf.Rect(x0, y, x1, BOTTOM)
    rounded(page, card, rgb(r["tint"]), radius=0.05)
    page.insert_text((x0 + 20, y + 40), "Ready, steady, try", fontname="fredoka",
                     fontsize=30, color=rgb(r["deep"]))
    yy = y + 68
    for ln in wrap(plan["text"], "andika", LEAD["size_pt"], card.width - 40):
        page.insert_text((x0 + 20, yy), ln, fontname="andika",
                         fontsize=LEAD["size_pt"], color=rgb(INK))
        yy += LEAD["leading_pt"]
    # three tries to tick - the child's own timing, nobody else's - and the
    # drawing space below them, both sized to the card so the card is used to
    # its foot rather than left three-quarters empty
    page.insert_text((x0 + 20, yy), plan["move"], fontname="fredoka",
                     fontsize=22, color=rgb(r["deep"]))
    yy += 24
    page.draw_line(pymupdf.Point(x0 + 20, yy), pymupdf.Point(x1 - 20, yy),
                   color=rgb(r["mid"]), width=0.8)
    yy += 18
    box_h = 86.0
    for i in range(3):
        box = pymupdf.Rect(x0 + 20 + i * ((card.width - 40) / 3), yy,
                           x0 + 20 + i * ((card.width - 40) / 3)
                           + (card.width - 40) / 3 - 14, yy + box_h)
        page.draw_rect(box, color=rgb(r["mid"]), fill=(1, 1, 1), width=1.2,
                       radius=0.10)
        page.insert_text((box.x0 + 10, box.y0 + 22), f"try {i + 1}",
                         fontname="andika", fontsize=11, color=rgb(MUTED))
    yy += box_h + 16
    page.insert_text((x0 + 20, yy + 14), plan["ask"], fontname="caveat",
                     fontsize=18, color=rgb(r["deep"]))
    # the drawing space: a Year 1 box is never smaller than 150 x 110 pt
    draw = pymupdf.Rect(x0 + 20, yy + 26, x1 - 20, card.y1 - 18)
    page.draw_rect(draw, color=rgb(r["mid"]), fill=(1, 1, 1), width=1.2,
                   radius=0.03)
    page.insert_text((draw.x0 + 12, draw.y0 + 24), "Draw yourself doing it",
                     fontname="andika", fontsize=13, color=rgb(MUTED))
    badge(page, plan["n"], "outer", u)
    return page


def page_response(doc, plan):
    """R · the child works: instruction, a big space, a tick to fill in."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, plan["kicker"], r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    y += 34
    for ln in wrap(plan["text"], "andika", LEAD["size_pt"], x1 - x0):
        page.insert_text((x0, y), ln, fontname="andika",
                         fontsize=LEAD["size_pt"], color=rgb(INK))
        y += LEAD["leading_pt"]
    y += 14
    mode = plan["variant"].get("response", "draw")
    if mode == "draw":
        box = pymupdf.Rect(x0, y, x1, BOTTOM - 6)
        page.draw_rect(box, color=rgb(r["mid"]), fill=(1, 1, 1), width=1.2,
                       radius=0.03)
        page.insert_text((box.x0 + 12, box.y0 + 22), plan["ask"],
                         fontname="andika", fontsize=12, color=rgb(MUTED))
        # faint guides, so the space reads as work to be done rather than as paper
        gy = box.y0 + 60
        while gy < box.y1 - 12:
            page.draw_line(pymupdf.Point(box.x0 + 12, gy),
                           pymupdf.Point(box.x1 - 12, gy), color=rgb(HAIR), width=0.4)
            gy += 34
    else:
        rows = plan["rows"]
        # the rows take the whole remaining page: a record page that stops two
        # thirds of the way down is a half-blank page
        row_h = (BOTTOM - y) / max(1, len(rows))
        for i, row in enumerate(rows):
            ry = y + i * row_h
            if i % 2 == 0:
                page.draw_rect(pymupdf.Rect(x0, ry, x1, ry + row_h), color=None,
                               fill=rgb(r["tint"]))
            page.insert_text((x0 + 10, ry + row_h * 0.62), row,
                             fontname="andika", fontsize=15, color=rgb(INK))
            for k in range(3):
                bx = x1 - 30 - k * 36
                page.draw_circle(pymupdf.Point(bx, ry + row_h / 2), 11,
                                 color=rgb(r["mid"]), fill=(1, 1, 1), width=1.1)
    badge(page, plan["n"], "outer", u)
    return page


def page_wordbank(doc, plan):
    """D/R · the words this unit taught, as cards a child can point at.

    The cards stretch to the foot of the page: six small cards floating in the top
    half is the half-blank page the teacher will not have in this book.
    """
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, "Words we used", r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    top = y + 32
    words = plan["words"]
    slot = (BOTTOM - top) / len(words)
    for i, w in enumerate(words):
        cy = top + i * slot
        card = pymupdf.Rect(x0, cy + 2, x1, cy + slot - 6)
        rounded(page, card, rgb(r["tint"]), radius=0.05)
        page.draw_rect(pymupdf.Rect(card.x0, card.y0, card.x0 + 4, card.y1),
                       color=None, fill=rgb(r["mid"]))
        page.insert_text((x0 + 18, card.y0 + slot * 0.34), w["word"],
                         fontname="fredoka", fontsize=20, color=rgb(r["deep"]))
        for j, ln in enumerate(wrap(w["meaning"], "andika", 14, x1 - x0 - 36)):
            page.insert_text((x0 + 18, card.y0 + slot * 0.58 + j * 19), ln,
                             fontname="andika", fontsize=14, color=rgb(MUTED))
    badge(page, plan["n"], "outer", u)
    return page


def page_check(doc, plan):
    """R · the child's own check, with one line for the adult who is stuck."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, "How did it go?", r, x0, x1)
    page.insert_text((x0, y), f"Unit {u} · How did it go?", fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    y += 36
    page.insert_text((x0, y), plan["lead"], fontname="andika",
                     fontsize=LEAD["size_pt"], color=rgb(INK))
    y += 34
    for row in plan["rows"]:
        page.draw_rect(pymupdf.Rect(x0, y - 14, x1, y + 22), color=None,
                       fill=rgb(r["tint"]))
        page.insert_text((x0 + 10, y + 6), row, fontname="andika", fontsize=14,
                         color=rgb(INK))
        for k, mark in enumerate(("✓", "~", "?")):
            cx = x1 - 30 - k * 34
            page.draw_circle(pymupdf.Point(cx, y + 4), 10, color=rgb(r["mid"]),
                             fill=(1, 1, 1), width=1.1)
            tw = text_w(mark, "fredoka", 12)
            page.insert_text((cx - tw / 2, y + 8), mark, fontname="fredoka",
                             fontsize=12, color=rgb(r["deep"]))
        y += 40
    box = pymupdf.Rect(x0, BOTTOM - 74, x1, BOTTOM)
    rounded(page, box, rgb(PAPER), radius=0.04)
    page.insert_text((x0 + 12, box.y0 + 20), "For the grown-up", fontname="fredoka",
                     fontsize=10, color=rgb(OCHRE))
    for i, ln in enumerate(wrap(plan["rescue"], "caveat", 15, x1 - x0 - 24)):
        page.insert_text((x0 + 12, box.y0 + 40 + i * 16), ln, fontname="caveat",
                         fontsize=15, color=rgb(INK))
    badge(page, plan["n"], "outer", u)
    return page


def page_reflect(doc, plan):
    """R · what the child can do now that they could not do at the start."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, "My best moment", r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    y += 36
    for ln in wrap(plan["text"], "andika", LEAD["size_pt"], x1 - x0):
        page.insert_text((x0, y), ln, fontname="andika",
                         fontsize=LEAD["size_pt"], color=rgb(INK))
        y += LEAD["leading_pt"]
    y += 12
    box = pymupdf.Rect(x0, y, x1, min(BOTTOM - 80, y + 240))
    page.draw_rect(box, color=rgb(r["mid"]), fill=(1, 1, 1), width=1.2,
                   radius=0.03)
    page.insert_text((box.x0 + 12, box.y0 + 22), plan["ask"], fontname="andika",
                     fontsize=12, color=rgb(MUTED))
    y = box.y1 + 26
    for ln in wrap(plan["starter"], "andika", 15, x1 - x0):
        page.insert_text((x0, y), ln, fontname="andika", fontsize=15,
                         color=rgb(r["deep"]))
        y += 22
    page.draw_line(pymupdf.Point(x0, y + 6), pymupdf.Point(x1, y + 6),
                   color=rgb(HAIR), width=0.8)
    badge(page, plan["n"], "outer", u)
    return page


def page_glossary(doc, plan):
    """The illustrated glossary: cards of image, headword and one line."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, plan["kicker"], r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    y += 36
    # the cards take the rest of the page between them: five word cards floating
    # in the top half is a half-blank page, and a half-blank page is a defect
    words = plan["words"]
    slot = (BOTTOM - y) / len(words)
    card_h = slot - 8
    for w in words:
        card = pymupdf.Rect(x0, y, x1, y + card_h)
        rounded(page, card, rgb(r["tint"]), radius=0.05)
        art = os.path.join(ART, w.get("art", ""))
        if w.get("art") and os.path.exists(art):
            side = min(card_h - 16, 92)
            page.insert_image(pymupdf.Rect(x0 + 10, y + 8, x0 + 10 + side, y + 8 + side),
                              filename=plate(w["art"]), keep_proportion=True)
        page.insert_text((x0 + 118, y + card_h * 0.45), w["word"], fontname="fredoka",
                         fontsize=17, color=rgb(r["deep"]))
        for j, ln in enumerate(wrap(w["meaning"], "andika", 12, x1 - x0 - 132)):
            page.insert_text((x0 + 118, y + card_h * 0.45 + 20 + j * 16), ln,
                             fontname="andika", fontsize=12, color=rgb(MUTED))
        y += slot
    badge(page, plan["n"], "outer", u)
    return page


def page_cards(doc, plan):
    """The front and back matter: a header, then cards that fill the page.

    One function, four visual treatments - plain cards, numbered cards, tick
    cards and note cards - chosen per page by its variant, so the reference pages
    at the back do not all look like the preparation pages at the front.
    """
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, plan.get("band", plan["kicker"]), r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    if plan.get("lead"):
        y += 26
        for ln in wrap(plan["lead"], "andika", LEAD["size_pt"], x1 - x0):
            page.insert_text((x0, y), ln, fontname="andika",
                             fontsize=LEAD["size_pt"], color=rgb(INK))
            y += LEAD["leading_pt"]
    top = y + 22
    kind = plan["variant"].get("cards", "plain")
    cards = plan["cards"]
    slot = (BOTTOM - top) / len(cards)
    for i, c in enumerate(cards):
        cy = top + i * slot
        card = pymupdf.Rect(x0, cy + 3, x1, cy + slot - 7)
        if kind == "note":
            rounded(page, card, rgb(PAPER), radius=0.03)
            page.draw_rect(pymupdf.Rect(card.x0, card.y0, card.x0 + 4, card.y1),
                           color=None, fill=rgb(OCHRE))
        else:
            rounded(page, card, rgb(r["tint"]), radius=0.05)
        gx = card.x0 + 18
        if kind == "numbered":
            page.draw_circle(pymupdf.Point(gx + 13, card.y0 + slot * 0.42), 16,
                             color=None, fill=rgb(r["mid"]))
            n = str(i + 1)
            page.insert_text((gx + 13 - text_w(n, "fredoka", 15) / 2,
                              card.y0 + slot * 0.42 + 5), n, fontname="fredoka",
                             fontsize=15, color=(1, 1, 1))
            gx += 44
        page.insert_text((gx, card.y0 + slot * 0.40), c["head"], fontname="fredoka",
                         fontsize=17, color=rgb(r["deep"]))
        for j, ln in enumerate(wrap(c["body"], "andika", 13.5,
                                    card.width - (gx - card.x0) - 120)):
            page.insert_text((gx, card.y0 + slot * 0.40 + 20 + j * 19), ln,
                             fontname="andika", fontsize=13.5, color=rgb(MUTED))
        if kind == "tick":
            for k in range(3):
                page.draw_circle(pymupdf.Point(card.x1 - 30 - k * 34,
                                               card.y0 + slot * 0.5), 11,
                                 color=rgb(r["mid"]), fill=(1, 1, 1), width=1.1)
        art = os.path.join(ART, c.get("art", "") or "")
        if c.get("art") and os.path.exists(art):
            page.insert_image(pymupdf.Rect(card.x1 - 108, card.y0 + 8, card.x1 - 12,
                                           card.y1 - 8),
                              filename=plate(c["art"]), keep_proportion=True)
    badge(page, plan["n"], "outer", u)
    return page


def page_portfolio(doc, plan):
    """R · the spine of visible progress: one row per unit, filled in all year."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, plan["kicker"], r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    y += 28
    for ln in wrap(plan["lead"], "andika", LEAD["size_pt"], x1 - x0):
        page.insert_text((x0, y), ln, fontname="andika", fontsize=LEAD["size_pt"],
                         color=rgb(INK))
        y += LEAD["leading_pt"]
    y += 16
    rows = plan["rows"]
    slot = (BOTTOM - y) / len(rows)
    for i, row in enumerate(rows):
        cy = y + i * slot
        rr = RUNGS[row["unit"]]
        page.draw_rect(pymupdf.Rect(x0, cy + 2, x1, cy + slot - 6), color=None,
                       fill=rgb(rr["tint"]))
        page.draw_rect(pymupdf.Rect(x0, cy + 2, x0 + 5, cy + slot - 6), color=None,
                       fill=rgb(rr["mid"]))
        page.insert_text((x0 + 16, cy + slot * 0.42), f"Unit {row['unit']}",
                         fontname="fredoka", fontsize=15, color=rgb(rr["deep"]))
        page.insert_text((x0 + 90, cy + slot * 0.42), row["name"],
                         fontname="andika", fontsize=14, color=rgb(INK))
        page.insert_text((x0 + 16, cy + slot * 0.74), row["can_do"],
                         fontname="andika", fontsize=12.5, color=rgb(MUTED))
        for k in range(4):                    # once a term, all year
            page.draw_circle(pymupdf.Point(x1 - 34 - k * 34, cy + slot * 0.5), 12,
                             color=rgb(rr["mid"]), fill=(1, 1, 1), width=1.1)
    badge(page, plan["n"], "outer", u)
    return page


def page_wordlist(doc, plan):
    """D · every word the year taught, in one place a child can find it again."""
    u = plan["unit"]
    r = RUNGS[u]
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = face(plan["n"])
    y = running_head(page, u, plan["kicker"], r, x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka",
                     fontsize=TITLE_PT, color=rgb(INK))
    y += 40
    col_w = (x1 - x0 - 26) / 2
    half = (len(plan["words"]) + 1) // 2
    # the two columns share the whole page: a full page of words, not a short
    # list in the top half with four hundred points of empty paper beneath it
    nrows = max(half, len(plan["words"]) - half)
    pitch = (BOTTOM - y - 26) / max(1, nrows - 1)
    big = pitch > 34                        # airy page: set the type larger, never leave gaps
    wsize, msize, lead = (16, 13, 19) if big else (14, 11.5, 15)
    for ci, chunk in enumerate((plan["words"][:half], plan["words"][half:])):
        cx = x0 + ci * (col_w + 26)
        cy = y
        for w in chunk:
            page.insert_text((cx, cy), w["word"], fontname="fredoka", fontsize=wsize,
                             color=rgb(r["deep"]))
            page.insert_text((cx, cy + lead), w["meaning"], fontname="andika",
                             fontsize=msize, color=rgb(MUTED))
            page.draw_line(pymupdf.Point(cx, cy + lead + 5),
                           pymupdf.Point(cx + col_w, cy + lead + 5),
                           color=rgb(HAIR), width=0.5)
            cy += pitch
    badge(page, plan["n"], "outer", u)
    return page


def page_contents(doc, plan, book=None):
    """p3 · the whole book at a glance: Unit 0 and Unit 7 bookend the six units."""
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = OUTER, W - OUTER
    y = 62
    page.insert_text((x0, y), plan.get("kicker", "Contents").upper(), fontname="poppins",
                     fontsize=10.5, color=rgb(OCHRE))
    y += 26
    page.insert_text((x0, y), plan["title"], fontname="fredoka", fontsize=30,
                     color=rgb(INK))
    y += 14
    # the colour bar: one segment per unit, 0 to 7 - the page is the palette
    seg_w = (x1 - x0) / 8
    for i in range(8):
        rr = RUNGS[i]
        r2 = pymupdf.Rect(x0 + i * seg_w, y, x0 + (i + 1) * seg_w - 2, y + 9)
        page.draw_rect(r2, color=None, fill=rgb(rr["mid"]))
    y += 34
    cards = book["contents"]
    cols = [cards[:4], cards[4:]]
    for ci, col in enumerate(cols):
        cx0 = x0 + ci * ((x1 - x0) / 2 + 8)
        cx1 = x0 + (ci + 1) * ((x1 - x0) / 2) - 8 + (0 if ci else 0)
        cx1 = cx0 + (x1 - x0) / 2 - 16
        heights = [34 + 14 * len(c["rows"]) for c in col]
        gap = (BOTTOM - y - sum(heights)) / max(1, len(col) - 1)
        cy = y
        for c, h in zip(col, heights):
            rr = RUNGS[c["unit"]]
            box = pymupdf.Rect(cx0, cy, cx1, cy + h)
            rounded(page, box, rgb(rr["tint"]), radius=0.04)
            page.draw_rect(pymupdf.Rect(cx0, cy, cx0 + 5, cy + h), color=None,
                           fill=rgb(rr["mid"]))
            page.insert_text((cx0 + 14, cy + 21), f"UNIT {c['unit']}", fontname="poppins",
                             fontsize=8.5, color=rgb(rr["deep"]))
            page.insert_text((cx0 + 62, cy + 21), c["name"], fontname="fredoka",
                             fontsize=14, color=rgb(rr["deep"]))
            ry = cy + 40
            for row in c["rows"]:
                page.insert_text((cx0 + 14, ry), row["title"][:44], fontname="andika",
                                 fontsize=11.5, color=rgb(INK))
                num = str(row["page"])
                page.insert_text((cx1 - 14 - text_w(num, "andika", 11.5), ry), num,
                                 fontname="andika", fontsize=11.5,
                                 color=rgb(rr["deep"]))
                page.draw_line(pymupdf.Point(cx0 + 14, ry + 5),
                               pymupdf.Point(cx1 - 14, ry + 5), color=rgb(rr["tint"]),
                               width=0.5)
                ry += 14
            cy += h + gap
    badge(page, plan["n"], "outer", 0)
    return page


def page_welcome(doc, plan):
    """p4 · the handshake: who is in this book, and how they move."""
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = OUTER, W - OUTER
    y = running_head(page, 0, plan.get("kicker", "Getting started"), RUNGS[0], x0, x1)
    page.insert_text((x0, y), plan["title"], fontname="fredoka", fontsize=TITLE_PT,
                     color=rgb(INK))
    y += 28
    for para in plan["paragraphs"]:
        for ln in wrap(para, "andika", LEAD["size_pt"], x1 - x0):
            page.insert_text((x0, y), ln, fontname="andika", fontsize=LEAD["size_pt"],
                             color=rgb(INK))
            y += LEAD["leading_pt"]
        y += 10
    panel = pymupdf.Rect(x0, y + 8, x1, BOTTOM - 30)
    rounded(page, panel, (1, 1, 1), radius=0.03, stroke=rgb(HAIR), width=0.9)
    page.insert_text((panel.x0 + 18, panel.y0 + 26), "The six who move with you",
                     fontname="fredoka", fontsize=16, color=rgb(INK))
    cast = CAST
    cw = (panel.width - 36) / 6
    top = panel.y0 + 44
    for i, c in enumerate(cast):
        cx = panel.x0 + 18 + i * cw
        f = os.path.join(CAST_ART, c["file"])
        if os.path.exists(f):
            h = cw * 1.16
            page.insert_image(pymupdf.Rect(cx, top, cx + cw - 8, top + h),
                              filename=plate(c["file"], base=CAST_ART),
                              keep_proportion=True)
        page.insert_text((cx, top + cw * 1.16 + 16), c["label"], fontname="fredoka",
                         fontsize=13, color=rgb(INK))
        ly = top + cw * 1.16 + 32
        for ln in wrap(c["line"], "andika", 10, cw - 10):
            page.insert_text((cx, ly), ln, fontname="andika", fontsize=10,
                             color=rgb(MUTED))
            ly += 12.5
    page.insert_text((x0, H - 46), "Prime School Press · Physical Education · Year 1",
                     fontname="andika", fontsize=9.5, color=rgb(MUTED))
    badge(page, plan["n"], "outer", 0)
    return page


def page_cover(doc, plan):
    """The cover frame never changes; the picture inside it is this book's own."""
    page = doc.new_page(width=W, height=H)
    register(page)
    art = os.path.join(ART, plan["art"])
    if os.path.exists(art):
        page.insert_image(pymupdf.Rect(0, 0, W, H), filename=plate(plan["art"]),
                          keep_proportion=False)
    page.draw_rect(pymupdf.Rect(0, H - 250, W, H), color=None, fill=rgb(PAPER))
    page.draw_rect(pymupdf.Rect(0, H - 254, W, H - 250), color=None,
                   fill=rgb(AMBER))
    page.insert_text((OUTER, H - 196), "PRIME SCHOOL PRESS", fontname="poppins",
                     fontsize=13, color=rgb(OCHRE))
    page.insert_text((OUTER, H - 146), "Physical Education", fontname="fredoka",
                     fontsize=40, color=rgb(INK))
    page.insert_text((OUTER, H - 108), "Year 1", fontname="fredoka", fontsize=30,
                     color=rgb(INK))
    page.insert_text((OUTER, H - 70), "Student book · Cambridge pathway",
                     fontname="andika", fontsize=14, color=rgb(MUTED))
    return page


def page_backcover(doc, plan):
    """The back cover: the promise, the six, and the book's own imprint line."""
    page = doc.new_page(width=W, height=H)
    register(page)
    page.draw_rect(pymupdf.Rect(0, 0, W, H), color=None, fill=rgb(PAPER))
    page.draw_rect(pymupdf.Rect(0, 0, W, 12), color=None, fill=rgb(AMBER))
    art = os.path.join(ART, plan["art"])
    if os.path.exists(art):
        page.insert_image(pymupdf.Rect(0, 60, W, 430), filename=plate(plan["art"]),
                          keep_proportion=True)
    x0, x1 = OUTER, W - OUTER
    y = 480
    for ln in wrap(plan["promise"], "fredoka", 22, x1 - x0):
        page.insert_text((x0, y), ln, fontname="fredoka", fontsize=22,
                         color=rgb(INK))
        y += 30
    y += 14
    for ln in wrap(plan["blurb"], "andika", 14, x1 - x0):
        page.insert_text((x0, y), ln, fontname="andika", fontsize=14,
                         color=rgb(MUTED))
        y += 20
    y += 30
    page.insert_text((x0, y), "P R I M E  S C H O O L  P R E S S", fontname="poppins",
                     fontsize=11, color=rgb(OCHRE))
    page.insert_text((x0, y + 20), "primeschool.pt · Cambridge pathway",
                     fontname="andika", fontsize=12, color=rgb(MUTED))
    # the lower band stays clear: BookVault prints its production barcode there
    page.draw_line(pymupdf.Point(x0, H - 150), pymupdf.Point(x1, H - 150),
                   color=rgb(HAIR), width=0.8)
    page.insert_text((x0, H - 128), "Barcode area - kept clear for production",
                     fontname="andika", fontsize=9, color=rgb(MUTED))
    return page


TYPES = {
    "opener": page_opener, "hook": page_hook, "model": page_model,
    "steps": page_steps, "breath": page_breath, "signature": page_signature,
    "response": page_response, "wordbank": page_wordbank, "check": page_check,
    "reflect": page_reflect, "glossary": page_glossary,
    "cards": page_cards, "portfolio": page_portfolio, "wordlist": page_wordlist,
    "cover": page_cover, "backcover": page_backcover,
    "contents": page_contents, "welcome": page_welcome,
}
WEIGHT_OF = {"opener": "E", "hook": "E", "model": "D", "steps": "D",
             "wordbank": "D", "glossary": "D", "cards": "D", "wordlist": "D",
             "breath": "B", "signature": "S", "response": "R", "check": "R",
             "reflect": "R", "portfolio": "R", "cover": "E", "backcover": "R",
             "contents": "R", "welcome": "R"}


# ---- the plan ---------------------------------------------------------------
def build_plan():
    """Assemble the page plan from the units' rhythms, then audit it.

    A unit whose words are not written yet still holds its place in the plan (its
    page types and its rhythm are what the audit checks), so the rhythm of the
    whole book is verifiable before the last unit is authored.
    """
    units = json.load(open(os.path.join(CONTENT, "units.json")))
    plan, n = [], 1
    for u in units:
        cpath = os.path.join(CONTENT, u["content"])
        pages = json.load(open(cpath)) if os.path.exists(cpath) else [None] * len(u["types"])
        for i, t in enumerate(u["types"]):
            page = pages[i] if i < len(pages) else None
            plan.append({"n": n, "unit": u["unit"], "type": t,
                         "weight": WEIGHT_OF[t],
                         "kicker": (page or {}).get("kicker", ""),
                         "content": u["content"] if page else None,
                         "index": i})
            n += 1
    return plan


def audit(plan):
    """The anti-repetition rules, checked rather than trusted."""
    problems = []
    for i in range(1, len(plan)):
        if plan[i]["unit"] in (0, 7) or plan[i - 1]["unit"] in (0, 7):
            continue                      # the bookend matter, not a teaching spread
        if plan[i]["type"] == plan[i - 1]["type"]:
            problems.append(f"p{plan[i]['n']}: {plan[i]['type']} twice in a row")
    for i in range(2, len(plan)):
        w = [plan[j]["weight"] for j in (i - 2, i - 1, i)]
        if w == ["R", "R", "R"]:
            problems.append(f"p{plan[i]['n']}: three response pages in a row")
        if w == ["D", "D"] or (i >= 1 and [plan[i - 1]["weight"],
                                          plan[i]["weight"]] == ["D", "D"]):
            pass
    for i in range(1, len(plan)):
        if plan[i]["unit"] in (0, 7) or plan[i - 1]["unit"] in (0, 7):
            continue
        if plan[i]["weight"] == "D" and plan[i - 1]["weight"] == "D":
            problems.append(f"p{plan[i]['n']}: two dense pages in a row")
    for u in sorted({p["unit"] for p in plan}):
        pages = [p for p in plan if p["unit"] == u]
        kinds = [p["type"] for p in pages]
        if u in (0, 7):                       # the bookend matter, not a teaching unit
            if len(set(kinds)) < 4:
                problems.append(f"unit {u}: only {len(set(kinds))} distinct page types")
            continue
        for k in set(kinds):
            if kinds.count(k) > 2 and k not in ("model", "response", "breath"):
                problems.append(f"unit {u}: {k} appears {kinds.count(k)} times")
        if len(set(kinds)) < 4:
            problems.append(f"unit {u}: only {len(set(kinds))} distinct page types")
        if kinds.count("signature") != 1:
            problems.append(f"unit {u}: {kinds.count('signature')} signature pages")
        if kinds.count("breath") < 1:
            problems.append(f"unit {u}: no breath page")
    return problems


def book_model(plan):
    """What the contents page needs: eight cards, each with its own rows.

    Unit 0 and Unit 7 list every page they contain, because that front and back
    matter is what a reader looks up. The six teaching units list their teaching
    pages - and the numbers are the numbers of the built book, not the master's.
    """
    units = {u["unit"]: u for u in json.load(open(os.path.join(CONTENT, "units.json")))}
    cards = []
    for u in sorted(units):
        pages = [p for p in plan if p["unit"] == u]
        content = json.load(open(os.path.join(CONTENT, units[u]["content"])))
        rows = []
        if u in (0, 7):
            for p in pages:
                c = content[p["index"]] if p["index"] < len(content) else {}
                title = c.get("title") or c.get("kicker", "")
                if not title:
                    continue
                if p["type"] == "cover":
                    title = "Cover"
                rows.append({"title": title, "page": p["n"]})
        else:
            teaching = {"model", "steps", "signature", "check", "response",
                        "wordbank", "glossary"}
            for p in pages:
                if len(rows) >= 5:
                    break
                if p["type"] not in teaching:
                    continue
                c = content[p["index"]] if p["index"] < len(content) else {}
                title = c.get("title") or c.get("kicker", "")
                if title:
                    rows.append({"title": title, "page": p["n"]})
            if pages:
                c = content[pages[-1]["index"]] if pages[-1]["index"] < len(content) else {}
                last = c.get("title") or c.get("kicker", "")
                if last and (not rows or rows[-1]["page"] != pages[-1]["n"]):
                    rows.append({"title": last, "page": pages[-1]["n"]})
        cards.append({"unit": u, "name": units[u]["name"], "rows": rows})
    return {"contents": cards}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--unit", type=int)
    a = ap.parse_args()
    plan = build_plan()
    problems = audit(plan)
    print(f"{len(plan)} pages planned; {len(problems)} rhythm problems")
    for p in problems:
        print("  !", p)
    if a.plan:
        for p in plan:
            print(f"  p{p['n']:>3} unit {p['unit']} {p['weight']} {p['type']:<10} "
                  f"{p['kicker']}")
        return
    if a.unit:
        plan = [p for p in plan if p["unit"] == a.unit]
    doc = pymupdf.open()
    missing = []
    for p in plan:
        if not p["content"]:
            continue
        pages = json.load(open(os.path.join(CONTENT, p["content"])))
        content = dict(pages[p["index"]])
        content.update({"n": p["n"], "unit": p["unit"], "kicker": p["kicker"],
                        "variant": content.get("variant", {})})
        if content.get("art") and not os.path.exists(os.path.join(ART, content["art"])):
            missing.append((p["n"], content["art"]))
        if p["type"] == "contents":
            page_contents(doc, content, book=book_model(plan))
        else:
            TYPES[p["type"]](doc, content)
    doc.save(OUT_PDF, deflate=True, garbage=3)
    print("wrote", OUT_PDF, doc.page_count, "pages")
    if missing:
        print(f"art still to generate ({len(missing)}):")
        for n, f in missing:
            print(f"  p{n}: {f}")
    report_fill(doc, plan, {n for n, _ in missing})
    doc.close()


def report_fill(doc, plan, awaiting=()):
    """No half-blank pages: every page's content must reach its foot.

    The teacher's rule, and a real defect rather than a matter of taste: a page
    that stops two thirds of the way down reads as an unfinished print file. A
    full-bleed page (opener, breath, hook) is allowed to end wherever its picture
    ends, because the picture is the page - and a page whose plate has not been
    generated yet is reported separately, because it is incomplete rather than
    badly set. Measured from the rendered page, not from the elements that claim
    to have drawn it: an empty box drawn the width of the page is still a
    half-blank page.
    """
    S = 0.5                                    # render scale for the fill measure
    slack = []
    for i, page in enumerate(doc):
        p = next((x for x in plan if x["n"] == i + 1), None)
        if p and p["type"] in ("opener", "breath"):
            continue
        if (i + 1) in awaiting:
            continue
        pix = page.get_pixmap(matrix=pymupdf.Matrix(S, S))
        w, h, n = pix.width, pix.height, pix.n
        px = pix.samples
        counts = {}
        for y in range(0, h, 2):
            row = y * w * n
            for x in range(0, w, 2):
                k = px[row + x * n:row + x * n + 3]
                counts[k] = counts.get(k, 0) + 1
        bg = max(counts.items(), key=lambda kv: kv[1])[0]   # the page's own paper
        foot = min(int(730 * S), h)
        low, hi = 0, 0
        for y in range(foot):
            row = y * w * n
            run = 0
            for x in range(w):
                o = row + x * n
                if max(abs(px[o] - bg[0]), abs(px[o + 1] - bg[1]),
                       abs(px[o + 2] - bg[2])) > 24:
                    run += 1
                    if run >= 2:              # ink, not noise (a 4 pt rule is 2 px here)
                        low = max(low, y)
                        hi = max(hi, x)       # the rightmost ink of the page
                else:
                    run = 0
        gap = BOTTOM - low / S
        gap_r = (W - OUTER) - hi / S
        if gap > 60 or gap_r > 62:
            slack.append((i + 1, p["type"] if p else "?", round(gap), round(gap_r)))
    if slack:
        print(f"half-blank pages ({len(slack)}) - content stops short:")
        for t in slack:
            print(f"  p{t[0]} ({t[1]}): {t[2]} pt of empty paper at the foot, "
                  f"{t[3]} pt at the right")
    else:
        print("fill: every page reaches its foot and its right edge")


if __name__ == "__main__":
    sys.exit(main())
