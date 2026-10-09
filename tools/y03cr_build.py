#!/usr/bin/env python3
"""Re-cut y03-computing-and-robotics onto Standard A-2.3 (Years 1-4).

Cover and back cover are rebuilt in the house frame (same art as the master,
which is the teacher's own picture for this title); the imprint is re-typeset on
the standard page as the front-matter page 2; every interior page is rebuilt
through tools/pb_engine.py from tools/y03cr_book_content.py, one colour per
unit, with the Year 3 reading ladder and the standard's band, rule and folio.

Usage
    .venv/bin/python tools/y03cr_build.py            # build + report
    .venv/bin/python tools/y03cr_build.py --commit   # ... and publish the master
"""
from __future__ import annotations

import os
import shutil
import sys

import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pb_engine as E            # noqa: E402
import std_back_lib as SB        # noqa: E402
import std_front_lib as SF       # noqa: E402
import y03cr_book_content as C   # noqa: E402

SLUG = "y03-computing-and-robotics"
MASTER = os.path.join(REPO, "public", "library", SLUG, "book.pdf")
WORK = os.path.join(REPO, "work", "y03cr")
IMG = os.path.join(WORK, "img")
OUT = os.path.join(WORK, "book_new.pdf")

TITLE = "Computing & Robotics"
YEAR = 3
STRIPE = (239, 117, 34)          # Year 3 stripe, cover_meta.json
LEVEL = "Cambridge Primary"
AGES = "Ages 7\u20138"
BAND = "Lower Primary"

E.IMG_DIR = IMG

# The Year 3 reading ladder from the locked standard: 15 pt on 20 pt leading,
# and every piece of furniture one tier below it.
Y3 = dict(lead=15.0, lead_pitch=20.0, para=15.0, para_pitch=20.0,
          panel=15.0, panel_pitch=19.0, item=14.0, item_pitch=17.4,
          tail=14.0, tail_pitch=20.0, card=12.5, card_pitch=15.8,
          card_title=12.5, table=11.5, table_pitch=13.0, cap=11.0,
          cap_pitch=14.0, qr=12.5, subhead=14.5)
E.A2.update(Y3)

# -------------------------------------------------------------- unit palette --
# The LOCKED A-2.3 palette (public/standards/years-1-4.json -> unit_palette).
# "unit colour rung n = unit n, across the whole series" is an invariant of the
# identity layer, so unit 1 is violet in this book exactly as it is in the
# reference titles (y01-art-and-design, y01-german-a1a2): deep #4A3173,
# mid #6B4BA1, tint #EFE6FA, with the band, the 1.8 pt rule, the kicker, the
# headings and the folio badge all taking the rung.
#
# tools/pb_engine.py still defaults to the retired A-2.2 six-rung table (unit 1
# #1E4E6B / #3C7CA6 / #EAF3F9), which is why this book read blue instead of
# violet. The table lives here, in this title's own build file, because the
# palette is the book's identity and the engine is shared by the other builds
# running in parallel. Report the engine drift rather than changing its global.
E.UNIT_THEMES.update({
    1: E._themed(E.PE, "4A3173", "6B4BA1", "EFE6FA", "DCD0F0"),   # violet
    2: E._themed(E.PE, "96204A", "D6336C", "FCE4EC", "F2CBD9"),   # rose
    3: E._themed(E.PE, "8C3A12", "C4561F", "FBE7D8", "F0D4C3"),   # terracotta
    4: E._themed(E.PE, "0B3C85", "1256B8", "DEEAFB", "C6D9F4"),   # blue
    5: E._themed(E.PE, "2F5233", "4E7C52", "E8F0E3", "D3E2CB"),   # sage
    6: E._themed(E.PE, "6B4A0C", "9A6A12", "FBF0D8", "EFE0BC"),   # ochre
})


# ------------------------------------------------------------------- covers --
def draw_cover(doc):
    pg = doc.new_page(width=E.W, height=E.H)
    SF.build_front(pg, YEAR, TITLE, LEVEL, os.path.join(IMG, "front_art.png"),
                   STRIPE, art_top=315.0)
    return pg


