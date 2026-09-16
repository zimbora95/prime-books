#!/usr/bin/env python3
"""Build the first two standardised pages of Physical Education Year 1.

Physical page 3 is the CONTENTS page and physical page 4 is the WELCOME page,
per Standard A-2.3 Years 1 to 4 (public/standards/years-1-4.json).

WHAT CHANGED IN THIS REVISION (the teacher's brief)
  * no running head. "Prime School Press / Physical Education · Year 1" bought
    nothing on a page the reader has just opened, and the space is better spent
    on the cards; BookVault also wants the gutter clear, so every point back is
    worth having.
  * the page's matter is no longer loose rows at the top: the front matter is a
    coloured UNIT 0 card ("Getting started") and the back matter a coloured
    UNIT 7 card ("Looking back"), so the contents reads as one grid of eight
    cards - the six units and the two ends of the book - each in its own colour.
  * the nine-segment colour bar carries 0 and 7 as well as the six units.
  * the cast portraits are cut out of their cream sheet and stand on the page's
    own tint, so the six read as characters in the book, not as six photographs
    in six white boxes.
  * the page is student-facing: the teacher note that used to sit at the foot of
    the welcome page is gone (it belongs in the teacher's manual, and the same
    words remain on the master's own page 3).

    .venv/bin/python build_pages.py            # build + render + report
"""
import json
import os

import pymupdf

WORK = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(WORK, "art")
REPO = os.path.abspath(os.path.join(WORK, "..", ".."))
FONTDIR = "/root/pbfonts"
MASTER = os.path.join(REPO, "public/library/y01-physical-education/book.pdf")
TOKENS = json.load(open(os.path.join(REPO, "public/standards/years-1-4.json")))
MODEL = json.load(open(os.path.join(WORK, "contents-model.json")))

OUT_PDF = os.path.join(WORK, "y01-pe-standard-pages.pdf")
OUT_JSON = os.path.join(WORK, "build-report.json")

# ---- tokens -----------------------------------------------------------------
T = TOKENS
INK = T["ink"]
MUTED = T["muted_ink"]
AMBER = T["year_stripes"]["1"]            # Year 1 stripe: the front-matter accent
OCHRE = "#9A6A12"                         # house ochre mid: publisher furniture
# the art's own paper: the cut portraits were painted on (249,243,230), so a panel
# in exactly that colour shows no seam where a thread of paper survives the cut
PAPER = "#F9F3E6"
RUNGS = {r["unit"]: r for r in T["unit_palette"]["rungs"]}
W, H = T["geometry"]["authoring_page_pt"]
TOP = 60.0
BOTTOM = 726.0
GUTTER = 56.7                             # 20 mm from the binding edge
TRIM_SAFETY = 14.2                        # 5 mm from the other three edges
FOLIO = T["geometry"]["folio_centre_pt"]
FOLIO_D = T["geometry"]["folio_diameter_pt"]
YEAR = 1
SUBJECT = "Physical Education"

# the two ends of the book get rungs of their own, declared in the standard so
# every Year 1-4 title uses the same two colours for the same two cards
UNIT0 = RUNGS[0]
UNIT7 = RUNGS[7]

FONTS = {
    "fredoka": os.path.join(FONTDIR, "Fredoka-SemiBold.ttf"),
    "andika": os.path.join(FONTDIR, "Andika-Regular.ttf"),
    "andika_bold": os.path.join(FONTDIR, "Andika-Bold.ttf"),
    "poppins": os.path.join(FONTDIR, "Poppins-SemiBold.ttf"),
    "poppins_xb": os.path.join(FONTDIR, "Poppins-ExtraBold.ttf"),
    "caveat": os.path.join(FONTDIR, "Caveat-Regular.ttf"),
}


def rgb(hexs):
    hexs = hexs.lstrip("#")
    return tuple(int(hexs[i:i + 2], 16) / 255 for i in (0, 2, 4))


