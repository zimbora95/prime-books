#!/usr/bin/env python3
"""Build KDP wrap covers for Prime Books, straight from the book PDF.

KDP PAPERBACK SPEC (user-confirmed, Premium Color):
  Trim        8.5 x 11.5 in  (215.9 x 292.1 mm)
  Bleed       0.125 in       (3.175 mm) on every edge
  Spine       pages x 0.002347 in  (pages x 0.0596138 mm)
  Output      ONE PDF, left to right: bleed + BACK + SPINE + FRONT + bleed
  Resolution  300 DPI
  Spine text  only when pages >= 79, kept clear of the spine edges

THE WRAP IS DERIVED, NEVER HAND-DRAWN:
  - FRONT COVER  = the PDF's first page, full-bleed.
  - BACK COVER   = the PDF's designed back page when present (detected via
    imprint/blurb markers or a textless full-art page), else a composed back
    (dimmed front art + blurb from the book's own Welcome/About page +
    imprint + barcode box).
  - SPINE        = solid colour from the OFFICIAL Prime Books year palette
    (the same colour as each year's catalogue-cover band: Y1 amber, Y2 sky
    blue, Y3 orange, ... Y12 red), vertical title + imprint when the page
    count allows text.

Because everything is derived from the book PDF, updating the book's cover
or back cover and re-running this script (the site does it automatically
when it detects the PDF is newer than the wrap) updates the wrap.

Usage:
  python make_wrap_cover.py <slug> [slug2 ...]
  python make_wrap_cover.py --all
"""
import json
import pathlib
import sys

import pymupdf
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter

REPO = pathlib.Path(__file__).resolve().parent.parent
LIBRARY = REPO / "public" / "library"
FONTS = REPO / "public" / "Resources" / "Fonts"

DPI = 300
TRIM_W, TRIM_H = 8.5, 11.5  # inches (user spec)
BLEED = 0.125  # inches
SPINE_PER_PAGE = 0.002347  # inches, Premium Color
MIN_SPINE_TEXT_PAGES = 79  # KDP rule

CREAM = (246, 241, 230)
INK = (32, 38, 48)
GOLD = (201, 163, 92)

# Official Prime Books year colours, sampled from the catalogue covers'
# spine-side bands (public/collection-covers). Y13 has no cover yet; fall
# back to the deepest tone.
YEAR_COLOURS = {
    1: (241, 179, 0),    # amber
    2: (126, 196, 232),  # sky blue
    3: (237, 118, 35),   # orange
    4: (96, 188, 70),    # green
    5: (193, 35, 127),   # magenta
    6: (129, 94, 193),   # violet
    7: (200, 153, 21),   # gold
    8: (91, 42, 134),    # purple
    9: (121, 31, 43),    # oxblood
    10: (74, 94, 58),    # olive
    11: (30, 79, 166),   # blue
    12: (201, 15, 46),   # red
}


def spine_colour(year: int) -> tuple:
    return YEAR_COLOURS.get(int(year), YEAR_COLOURS[12])


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def rows() -> list:
    return json.loads((REPO / "public" / "library.json").read_text())


def slug_meta(slug: str) -> dict:
    for r in rows():
        if r["slug"] == slug:
            return r
    raise SystemExit(f"slug not in library.json: {slug}")


def page_image(doc: pymupdf.Document, idx: int, dpi: int) -> Image.Image:
    pix = doc[idx].get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


BACK_MARKERS = (
    "about this book",
    "www.prime",
    "first edition",
    "isbn",
    "barcode",
    "all rights",
    "primeschool.pt",
)


def page_is_art(doc: pymupdf.Document, idx: int) -> bool:
    """Textless page that is not pure white — cream back covers (Y2) carry
    their whole design as vector art, so whiteness must be measured against
    pure paper (255) with a tolerance."""
    if doc[idx].get_text().strip():
        return False
    pix = doc[idx].get_pixmap(dpi=10)
    d = pix.samples
    n = len(d) // 3
    nonwhite = 0
    for i in range(0, len(d), 3):
        if not (d[i] > 252 and d[i + 1] > 252 and d[i + 2] > 252):
            nonwhite += 1
    return n > 0 and nonwhite / n > 0.3