def draw_back(doc):
    """The back cover: the teacher's own back art, the house frame, Poppins text."""
    pg = doc.new_page(width=E.W, height=E.H)
    W, H = E.W, E.H
    bg = Image.open(os.path.join(IMG, "back_art.png")).convert("RGB")
    bg = bg.resize((714, int(714 * H / W)), Image.LANCZOS)
    tmp = os.path.join(WORK, "_backbg.jpg")
    bg.save(tmp, quality=88)
    pg.insert_image(pymupdf.Rect(0, 0, W, H), filename=tmp, keep_proportion=False)
    pg.draw_rect(pymupdf.Rect(0, 0, 34.0, H), color=None,
                 fill=tuple(c / 255 for c in STRIPE))
    x0 = 85.0
    pg.insert_text((x0, 78), "P R I M E  S C H O O L  P R E S S", fontsize=9.6,
                   fontname="med", fontfile=SB.FONT_TITLE_MED, color=SB.GREY)
    size, y = 33.0, 96
    for i, line in enumerate(SB.wrap(TITLE, SB.f_title, size, 460)):
        pg.insert_text((x0, y + 32 + i * 36), line, fontsize=size, fontname="ttl",
                       fontfile=SB.FONT_TITLE, color=SB.INK)
    ty = y + 32 + 2 * 36 + 2
    pg.draw_rect(pymupdf.Rect(x0, ty, x0 + 22, ty + 3), color=None,
                 fill=tuple(c / 255 for c in STRIPE))
    pg.insert_text((x0, ty + 22), "Year %d · Prime School Press · Student Manual"
                   % YEAR, fontsize=11, fontname="body", fontfile=SB.FONT_BODY,
                   color=SB.GREY)
    f_body = pymupdf.Font(fontfile=SB.FONT_BODY)
    by = ty + 48
    for para in ("Instructions are just stepping stones, and you write them.",
                 "Five units that take you from clear instructions to real "
                 "programs. Spot the bug before the machine does, collect honest "
                 "data, and build a program that does exactly what you meant."):
        for ln in SB.wrap(para, f_body, 11.4, 438):
            pg.insert_text((x0, by), ln, fontsize=11.4, fontname="body",
                           fontfile=SB.FONT_BODY, color=SB.INKISH)
            by += 17.2
        by += 7
    bullets = ["Five units from instructions to programs",
               "Predict, run and compare, every time",
               "Real bug hunts, with the fix never printed",
               "A project in every unit",
               "QR codes, each printed in words as well"]
    card_x0, card_x1 = x0 - 14, 470
    card_y0 = max(by + 6, 0.42 * H)
    card_y1 = min(card_y0 + 30 + 9 + len(bullets) * 19 + 14, H - 120)
    card = pg.new_shape()
    card.draw_rect(pymupdf.Rect(card_x0, card_y0, card_x1, card_y1), radius=0.06)
    card.finish(color=None, fill=SB.SAND)
    card.commit()
    pg.insert_text((card_x0 + 16, card_y0 + 24), "INSIDE THIS BOOK", fontsize=9.4,
                   fontname="med", fontfile=SB.FONT_TITLE_MED, color=SB.BROWN)
    yy = card_y0 + 44
    for bl in bullets:
        pg.insert_text((card_x0 + 16, yy), "\u2022", fontsize=10.6, fontname="body",
                       fontfile=SB.FONT_BODY, color=SB.INKISH)
        first = True
        for ln in SB.wrap(bl, f_body, 10.6, card_x1 - card_x0 - 46):
            pg.insert_text((card_x0 + 30, yy), ln, fontsize=10.6, fontname="body",
                           fontfile=SB.FONT_BODY, color=SB.INKISH)
            yy += 19 if first else 15
            first = False
    fy = H - 65
    pg.insert_text((x0, fy), "Prime School Press · %s" % TITLE, fontsize=9,
                   fontname="med", fontfile=SB.FONT_TITLE_MED, color=SB.INK)
    pg.insert_text((x0, fy + 16), "%s · %s" % (AGES, BAND), fontsize=9,
                   fontname="body", fontfile=SB.FONT_BODY, color=SB.GREY)
    pg.insert_text((x0, fy + 32), "primeschool.pt", fontsize=9, fontname="med",
                   fontfile=SB.FONT_TITLE_MED, color=SB.TERRA)
    return pg


# ------------------------------------------------------------------ imprint --
IMPRINT_ROWS = [
    ["EDITION", "First edition, 2026. Printed in full colour on white stock."],
    ["PUBLISHER", "Prime School Press is the publishing imprint of Prime School, "
                  "Portugal."],
    ["RIGHTS", "© Prime School 2026. All rights reserved. No part of this "
               "publication may be reproduced, stored in a retrieval system or "
               "transmitted in any form or by any means without the prior written "
               "permission of the publisher."],
    ["CREDITS", "Editorial Board. Pedagogical Academic Group · Pedagogical Team · "
                "Pedagogical Department · Content Creation Team. Written, "
                "illustrated and typeset in the Prime School Press studio, Lisbon."],
    ["LICENCE", "It is an independent publication and is not an official Cambridge "
                "Assessment International Education or Oxford University Press "
                "publication."],
    ["TEACHERS", "Pupils write in this book. It is meant to be written in."],
]