# Measure with the real font files: get_text_length() only knows the base-14
# names, and every page here is set in an embedded house face.
FONT_OBJ = {name: pymupdf.Font(fontfile=path) for name, path in FONTS.items()}


def text_w(text, font, size):
    return FONT_OBJ[font].text_length(text, fontsize=size)


def wrap(text, font, size, width):
    """Greedy wrap; returns a list of lines that fit `width`."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def right(page, text, font, size, x_right, baseline, color):
    page.insert_text((x_right - text_w(text, font, size), baseline), text,
                     fontname=font, fontsize=size, color=color)


def leader(page, x0, x1, baseline, color, gap=3.0):
    """A light dot leader between a row's title and its page number."""
    if x1 - x0 < 8:
        return
    y = baseline - 1.6
    x = x0
    while x < x1 - gap:
        page.draw_line(pymupdf.Point(x, y), pymupdf.Point(min(x + 0.7, x1 - gap), y),
                       color=color, width=0.35)
        x += 3.2


def dot_row(page, title, pageno, x0, x1, baseline, font, size, color, page_color):
    """A matter row inside a card: title, dot leader, right-aligned page."""
    page.insert_text((x0, baseline), title, fontname=font, fontsize=size, color=color)
    ptxt = str(pageno)
    pw = text_w(ptxt, font, size)
    right(page, ptxt, font, size, x1, baseline, page_color)
    start = x0 + text_w(title, font, size) + 4
    leader(page, start, x1 - pw - 4, baseline, rgb("#C9C2D6"))


def wrap_balanced(text, font, size, width, max_lines=3):
    """Wrap so no line is left with a single orphan word.

    "A barn owl. She watches, and says what she / saw." leaves "saw." alone on
    the last line; narrowing the measure until the last line carries at least two
    words evens the block out without changing a word of the sentence.
    """
    base = wrap(text, font, size, width)
    for shrink in (0.97, 0.94, 0.91, 0.88, 0.85, 0.82):
        alt = wrap(text, font, size, width * shrink)
        if len(alt) == len(base) and len(alt[-1].split()) > 1:
            return alt[:max_lines]
    return base[:max_lines]


def register(page):
    for name, path in FONTS.items():
        page.insert_font(fontname=name, fontfile=path)


def rounded(page, rect, fill, radius=0.06, stroke=None, width=0.6):
    """Rounded panel. PyMuPDF takes the radius as a fraction of the short side."""
    try:
        page.draw_rect(rect, color=stroke, fill=fill, width=width, radius=radius)
    except (TypeError, ValueError):
        page.draw_rect(rect, color=stroke, fill=fill, width=width)


def badge(page, x, y, label, fill, numeral):
    page.draw_circle(pymupdf.Point(x, y), FOLIO_D / 2, color=None, fill=fill)
    tw = text_w(label, "fredoka", 11)
    page.insert_text((x - tw / 2, y + 3.9), label, fontname="fredoka", fontsize=11,
                     color=numeral)


def matter_card(page, rect, rung, box, eyebrow, title, span, summary, rows, row_step=9.6):
    """One of the two book-end cards: a heading, then the page's own list.

    Laid out exactly like a unit card - colour bar on the leading edge, eyebrow
    and range on the first line, the card's name under it, a one-line summary -
    so the eight cards read as one set, while the dot leaders keep it obvious
    that these rows are pages rather than topics. Rows start on the same line as
    the unit cards' topics and step at the same pitch, so the grid lines up
    across the page.
    """
    cx, cy, card_w, card_h = rect
    rounded(page, pymupdf.Rect(cx, cy, cx + card_w, cy + card_h), rgb(rung["tint"]),
            radius=0.055)
    page.draw_rect(pymupdf.Rect(cx, cy, cx + 3.5, cy + card_h),
                   color=None, fill=rgb(rung["mid"]))
    tx = cx + 14
    page.insert_text((tx, cy + 19), eyebrow, fontname="fredoka", fontsize=9.5,
                     color=rgb(rung["deep"]))
    right(page, span, "andika", 8.5, cx + card_w - 12, cy + 19, rgb(MUTED))
    page.insert_text((tx, cy + 37), title, fontname="fredoka", fontsize=13.5,
                     color=rgb(rung["deep"]))
    sum_lines = wrap(summary, "andika", 8.5, card_w - 28)[:1]
    if sum_lines:
        page.insert_text((tx, cy + 50), sum_lines[0], fontname="andika",
                         fontsize=8.5, color=rgb(MUTED))
    y = cy + 56 + row_step
    for label, pg in rows:
        dot_row(page, label, pg, tx, cx + card_w - 12, y, "andika", 9, rgb(INK),
                rgb(rung["deep"]))
        y += row_step
    return y