def find_designed_back(doc: pymupdf.Document) -> int | None:
    """Index of the book's real back-cover page.

    The back cover is nearly always the LAST page. Only walk further back
    when the last page is provably interior (running headers/page numbers).
    "FOR TEACHERS" pages with 'about this book' are interior pages, not
    covers — excluded explicitly.
    """
    n = doc.page_count
    for i in range(n - 1, max(n - 4, 0) - 1, -1):
        t = doc[i].get_text().strip().lower()
        if "for teachers" in t or t[:4] == "page":
            continue  # interior furniture
        if any(m in t for m in BACK_MARKERS):
            return i
    if page_is_art(doc, n - 1):
        return n - 1
    return None


def find_blurb(doc: pymupdf.Document) -> str:
    """Pull a back-cover blurb from the book's own front matter.

    "about this book" > "welcome" > "introduction" — weaker anchors also
    appear on the FRONT COVER, so never scan page 1 and only accept real
    paragraphs.
    """
    n = doc.page_count
    anchors = ("about this book", "welcome", "introduction")
    for i in range(1, min(6, n)):
        t = doc[i].get_text()
        low = t.lower()
        for anchor in anchors:
            at = low.find(anchor)
            if at >= 0:
                snippet = t[at : at + 800]
                lines = [
                    ln.strip()
                    for ln in snippet.splitlines()
                    if ln.strip() and not ln.strip().isdigit()
                ]
                text = " ".join(lines[1:])
                text = " ".join(text.split())
                if (
                    len(text) > 120
                    and text.count("Prime Books") <= 2
                    and "image " not in text[:30].lower()
                ):
                    return text[:600].rsplit(".", 1)[0] + "."
    return ""