def imprint_spec():
    return dict(hl=C.FRONT, hr=C.HR_FRONT, kick="IMPRINT · COMPUTING & ROBOTICS · YEAR 3",
                title="Prime School Press", blocks=[
                    E.B.subhead("P R I M E  S C H O O L  P R E S S"),
                    E.B.lead("%s · Year %d · Student Book" % (TITLE, YEAR)),
                    E.B.para("Instructions are just stepping stones, and you write "
                             "them."),
                    E.B.ticks("Inside this book", [
                        "Five units from instructions to programs",
                        "Predict, run and compare, every time",
                        "Real bug hunts, with the fix never printed",
                        "A project in every unit",
                        "QR codes, each printed in words as well"]),
                    E.B.table(["IMPRINT", ""], IMPRINT_ROWS, widths=[0.20, 0.80]),
                    E.B.para("Independent publication. This is an independent "
                             "publication produced by Prime School for use within "
                             "its own programmes of study. It is not affiliated "
                             "with, licensed by, endorsed by or approved by any "
                             "examination board, or by any other publisher."),
                    E.B.para("%s · %s   ·   www.primeschool.pt" % (AGES, BAND)),
                ])


# --------------------------------------------------------------------- build --
def main():
    pages = C.build_pages()
    doc = pymupdf.open()
    draw_cover(doc)
    pg, bottom, over = E.render_page(doc, imprint_spec(), C.FRONT, 2, unit=0)
    print("imprint bottom %.1f over=%s" % (bottom, over))

    report = []
    for i, p in enumerate(pages):
        num = doc.page_count + 1
        if p["kind"] == "page":
            spec = dict(hl=p["hl"], hr=p["hr"], kick=p["kick"], title=p["title"],
                        blocks=p["blocks"])
        else:
            spec = p["spec"]
        if p["kind"] == "opener":
            _pg, bottom = E.render_opener(doc, spec, num)
            report.append((num, "opener", round(bottom, 1), 0, False))
            continue
        _pg, bottom, bad = E.render_page(doc, spec, p["folio"], num, unit=p["unit"])
        print("  built p%-3d %-38s bottom %6.1f" % (num, spec["title"][:38], bottom),
              flush=True)
        text = _pg.get_text().strip()
        sparse = len(text) < 140 and not any(n == "plate" for n, _ in spec["blocks"])
        report.append((num, spec["title"][:34], round(bottom, 1), len(text), sparse))
        if bad:
            print("  !! overflow page %d  bottom %.1f  %s" % (num, bottom,
                                                              spec["title"][:40]))
        if sparse:
            print("  !! sparse page %d  %d chars  %s" % (num, len(text),
                                                         spec["title"][:40]))

    draw_back(doc)
    total = doc.page_count
    doc.set_metadata({"title": "%s - Year %d (Prime Books)" % (TITLE, YEAR),
                      "author": "Prime School Press", "subject": "Computing & Robotics",
                      "creator": "Prime Books standard A-2.3 build"})
    doc.save(OUT, deflate=True, garbage=3, clean=True)
    print("total pages:", total, "even:", total % 2 == 0)
    print("interior content pages:", len(pages))
    for row in report:
        print("   p%-3d %-36s bottom %6.1f chars %5d%s"
              % (row[0], row[1], row[2], row[3], "  SPARSE" if row[4] else ""))

    chk = pymupdf.open(OUT)
    bad = []
    for i, q in enumerate(chk):
        for b in q.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            x0, y0, x1, y1 = b["bbox"]
            if x1 > E.MR + 1.5 or x0 < E.ML - 1.5 or y1 > 776:
                bad.append((i + 1, round(x0, 1), round(x1, 1), round(y1, 1)))
    print("out-of-margin text:", bad)
    fams = set()
    for q in chk:
        for f in q.get_fonts(full=True):
            fams.add((f[3], f[2]))
    print("fonts:", sorted(fams))

    sizes = {}
    for q in chk:
        for b in q.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    k = round(s["size"], 1)
                    sizes[k] = sizes.get(k, 0) + len(s["text"])
    big = sorted(((v, k) for k, v in sizes.items() if v >= 300), reverse=True)
    print("char counts by size:", sorted(sizes.items()))
    print("modal reading size (largest carrier >=300 chars):",
          big[0][1] if big else None)

    if "--commit" in sys.argv:
        shutil.copy(OUT, MASTER)
        print("master replaced:", MASTER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