# ---- page 3: contents -------------------------------------------------------
def build_contents(doc):
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = GUTTER, W - TRIM_SAFETY           # recto: gutter on the left
    cw = x1 - x0

    page.insert_text((x0, TOP + 2), "CONTENTS", fontname="fredoka", fontsize=9.5,
                     color=rgb(OCHRE))
    page.insert_text((x0, TOP + 32), "What is inside?", fontname="fredoka",
                     fontsize=26, color=rgb(INK))
    # the master's own line, word for word, then one line naming the two book-end
    # cards so "six units" and "eight colours" do not contradict each other
    page.insert_text((x0, TOP + 54), MODEL["lead"], fontname="andika", fontsize=14.5,
                     color=rgb(INK))
    page.insert_text((x0, TOP + 70),
                     "The pages before Unit 1 and the pages you come back to "
                     "have colours of their own.",
                     fontname="andika", fontsize=11.5, color=rgb(MUTED))

    # the colour bar: UNIT 0, the six units, UNIT 7 - one segment each
    units = MODEL["units"]
    keys = [0] + [u["unit"] for u in units] + [7]
    bar_y, bar_h, gap = TOP + 80, 15.0, 4.0
    seg = (cw - gap * (len(keys) - 1)) / len(keys)
    for i, k in enumerate(keys):
        r = RUNGS[k]
        bx = x0 + i * (seg + gap)
        page.draw_rect(pymupdf.Rect(bx, bar_y, bx + seg, bar_y + bar_h),
                       color=None, fill=rgb(r["mid"]))
        label = str(k)
        lw = text_w(label, "fredoka", 9)
        page.insert_text((bx + seg / 2 - lw / 2, bar_y + 10.6), label,
                         fontname="fredoka", fontsize=9, color=(1, 1, 1))

    # eight cards, two to a row: Unit 0 opens the grid, Unit 7 closes it, so the
    # contents reads in one pass: what comes before the work, the work, what is
    # there to come back to.
    card_w = (cw - 17) / 2
    topic_step = 9.6
    card_h = 56.0 + 6 * topic_step + 12.0 + 8.0
    top = bar_y + bar_h + 14
    vgap = 7.0

    front = [(r["title"], 4 if r["title"] == "Welcome" else r["real_page"])
             for r in MODEL["front_matter"]
             if r["title"] not in ("Contents", "CONTENTS")]
    # the master's own contents page is wrong on one row: it sends Answers for
    # every unit (2) to 92; the page it names is headed "Answers for every unit
    # (continued)" and sits at 91. Verified against the built PDF.
    back = [(r["title"], {"Answers for every unit (2)": 91}.get(r["title"], r["real_page"]))
            for r in MODEL["back_matter"]
            if r["title"] not in ("Contents", "CONTENTS")]

    slots = ([("unit0", front)] + [("unit", u) for u in units] + [("unit7", back)])
    for i, (kind, payload) in enumerate(slots):
        col, row = i % 2, i // 2
        cx = x0 + col * (card_w + 17)
        cy = top + row * (card_h + vgap)
        if kind == "unit0":
            matter_card(page, (cx, cy, card_w, card_h), UNIT0, None, "UNIT 0",
                        "Getting started", "pages 4\u201311",
                        "The book itself, and how to use it.", payload, topic_step)
            continue
        if kind == "unit7":
            matter_card(page, (cx, cy, card_w, card_h), UNIT7, None, "UNIT 7",
                        "Looking back", "pages 86\u201397",
                        "The words, the answers, the sources.", payload, topic_step)
            continue

        u = payload
        r = RUNGS[u["unit"]]
        card = pymupdf.Rect(cx, cy, cx + card_w, cy + card_h)
        rounded(page, card, rgb(r["tint"]), radius=0.055)
        page.draw_rect(pymupdf.Rect(cx, cy, cx + 3.5, cy + card_h),
                       color=None, fill=rgb(r["mid"]))
        tx = cx + 14
        page.insert_text((tx, cy + 19), f"UNIT {u['unit']}", fontname="fredoka",
                         fontsize=9.5, color=rgb(r["deep"]))
        right(page, f"page {u['real_opener']}", "andika", 8.5, cx + card_w - 12,
              cy + 19, rgb(MUTED))
        page.insert_text((tx, cy + 37), u["name"], fontname="fredoka", fontsize=13.5,
                         color=rgb(r["deep"]))
        sum_lines = wrap(u["summary"], "andika", 8.5, card_w - 28)[:1]
        if sum_lines:
            page.insert_text((tx, cy + 50), sum_lines[0], fontname="andika",
                             fontsize=8.5, color=rgb(MUTED))
        ty = cy + 56 + topic_step
        for t in u["topics"]:
            page.insert_text((tx, ty), t["title"], fontname="andika", fontsize=9,
                             color=rgb(INK))
            right(page, str(t["real_page"]), "andika", 9, cx + card_w - 12, ty,
                  rgb(r["deep"]))
            ty += topic_step
        ty += 2
        page.insert_text((tx, ty), u["check"], fontname="fredoka", fontsize=8.5,
                         color=rgb(r["deep"]))
        right(page, str(u["check_real_page"]), "andika", 9, cx + card_w - 12, ty,
              rgb(r["deep"]))

    badge(page, FOLIO[0], FOLIO[1], "3", rgb(AMBER), rgb(INK))
    return page