def fit(im: Image.Image, w: int, h: int) -> Image.Image:
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def compose_synth_back(front: Image.Image, meta: dict, blurb: str) -> Image.Image:
    """Synthetic back: dimmed front art, cream panel with the blurb,
    imprint bar, KDP barcode box."""
    back = fit(front, front.width, front.height)
    back = ImageEnhance.Brightness(back).enhance(0.55)
    back = back.filter(ImageFilter.GaussianBlur(6))
    bd = ImageDraw.Draw(back)
    W, H = back.size
    SORA = "Sora.dl"
    SPECTRAL = "Spectral-Medium.ttf.dl"
    pad = round(W * 0.07)
    px0, px1 = pad, W - pad
    py0 = round(H * 0.05)
    maxw = px1 - px0 - pad

    f_head = font(SORA, round(H * 0.019))
    f_title = font(SPECTRAL, round(H * 0.028))
    f_body = font(SPECTRAL, round(H * 0.015))
    f_meta = font(SPECTRAL, round(H * 0.014))

    def wrap(text, f, maxw):
        lines, cur = [], ""
        for w in text.split():
            t = (cur + " " + w).strip()
            if bd.textlength(t, font=f) <= maxw:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    b1 = (blurb or
          f"{meta['subject']} for Year {meta['year']}: structured units, "
          "activities and full-colour artwork, written for Prime School "
          "pupils in clear British English.")
    blocks = [
        (["ABOUT THIS BOOK"], f_head, GOLD, f_head.size, 18),
        ([f"{meta['subject']} \u00b7 Year {meta['year']}"], f_title, INK, f_title.size, 26),
        (wrap(b1, f_body, maxw), f_body, INK, f_body.size, 8),
        ([f"{meta.get('band') or 'Prime Books'}  \u00b7  Student Manual  \u00b7  "
          f"{meta.get('pages') or ''} pages".replace("  ·  ", "  \u00b7  ")],
         f_meta, (110, 100, 84), f_meta.size, 0),
    ]
    content_h = sum(len(ls) * s + g for ls, _, _, s, g in blocks)
    py1 = py0 + pad + content_h + pad
    bd.rounded_rectangle([px0, py0, px1, py1], radius=36, fill=CREAM)
    x, y = px0 + pad // 2, py0 + pad // 2
    for lines, f, color, s, g in blocks:
        for ln in lines:
            bd.text((x, y), ln, font=f, fill=color)
            y += s
        y += g

    # barcode + imprint (imprint bar sits ABOVE the barcode, full-width)
    bx1 = W - round(W * 0.05)
    bx0 = bx1 - round(W * 0.24)
    by1 = H - round(H * 0.03)
    by0 = by1 - round(H * 0.115)
    f_imp = font(SPECTRAL, round(H * 0.013))
    t = "Prime Books \u2014 the publishing imprint of Prime School, Portugal"
    wt = bd.textlength(t, font=f_imp)
    iy = by0 - round(H * 0.14)
    bd.rectangle([0, iy - 16, W, iy + round(H * 0.015)], fill=(24, 28, 34))
    bd.text(((W - wt) // 2, iy), t, font=f_imp, fill=CREAM)
    bd.rectangle([bx0, by0, bx1, by1], fill=(255, 255, 255))
    return back


def build(slug: str) -> pathlib.Path:
    meta = slug_meta(slug)
    year = int(meta["year"])
    subject = meta["subject"]

    doc = pymupdf.open(LIBRARY / slug / "book.pdf")
    n = doc.page_count
    front = page_image(doc, 0, DPI)
    back_idx = find_designed_back(doc)
    blurb = find_blurb(doc)
    doc.close()

    spine_in = n * SPINE_PER_PAGE
    W = round((TRIM_W * 2 + spine_in + BLEED * 2) * DPI)
    H = round((TRIM_H + BLEED * 2) * DPI)
    back_w = round((TRIM_W + BLEED) * DPI)
    spine_w = round(spine_in * DPI)
    front_w = round((TRIM_W + BLEED) * DPI)

    canvas = Image.new("RGB", (W, H), CREAM)

    if back_idx is not None:
        back = page_image(pymupdf.open(LIBRARY / slug / "book.pdf"), back_idx, DPI)
        canvas.paste(fit(back, back_w, H), (0, 0))
        back_src = "pdf-back"
    else:
        synth = compose_synth_back(fit(front, back_w, H), meta, blurb)
        canvas.paste(synth, (0, 0))
        back_src = "synthetic"

    canvas.paste(fit(front, front_w, H), (back_w + spine_w, 0))  # FRONT

    # ---- spine: official year colour, solid; text only when KDP allows ----
    col = spine_colour(year)
    canvas.paste(Image.new("RGB", (spine_w, H), col), (back_w, 0))
    if n >= MIN_SPINE_TEXT_PAGES:
        # Text on a TRANSPARENT strip pasted over the year colour — never a
        # black background (that was the bug: Image.new defaults to black).
        strip = Image.new("RGBA", (H, spine_w), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        f1 = font("Sora.dl", 34)
        f2 = font("Spectral-Medium.ttf.dl", 26)
        # ink colour chosen for contrast against the year colour
        lum = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
        ink = (32, 38, 48) if lum > 140 else CREAM

        def spine_line(text, f, x, color):
            bbox = sd.textbbox((0, 0), text, font=f)
            th = bbox[3] - bbox[1]
            ty = (spine_w - th) // 2 - bbox[1]
            sd.text((x, ty), text, font=f, fill=color + (255,))
            return sd.textlength(text, font=f)

        title = f"{subject.upper()}  \u00b7  YEAR {year}"
        t2 = "PRIME BOOKS"
        w1 = sd.textlength(title, font=f1)
        w2 = sd.textlength(t2, font=f2)
        gap = 160
        x0 = (H - (w1 + gap + w2)) // 2
        spine_line(title, f1, x0, ink)
        spine_line(t2, f2, x0 + w1 + gap, ink)
        canvas.paste(strip.transpose(Image.ROTATE_270), (back_w, 0), strip.transpose(Image.ROTATE_270))

    # KDP deliverable is a single PDF
    out_png = LIBRARY / slug / "cover-wrap-amazon.png"
    canvas.save(out_png, "PNG", optimize=True)
    out_pdf = LIBRARY / slug / "cover-wrap-amazon.pdf"
    canvas.save(out_pdf, "PDF", resolution=DPI)

    # keep the manifest in step so the site sees wrapCover immediately
    data = json.loads((REPO / "public" / "library.json").read_text())
    for r in data:
        if r.get("slug") == slug:
            r["wrapCover"] = f"/library/{slug}/cover-wrap-amazon.png"
            r["wrapCoverPdf"] = f"/library/{slug}/cover-wrap-amazon.pdf"
    (REPO / "public" / "library.json").write_text(
        json.dumps(data, indent=1, ensure_ascii=False)
    )

    print(
        f"{slug}: {n}pp  spine {spine_in:.4f}in ({spine_in*25.4:.2f}mm)  "
        f"{W}x{H}px  back={back_src}  "
        f"pdf {out_pdf.stat().st_size/1e6:.1f}MB  png {out_png.stat().st_size/1e6:.1f}MB"
    )
    return out_pdf


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    if args[0] == "--all":
        args = [r["slug"] for r in rows() if (LIBRARY / r["slug"] / "book.pdf").is_file()]
    for slug in args:
        build(slug)