# ---- page 4: welcome --------------------------------------------------------
def build_welcome(doc):
    page = doc.new_page(width=W, height=H)
    register(page)
    x0, x1 = TRIM_SAFETY, W - GUTTER           # verso: gutter on the right
    cw = x1 - x0

    # "GETTING STARTED" rather than "WELCOME": this page is the first page of the
    # Unit 0 card on the contents page, and it avoids the kicker simply repeating
    # the display title underneath it
    page.insert_text((x0, TOP + 2), "GETTING STARTED", fontname="fredoka", fontsize=9.5,
                     color=rgb(OCHRE))
    page.insert_text((x0, TOP + 34), "Welcome", fontname="fredoka", fontsize=26,
                     color=rgb(INK))

    # the hero picture: full content width, cropped to a wide band
    hero_h = 150.0
    slot = pymupdf.Rect(x0, TOP + 48, x1, TOP + 48 + hero_h)
    page.insert_image(slot, filename=ART + "/hero-meadow-3to1.png")

    # the invitation, word for word from the approved page
    prose_y = slot.y1 + 22
    for para in MODEL["welcome_paragraphs"]:
        for ln in wrap(para, "andika", 14, cw):
            page.insert_text((x0, prose_y), ln, fontname="andika", fontsize=14,
                             color=rgb(INK))
            prose_y += 18.5
        prose_y += 6.0

    # this subject's own cast, two rows of three so the portraits are large
    # enough to read and each character keeps a legible line
    cast = json.load(open(os.path.join(ART, "cast.json")))["cast"]
    head_y = prose_y + 6
    page.insert_text((x0, head_y), "THE SIX WHO MOVE WITH YOU", fontname="fredoka",
                     fontsize=9.5, color=rgb(OCHRE))
    band = pymupdf.Rect(x0, head_y + 10, x1, BOTTOM)
    # the panel is the book's own paper, not a unit tint: the cut portraits carry
    # a thread of their original cream paper, and on paper it disappears where on
    # a tint it reads as a box. The teal of Unit 0 stays in the kicker.
    rounded(page, band, rgb(PAPER), radius=0.03)
    cols, rows = 3, 2
    pad = 12.0
    gap_x, gap_y = 8.0, 12.0
    cell_w = (band.width - pad * 2 - gap_x * (cols - 1)) / cols
    cell_h = (band.height - pad * 2 - gap_y * (rows - 1)) / rows
    fig_h = cell_h - 30
    hmax = max(c.get("frac", 1.0) for c in cast) or 1.0
    for i, c in enumerate(cast):
        col, row = i % cols, i // cols
        cell_x = band.x0 + pad + col * (cell_w + gap_x)
        cell_y = band.y0 + pad + row * (cell_h + gap_y)
        img = os.path.join(ART, c["file"])
        im = pymupdf.Pixmap(img)
        ar = im.width / im.height
        # partial normalisation: the hare stays the tallest, the hedgehog stops
        # leaving a hole above itself
        d_h = fig_h * (c.get("frac", 1.0) / hmax) ** 0.45
        d_w = d_h * ar
        if d_w > cell_w:
            d_w, d_h = cell_w, cell_w / ar
        # bottom-aligned in the cell, centred: one baseline per row
        ix = cell_x + (cell_w - d_w) / 2
        iy = cell_y + fig_h - d_h
        page.insert_image(pymupdf.Rect(ix, iy, ix + d_w, iy + d_h), filename=img)
        label = (c.get("label") or c["name"]).capitalize()
        lw = text_w(label, "fredoka", 10)
        page.insert_text((cell_x + (cell_w - lw) / 2, cell_y + fig_h + 12), label,
                         fontname="fredoka", fontsize=10, color=rgb(INK))
        ly = cell_y + fig_h + 22
        for ln in wrap_balanced(c["line"], "andika", 8.2, cell_w):
            lw2 = text_w(ln, "andika", 8.2)
            page.insert_text((cell_x + (cell_w - lw2) / 2, ly), ln,
                             fontname="andika", fontsize=8.2, color=rgb(MUTED))
            ly += 9.6

    # the imprint sits at the inner edge, on the footer line, so the badge and the
    # address are not stacked into one crowded corner
    right(page, "www.primeschool.pt", "andika", 9, x1, 746, rgb(MUTED))
    badge(page, W - FOLIO[0], FOLIO[1], "4", rgb(AMBER), rgb(INK))   # mirrored folio
    return page


def main():
    doc = pymupdf.open()
    build_contents(doc)
    build_welcome(doc)
    doc.set_metadata({"title": f"{SUBJECT} · Year {YEAR} · Standard A-2.3 shell pages",
                      "author": "Prime School Press",
                      "subject": "Prime Books Standard A-2.3, Years 1 to 4"})
    doc.save(OUT_PDF, deflate=True, garbage=3)
    report = {"pdf": OUT_PDF, "pages": doc.page_count,
              "size_pt": [W, H],
              "units": len(MODEL["units"]),
              "cards": 8,
              "topics": sum(len(u["topics"]) for u in MODEL["units"]),
              "cast": len(json.load(open(os.path.join(ART, "cast.json")))["cast"]),
              "running_head": False,
              "drift_rows": len(MODEL["drift"])}
    json.dump(report, open(OUT_JSON, "w"), indent=1)
    print(json.dumps(report, indent=1))
    for i, name in ((0, "p3-contents"), (1, "p4-welcome")):
        pix = doc[i].get_pixmap(dpi=140)
        out = os.path.join(WORK, f"render-{name}.png")
        pix.save(out)
        print("rendered", out, pix.width, "x", pix.height)
    doc.close()


if __name__ == "__main__":
    main()
