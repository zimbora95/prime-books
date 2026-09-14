#!/usr/bin/env python3
"""Build the BookVault upload pack for one Prime Books title.

WHAT BOOKVAULT ASKS FOR (help.bookvault.app + bookvault.app/uploading-your-files)
-------------------------------------------------------------------------------
Two files per title, uploaded individually:

  "text file"   the INTERIOR, print-ready PDF, single pages, page count matching
                the spec entered on the title.
  "cover file"  the COVER WRAP as one PDF: back cover + spine + front cover,
                left to right, built over BookVault's cover template for the
                chosen binding.

  Both PDFs, PDF/X-1a:2001 or PDF/X-3:2002, CMYK (or Grayscale), fonts fully
  embedded, images >= 300 DPI, 0.125 in (3.175 mm) bleed wherever art reaches
  the trim, nothing critical within 3 mm of the trim, no crop marks.

WHAT THIS SCRIPT PRODUCES  (public/library/<slug>/bookvault/)
------------------------------------------------------------
  <slug>-text-file.pdf      the interior, BookVault-ready:
                              - the book's OWN trim size, declared in BookVault
                                as a CUSTOM size (US Letter 215.9 x 279.4 mm)
                              - front cover and back cover STRIPPED OUT: in a
                                Prime Books PDF page 1 IS the front cover and
                                the last page IS the back cover, and both are
                                reprinted in the cover file. Leaving them in
                                prints the cover twice.
                              - 0.125 in bleed on all four edges, extended from
                                each page's own edge artwork as VECTOR
                                (see bleed_page: no rasterising, no hairline)
                              - converted to PDF/X-3:2002 with CMYK by
                                Ghostscript (--no-pdfx skips this)
  <slug>-cover-file.pdf     the wrap: back + spine + front, full bleed, 300 DPI,
                            spine width from the interior page count
  <slug>-cover-file.png     a PNG preview of the same wrap (for the web page)
  <slug>-bookvault.txt      the UPLOAD SHEET: every number BookVault will ask
                            for, plus the pass/fail checks, so the title can be
                            set up on bookvault.app without guessing
  build.json                machine-readable record: what was built, the spec,
                            the checks, and when. The web page reads this.

THE ONE NUMBER YOU MUST CONFIRM
-------------------------------
The SPINE WIDTH. BookVault's guide (p.18) computes it with the sizing calculator
on their site -- home > help > sizing calculator -- for the paper you print on,
then ROUNDS UP to a whole millimetre. Their worked example is 100 pages on
80 gsm bond = 5.6 mm = 6 mm, which is where SPINE_PER_PAGE_MM below comes from:
0.056 mm per page. A colour interior is likely a heavier stock and therefore a
thicker spine, so the number is printed on the sheet, the page shows it as an
OPEN check, and you can override it with --spine-mm <mm> (or
--spine-per-page-mm <mm>) once the calculator gives you the real figure.

All other numbers are taken from the guide and from BookVault's own templates,
which are committed alongside this tool in docs/bookvault/.

Usage
-----
    .venv/bin/python tools/make_bookvault_files.py <slug> [slug ...]
    .venv/bin/python tools/make_bookvault_files.py --all
    .venv/bin/python tools/make_bookvault_files.py <slug> --force --no-pdfx
"""
from __future__ import annotations

import argparse
import io
import json
import math
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

import pymupdf
from PIL import Image

REPO = pathlib.Path(__file__).resolve().parent.parent
LIBRARY = REPO / "public" / "library"
SETTINGS_PATH = REPO / "public" / "bookvault.json"

sys.path.insert(0, str(REPO / "tools"))
import make_wrap_cover as mwc  # noqa: E402  (shares the wrap-cover machinery)

# ------------------------------------------------ BookVault spec (their guide)
# Every number below comes from "Your Guide to Supplying Print-Ready PDF Files"
# (docs/bookvault/Guide-To-PDFs.pdf) and from BookVault's own templates:
#   docs/bookvault/v4_Text_279_216.pdf                 222 x 285 mm  (text)
#   docs/bookvault/v4_PerfectBound_Cover_279_216_5.pdf 443 x 285 mm  (cover)
MM_PER_PT = 25.4 / 72.0
PT_PER_MM = 72.0 / 25.4

TRIM_W_MM = 216.0          # finished book width  (template "Finished Size")
TRIM_H_MM = 279.0          # finished book height
BLEED_MM = 3.0             # guide p.5: "the bleed that we require for text is 3mm"
SAFETY_MM = 5.0            # guide p.19: content safety margin from the trim edge
BINDING_SAFETY_MM = 17.0   # template: "17 mm on the binding edge" (guide text says 20)
GUTTER_SAFETY_MM = 20.0    # guide p.3, interior files: "safety margin of 20mm on the gutter"
MARGIN_HEADROOM_MM = 1.0   # aim a millimetre past each rule, so trimming drift is absorbed
BARCODE_MM = (38.0, 25.0)  # template's barcode placement box
BARCODE_FROM_TRIM_MM = (6.4, 3.3)   # ...and its inset from the back cover trim
SPINE_PER_PAGE_MM = 0.056  # guide p.18: 100 pages on 80 gsm bond = 5.6 mm
PAGES_MODULO = 12          # guide p.5: "one less than a divisible of 12"

TRIM_W = TRIM_W_MM * PT_PER_MM          # 612.28 pt (was 612: US Letter)
TRIM_H = TRIM_H_MM * PT_PER_MM          # 790.87 pt (was 792)
BLEED_PT = BLEED_MM * PT_PER_MM         # 8.50 pt -- 3 mm, NOT 0.125 in (9 pt)
TEXT_W, TEXT_H = TRIM_W + 2 * BLEED_PT, TRIM_H + 2 * BLEED_PT   # 222 x 285 mm

DPI = 300                 # cover raster resolution (guide p.9: 300 DPI required)
SEG_PT = 1.0              # bleed smear segment length (1 pt: a piece of artwork
                          # no thicker than a rule must not be averaged away)
SEG_DPI = 600             # resolution the edge is sampled at
# The bleed continues the page's own edge colour, so it is sampled from a thin
# band INSIDE the cut, never from the last row: MuPDF renders a page's final
# ~0.1 pt as near-white (251,249,241), and a strip that touches it averages that
# phantom row into every colour, lightening the whole bleed margin.
EDGE_BAND_INSET_PT = 0.15  # start this far inside the edge
EDGE_BAND_PT = 0.7         # and stop this far inside (0.25 mm band in total)
SMEAR_SMOOTH_PT = 3.4      # box-average the smear over ~1.2 mm along the edge:
                           # see smooth_cols() -- 0 disables the averaging
SEAM_WINDOW_PT = 3.0       # seam check: compare over ~1 mm windows (see seam_mismatch)
MAX_EDGE_STEP = 20         # per-step colour change (of 255) that counts as a
                           # photographic edge -- above it a flat smear is visible
TRIM_DRIFT_MM = 1.0        # how far past the trim artwork must reach, so a
                           # printer's trim drift cannot expose the margin fill
EDGE_HAIR_MM = 0.25        # a margin fill reaching less than this inside the trim
                           # is a hairline: under any printing tolerance, and what
                           # a master 0.3 mm narrower than the trim produces
FIT_MAX = 1.12             # never enlarge a page more than this to reach the trim
GHOSTSCRIPT = shutil.which("gs")

# BookVault print defaults for a Prime Books title. Editable per book on the
# BookVault page (public/bookvault.json); these are only the fallbacks.
DEFAULT_SETTINGS = {
    "binding": "Perfect bound (paperback)",
    "paper": "Colour interior, 80 gsm uncoated",
    "lamination": "Matte",
    "isbn": "",
    "printType": "Standard",
}

# --------------------------------------------------------------------- helpers


def rows() -> list:
    return json.loads((REPO / "public" / "library.json").read_text())


def slug_meta(slug: str) -> dict:
    for r in rows():
        if r.get("slug") == slug:
            return r
    raise SystemExit(f"slug not in library.json: {slug}")


def read_settings() -> dict:
    try:
        d = json.loads(SETTINGS_PATH.read_text())
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def settings_for(slug: str) -> dict:
    s = dict(DEFAULT_SETTINGS)
    s.update(read_settings().get(slug) or {})
    return s


def pt_to_mm(v: float) -> float:
    return v * 25.4 / 72.0


def fmt_mm(v: float) -> str:
    return f"{pt_to_mm(v):.2f}".rstrip("0").rstrip(".")


def mm(v: float) -> str:
    """Format a value that is ALREADY in millimetres (cover geometry).

    Running those through fmt_mm() converted a 442 mm cover into '156 mm',
    which is exactly the sort of number a teacher would send to a printer.
    """
    return f"{v:.2f}".rstrip("0").rstrip(".")


def out_dir(slug: str) -> pathlib.Path:
    return LIBRARY / slug / "bookvault"


# ------------------------------------------------------- bleed: vector edge smear


def sample_edge(page: pymupdf.Page, horizontal: bool, length_pt: float,
                at_pt: float, steps: int, thickness_pt: float = 1.0) -> list[tuple[int, int, int]]:
    """Average a strip of the page's edge into `steps` colour samples.

    Averaging is done by PIL's BOX resize (C speed). Hand-rolling the loop in
    Python made this 60x slower and is why protos took minutes per book.
    """
    if horizontal:
        clip = pymupdf.Rect(0, at_pt, length_pt, at_pt + thickness_pt)
    else:
        clip = pymupdf.Rect(at_pt, 0, at_pt + thickness_pt, length_pt)
    pix = page.get_pixmap(clip=clip, dpi=SEG_DPI)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if not horizontal:
        im = im.transpose(Image.ROTATE_90)   # scan along the edge, not across
    im = im.resize((max(1, steps), 1), Image.BOX)
    return [tuple(im.getpixel((x, 0)))[:3] for x in range(im.width)]


def smear_columns(page: pymupdf.Page, horizontal: bool, offset_pt: float,
                  src_len_pt: float, media_len_pt: float, at_pt: float,
                  steps_pt: float, thickness_pt: float = EDGE_BAND_PT,
                  scale: float = 1.0) -> list[tuple[int, int, int]]:
    """Edge colours mapped into MEDIA coordinates, with the ends clamped.

    The page sits inside a slightly larger media box, so media row r shows source
    row (r - offset_pt) / scale. The smear has to follow that mapping: sampling
    the edge in the page's own coordinates and stretching the result across the
    margin shifts every abrupt edge in the artwork (a rule, a band bottom) by the
    offset, and the seam then shows a band of the wrong colour. Ends clamp to the
    first/last edge sample, which is what a bleed smear does at a corner.
    """
    n_media = max(1, int(round(media_len_pt / steps_pt)))
    n_src = max(1, int(round(src_len_pt / steps_pt)))
    cols = sample_edge(page, horizontal, src_len_pt, at_pt, n_src, thickness_pt)
    first, last = cols[0], cols[-1]
    out = []
    for i in range(n_media):
        # the media segment's CENTRE mapped into source space, then the sample
        # that contains it: floor, not round -- rounding picks the neighbouring
        # sample half the time and puts a 1 pt step at every abrupt edge.
        j = int(((i + 0.5) * steps_pt - offset_pt) / scale)
        out.append(first if j < 0 else last if j >= n_src else cols[j])
    return out


def smooth_cols(cols: list[tuple[int, int, int]], radius: int) -> list[tuple[int, int, int]]:
    """Box-average the smear across `radius` segments either side.

    At 1 pt segments the raw samples extrude the page's outermost row of pixels
    up its full margin, which on a photographic edge prints as fine vertical
    stripes. Averaging over ~1.2 mm turns the same colours into a soft
    continuation, and a flat, gradient or blank edge is unchanged by it.
    """
    if radius < 1 or len(cols) < 3:
        return cols
    out = []
    n = len(cols)
    for i in range(n):
        a, b = max(0, i - radius), min(n, i + radius + 1)
        take = cols[a:b]
        out.append((sum(c[0] for c in take) // len(take),
                    sum(c[1] for c in take) // len(take),
                    sum(c[2] for c in take) // len(take)))
    return out


def rgb01(c) -> tuple:
    return (c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)


def draw_runs(page: pymupdf.Page, cols, orientation: str, extent: float,
              thickness: float, start: float) -> None:
    """Draw the smear as merged solid runs -- vector, and a flat edge colour
    collapses into a single rectangle instead of hundreds.

    `extent` is the MEDIA span to cover (trim + 2 x bleed), not the trim: the
    samples come from the trim edge but the margin to paint is wider than the
    page, and using the trim width left the far strip of the top margin white.
    """
    n = len(cols)
    if not n:
        return
    seg_len = extent / n
    i = 0
    while i < n:
        j = i + 1
        while j < n and cols[j] == cols[i]:
            j += 1
        a, b = i * seg_len, j * seg_len
        rect = (pymupdf.Rect(a, start, b, start + thickness) if orientation == "v"
                else pymupdf.Rect(start, a, start + thickness, b))
        page.draw_rect(rect, color=None, fill=rgb01(cols[i]), width=0)
        i = j


def page_margins_mm(p: pymupdf.Page, w_mm: float, h_mm: float,
                    ox: float, oy: float, scale: float = 1.0) -> dict | None:
    """Live content's distance to the four trim edges, in mm.

    Text spans only: the full-bleed band and the artwork are meant to run off the
    page, so they are not "content" for this purpose. None when the page has no
    text at all (a picture page has nothing to protect). `ox`/`oy` are the
    master's page box offset from the trim's top-left at `scale`.
    """
    blocks = p.get_text("blocks")
    if not blocks:
        return None
    x0 = min(b[0] for b in blocks) * MM_PER_PT
    x1 = max(b[2] for b in blocks) * MM_PER_PT
    y0 = min(b[1] for b in blocks) * MM_PER_PT
    y1 = max(b[3] for b in blocks) * MM_PER_PT
    return {"left": ox + x0 * scale, "right": ox + (w_mm - x1) * scale,
            "top": oy + y0 * scale, "bottom": oy + (h_mm - y1) * scale}


def _master_size(slug: str) -> tuple[float, float]:
    """The master's page box in points, or (0, 0) when it is missing."""
    p = LIBRARY / slug / "book.pdf"
    if not p.is_file():
        return 0.0, 0.0
    d = pymupdf.open(p)
    rect = d[0].rect
    d.close()
    return rect.width, rect.height


def source_font_note(slug: str, missing: list[str]) -> str:
    """Say whether an unembedded font is ours or inherited from the master.

    Neither MuPDF nor Ghostscript can embed a font whose program is not in the
    file, and for a standard-14 name like Helvetica Ghostscript rewrites the file
    and leaves the reference exactly as it was (measured on y01-english: the
    reference survives `-dEmbedAllFonts=true`, `-sAlwaysEmbed`, and
    `subset_fonts()`). So when the master references the same font, the pack is
    only carrying the master's defect and the fix belongs in the source.
    """
    p = LIBRARY / slug / "book.pdf"
    if not p.is_file():
        return ""
    wanted = {m.split(" [")[0].strip() for m in missing}
    d = pymupdf.open(p)
    seen = set()
    for pno in range(d.page_count):
        for f in d.get_page_fonts(pno, full=True):
            if f[2] not in ("Type3", "Type 3") and f[3] in wanted:
                seen.add(f[3])
    d.close()
    if not seen:
        return ""
    return (" -- the master references the same font (" + ", ".join(sorted(seen)[:3])
            + "), so re-export the master without it: the pack cannot embed a font "
              "whose program is not in the file")


def margin_fill_inside_trim(slug: str, doc: pymupdf.Document, fit: float = 1.0,
                            shift: tuple = (0.0, 0.0)) -> tuple[int, float, float, float]:
    """Where the margin fill lands relative to the trim, from the placement geometry.

    Returns (pages whose fill reaches MORE THAN A HAIR inside the trim on a VISIBLE
    edge, the worst such depth in mm, the deepest fill at the gutter in mm, the
    least distance the artwork reaches PAST the trim on the visible edges).

    The gutter is treated separately because the safety shift deliberately moves
    the page away from it: the band that opens sits against the binding, inside
    BookVault's own 20 mm gutter zone, and is the page's own edge colour
    continuing into the spine. Outer, top and bottom are what the reader sees on
    an open page, and nothing artificial may reach inside the trim there.
    """
    master_path = LIBRARY / slug / "book.pdf"
    if not master_path.is_file():
        return 0, 0.0, 0.0, 0.0
    md = pymupdf.open(master_path)
    w, h = md[0].rect.width, md[0].rect.height
    n = min(doc.page_count, max(0, md.page_count - 2))
    bad, worst, worst_gutter, least = 0, 0.0, 0.0, 999.0
    for i in range(n):
        rect = place_rect(w, h, fit, i + 1, shift[0], shift[1])
        # positive = the margin fill starts INSIDE the trim; negative = the
        # artwork reaches that far past the trim into the bleed
        bands = {"left": rect.x0 - BLEED_PT,
                 "right": (TEXT_W - BLEED_PT) - rect.x1,
                 "top": rect.y0 - BLEED_PT,
                 "bottom": (TEXT_H - BLEED_PT) - rect.y1}
        recto = (i + 1) % 2 == 1          # pack page: odd pages are right-hand
        gutter_side = "left" if recto else "right"
        outer_side = "right" if recto else "left"
        # the vertical side the shift gives way on: the page moves down, so the
        # band opens along the top, and that edge is the page's own colour there
        give = "top" if shift[1] > 0 else ("bottom" if shift[1] < 0 else None)
        worst_gutter = max(worst_gutter, pt_to_mm(bands[gutter_side]))
        for side in ("left", "right", "top", "bottom"):
            if side in (gutter_side, give):
                continue                  # where the page deliberately gives way
            if bands[side] > EDGE_HAIR_MM * PT_PER_MM:
                bad += 1
                worst = max(worst, pt_to_mm(bands[side]))
        other_v = "bottom" if give == "top" else "top"
        least = min(least, -pt_to_mm(bands[outer_side]), -pt_to_mm(bands[other_v]))
    md.close()
    return bad, worst, worst_gutter, (0.0 if least == 999.0 else least)


def margin_extremes(src: pymupdf.Document, first: int, last: int) -> dict:
    """Tightest live-text margins in the MASTER's own coordinates, in mm.

    Measured once per book and reused: the shift that clears BookVault's margins
    depends on how much the page is scaled, and solving for that scale would
    otherwise re-read every page of a 750-page master on each pass.
    """
    w_mm, h_mm = src[0].rect.width * MM_PER_PT, src[0].rect.height * MM_PER_PT
    out = {"w": w_mm, "h": h_mm, "gutter": 999.0, "outer": 999.0,
           "top": 999.0, "bottom": 999.0, "tight": ""}
    for idx in range(first, last + 1):
        p = src[idx]
        blocks = p.get_text("blocks")
        if not blocks:
            continue
        x0 = min(b[0] for b in blocks) * MM_PER_PT
        x1 = max(b[2] for b in blocks) * MM_PER_PT
        y0 = min(b[1] for b in blocks) * MM_PER_PT
        y1 = max(b[3] for b in blocks) * MM_PER_PT
        recto = idx % 2 == 1              # pack page idx: odd pages are right-hand
        left, right = x0, w_mm - x1
        gutter = left if recto else right
        outer = right if recto else left
        if gutter < out["gutter"]:
            out["gutter"], out["tight"] = gutter, f"page {idx}, {gutter:.1f} mm off the gutter"
        out["outer"] = min(out["outer"], outer)
        out["top"] = min(out["top"], y0)
        out["bottom"] = min(out["bottom"], h_mm - y1)
    return out


def shift_for(scale: float, ex: dict) -> tuple[float, float]:
    """The safety shift for a given fit scale: (outward mm, down mm).

    The margins are measured from the TRIM, so the master's box offset at this
    scale counts: below 1.0 the box sits inside the trim and gives the margin
    away, above 1.0 it runs past the trim and takes it back.
    """
    if ex["gutter"] > 900:                # no live text anywhere (a picture book)
        return 0.0, 0.0
    ox = (TRIM_W_MM - ex["w"] * scale) / 2.0
    oy = (TRIM_H_MM - ex["h"] * scale) / 2.0
    min_gutter = ox + ex["gutter"] * scale
    min_outer = ox + ex["outer"] * scale
    min_top = oy + ex["top"] * scale
    min_bottom = oy + ex["bottom"] * scale
    shift_x = max(0.0, min(GUTTER_SAFETY_MM + MARGIN_HEADROOM_MM - min_gutter,
                           min_outer - SAFETY_MM - MARGIN_HEADROOM_MM))
    shift_y = max(0.0, min(SAFETY_MM + MARGIN_HEADROOM_MM - min_top,
                           min_bottom - SAFETY_MM - MARGIN_HEADROOM_MM))
    return shift_x, shift_y


def content_shift(src: pymupdf.Document, first: int, last: int,
                  scale: float = 1.0) -> tuple[float, float, str]:
    """How far to move the page furniture so live content clears their margins.

    BookVault wants a 20 mm safety margin on the gutter (guide p.3, interior
    files) and 5 mm from the trim on the other three edges (their text template;
    17 mm on the binding edge there). Our masters carry 13 mm to 18 mm gutter
    margins, so the page is MOVED, never rescaled for this purpose.

    Returns (mm toward the outer edge, mm down, a note for the printed sheet).
    """
    ex = margin_extremes(src, first, last)
    if ex["gutter"] > 900:
        return 0.0, 0.0, "no live text on the interior pages (a picture book); nothing to move"
    shift_x, shift_y = shift_for(scale, ex)
    ox = (TRIM_W_MM - ex["w"] * scale) / 2.0
    oy = (TRIM_H_MM - ex["h"] * scale) / 2.0
    min_gutter, min_outer = ox + ex["gutter"] * scale, ox + ex["outer"] * scale
    min_top, min_bottom = oy + ex["top"] * scale, oy + ex["bottom"] * scale
    got_gutter, got_outer = min_gutter + shift_x, min_outer - shift_x
    got_top, got_bottom = min_top + shift_y, min_bottom - shift_y
    note = (f"content moved {shift_x:.1f} mm toward the outer edge and {shift_y:.1f} mm down: "
            f"closest live text is now {got_gutter:.1f} mm off the gutter "
            f"(was {min_gutter:.1f}), {got_outer:.1f} mm from the outer trim "
            f"(was {min_outer:.1f}) and {got_top:.1f} mm from the top trim "
            f"(their rules: {GUTTER_SAFETY_MM:g} mm gutter, {SAFETY_MM:g} mm trim; "
            f"tightest {ex['tight']})")
    if got_gutter < GUTTER_SAFETY_MM - 0.05:
        note += (f"; this page cannot reach {GUTTER_SAFETY_MM:g} mm without pushing the "
                 f"outer margin under {SAFETY_MM:g} mm")
    elif got_gutter < GUTTER_SAFETY_MM + MARGIN_HEADROOM_MM - 0.05:
        note += "; the full 1 mm headroom will not fit, the rule itself does"
    return shift_x, shift_y, note


def edge_detail(src: pymupdf.Document, first: int, last: int,
                step_pt: float = 6.0) -> int:
    """Worst colour step along the outermost sliver of the interior pages.

    This is the measurement that decides whether a master smaller than the trim
    can simply sit inside it. The margin outside a page's box is filled with a
    flat smear of its edge colours: on a blank or flat-coloured edge that is
    invisible, on a photographic one it prints as clamped streaks, and where the
    master is smaller than the trim those streaks fall INSIDE the cut.
    """
    worst = 0
    for idx in range(first, last + 1):
        p = src[idx]
        for horizontal, length, at in ((True, p.rect.width, EDGE_BAND_INSET_PT),
                                       (True, p.rect.width, p.rect.height - EDGE_BAND_INSET_PT - EDGE_BAND_PT),
                                       (False, p.rect.height, EDGE_BAND_INSET_PT),
                                       (False, p.rect.height, p.rect.width - EDGE_BAND_INSET_PT - EDGE_BAND_PT)):
            n = max(2, int(round(length / step_pt)))
            cols = sample_edge(p, horizontal, length, at, n, EDGE_BAND_PT)
            for a, b in zip(cols, cols[1:]):
                worst = max(worst, max(abs(x - y) for x, y in zip(a, b)))
            if worst > MAX_EDGE_STEP:
                return worst
    return worst


def fit_scale(src: pymupdf.Document, first: int, last: int) -> tuple[float, str]:
    """How much the master's page box has to grow to reach BookVault's 216x279.

    1.0 unless the master is smaller than the trim AND its page edges carry
    detail. Enlarging moves type sizes, so it is only done where leaving it
    alone would print a flat smear of a photographic edge inside the cut --
    which is what a 209.9 x 269.9 mm master otherwise does on 3.05 mm (sides) and
    4.55 mm (top and bottom) of every page. The enlargement covers the whole
    222 x 285 mm media, not just the trim, so the bleed beyond the cut is real
    artwork too and no artificial band appears anywhere on the page. A master
    that already meets the trim (the US Letter books are 0.3 mm narrower and
    0.4 mm taller) never scales, and neither does one whose edges are blank or a
    flat colour.

    Oversized masters are NOT scaled down: the trim crops the overflow, which the
    crop check proves is margin only.
    """
    w = pt_to_mm(src[0].rect.width)
    h = pt_to_mm(src[0].rect.height)
    media_w, media_h = pt_to_mm(TEXT_W), pt_to_mm(TEXT_H)
    need = max(media_w / w, media_h / h)
    if need <= 1.0:
        return 1.0, (f"master page box {w:.1f} x {h:.1f} mm meets the "
                     f"{TRIM_W_MM:g} x {TRIM_H_MM:g} mm trim; no rescaling")
    if abs(w - TRIM_W_MM) < 1.0 and abs(h - TRIM_H_MM) < 1.0:
        return 1.0, (f"master page box {w:.1f} x {h:.1f} mm matches the trim "
                     f"within a printer's tolerance; no rescaling")
    detail = edge_detail(src, first, last)
    if detail <= MAX_EDGE_STEP:
        return 1.0, (f"master {w:.1f} x {h:.1f} mm sits {TRIM_W_MM - w:.2f} mm "
                     f"inside the trim on the sides and {TRIM_H_MM - h:.2f} mm "
                     f"top and bottom; its edges are flat (worst step {detail}/255) "
                     f"so the margin continues them invisibly -- no rescaling")
    # Enlarge just enough that the artwork still reaches 1 mm PAST the trim on
    # every side once the safety shift has moved the page -- the shift opens a
    # gap on the side it moves away from, and that gap has to fall in the bleed,
    # never on the printed page.
    #
    # Only taken when it converges: enlarging a page centred on the trim pushes
    # its content outward (the inset the undersized box was giving away is spent
    # on the enlargement), so a book whose text is already close to the gutter
    # needs a bigger shift, which needs a bigger enlargement, and so on. When
    # that diverges the page stays 1:1 -- its own inset keeps the gutter rule
    # comfortable -- and the 3-5 mm band inside the trim carries a soft
    # continuation of the page edge instead of artwork.
    ex = margin_extremes(src, first, last)
    scale, solved = need, False
    for _ in range(6):
        dx, dy = shift_for(scale, ex)
        want = max((TRIM_W_MM + 2 * TRIM_DRIFT_MM + 2 * dx) / w,
                   (TRIM_H_MM + 2 * TRIM_DRIFT_MM + 2 * dy) / h,
                   need)
        if abs(want - scale) < 0.0005:
            scale, solved = want, True
            break
        scale = want
    if not solved or scale > FIT_MAX:
        dix = TRIM_W_MM - w
        diy = TRIM_H_MM - h
        return 1.0, (f"master {w:.1f} x {h:.1f} mm is smaller than the "
                     f"{TRIM_W_MM:g} x {TRIM_H_MM:g} mm trim and its edges carry "
                     f"detail (worst step {detail}/255). Enlarging it to reach the "
                     f"cut would push its text out of the 20 mm gutter, so the page "
                     f"is placed 1:1: the outer {dix / 2:.2f} mm (sides) and "
                     f"{diy / 2:.2f} mm (top and bottom) of the printed page carry a "
                     f"soft continuation of the page edge. Re-export this master at "
                     f"{TRIM_W_MM:g} x {TRIM_H_MM:g} mm to remove it")
    # An enlargement is only worth its type-size change if the page then MEETS
    # their margins. It usually does not: growing an undersized page about the
    # trim's centre pushes its content outward, so a master whose text is already
    # close to the edges ends up further outside the rules, not closer.
    dx, dy = shift_for(scale, ex)
    ox = (TRIM_W_MM - w * scale) / 2.0
    oy = (TRIM_H_MM - h * scale) / 2.0
    if not (ox + ex["gutter"] * scale + dx >= GUTTER_SAFETY_MM - 0.05 and
            ox + ex["outer"] * scale - dx >= SAFETY_MM - 0.05 and
            oy + ex["top"] * scale + dy >= SAFETY_MM - 0.05 and
            oy + ex["bottom"] * scale - dy >= SAFETY_MM - 0.05):
        return 1.0, (f"master {w:.1f} x {h:.1f} mm is smaller than the "
                     f"{TRIM_W_MM:g} x {TRIM_H_MM:g} mm trim and its edges carry "
                     f"detail (worst step {detail}/255). Enlarging it would move "
                     f"its text further outside their gutter and trim margins "
                     f"rather than closer, so the page is placed 1:1 and its type "
                     f"sizes are untouched; the outer {(TRIM_W_MM - w) / 2:.2f} mm "
                     f"of the printed page carries a soft continuation of the page "
                     f"edge. Re-export this master at {TRIM_W_MM:g} x "
                     f"{TRIM_H_MM:g} mm with wider margins to remove it")
    return scale, (f"master {w:.1f} x {h:.1f} mm is smaller than the "
                   f"{TRIM_W_MM:g} x {TRIM_H_MM:g} mm trim and its edges carry "
                   f"detail (worst step {detail}/255), so a flat margin would show: "
                   f"the page is enlarged {scale * 100 - 100:.1f} % so the artwork "
                   f"reaches the edge of the {BLEED_MM:g} mm bleed")


def place_rect(w: float, h: float, scale: float, idx: int,
               shift_x_mm: float, shift_y_mm: float) -> pymupdf.Rect:
    """Where the master's page box lands on the media, at `scale`.

    Right-hand pages move toward their outer (right) edge, left-hand pages toward
    theirs, so the shift opens the gutter and gives way at the outer margin.
    """
    recto = idx % 2 == 1                 # pack page idx: odd pages are right-hand
    px = (TEXT_W - w * scale) / 2.0 + (shift_x_mm * PT_PER_MM if recto else -shift_x_mm * PT_PER_MM)
    py = (TEXT_H - h * scale) / 2.0 + shift_y_mm * PT_PER_MM
    return pymupdf.Rect(px, py, px + w * scale, py + h * scale)


def bleed_page(dst: pymupdf.Document, src: pymupdf.Document, idx: int,
               shift_x_mm: float = 0.0, shift_y_mm: float = 0.0,
               scale: float = 1.0) -> None:
    """One interior page onto BookVault's text-file media, 222 x 285 mm.

    The master is 612 x 792 pt (US Letter); BookVault's trim is 216 x 279 mm,
    which is 612.28 x 790.87 pt. Rather than rescale the page -- and with it
    every type size in the book -- the page is placed 1:1 on the trim box and the
    leftover margin is filled with the edge smear, so the artwork still reaches
    the cut line on all four sides.

    `shift_x_mm` moves the page toward its OUTER edge and `shift_y_mm` moves it
    down, so live text clears BookVault's gutter and trim safety margins (see
    content_shift). Right-hand pages move one way, left-hand pages the other, and
    what the shift opens at the gutter the smear fills.
    """
    p = src[idx]
    w, h = p.rect.width, p.rect.height
    page = dst.new_page(width=TEXT_W, height=TEXT_H)

    # The master's page box on the media at `scale` (1.0 unless the master is
    # undersized for the trim AND its edges carry detail -- see fit_scale), plus
    # the safety shift: outboard on a right-hand page, outboard-left on a
    # left-hand one.
    rect = place_rect(w, h, scale, idx, shift_x_mm, shift_y_mm)
    px, py, pw, ph = rect.x0, rect.y0, rect.width, rect.height

    # The band the bleed is sampled from, on each edge's inside. It must (a)
    # start inside the phantom white row MuPDF draws in the last ~0.1 pt (see
    # EDGE_BAND_PT) and (b) run right up to the cut, or the bleed continues
    # artwork from further inside the page and the cut line shows a step.
    ins, band = EDGE_BAND_INSET_PT, EDGE_BAND_PT
    top = smear_columns(p, True, px, w, TEXT_W, ins, SEG_PT, band, scale)
    bot = smear_columns(p, True, px, w, TEXT_W, h - ins - band, SEG_PT, band, scale)
    lef = smear_columns(p, False, py, h, TEXT_H, ins, SEG_PT, band, scale)
    rig = smear_columns(p, False, py, h, TEXT_H, w - ins - band, SEG_PT, band, scale)
    if SMEAR_SMOOTH_PT:
        r = max(1, int(round(SMEAR_SMOOTH_PT / SEG_PT)))
        top, bot = smooth_cols(top, r), smooth_cols(bot, r)
        lef, rig = smooth_cols(lef, r), smooth_cols(rig, r)

    # each margin is painted to its own extent: the placement is centred, so
    # the top and bottom strips are not the same thickness as the sides.
    # ARGUMENT ORDER IS (extent, thickness, start) -- swapping the last two
    # paints a page-sized band over the artwork (white interiors, caught by
    # page_content_survives()).
    draw_runs(page, top, "v", TEXT_W, py, 0)
    draw_runs(page, bot, "v", TEXT_W, TEXT_H - (py + ph), py + ph)
    draw_runs(page, lef, "h", TEXT_H, px, 0)
    draw_runs(page, rig, "h", TEXT_H, TEXT_W - (px + pw), px + pw)

    # corners: filled with the corner colour so no white pinhole survives
    for col, crect in (
        (top[0] if top else lef[0], pymupdf.Rect(0, 0, px, py)),
        (top[-1] if top else rig[0], pymupdf.Rect(px + pw, 0, TEXT_W, py)),
        (bot[0] if bot else lef[-1], pymupdf.Rect(0, py + ph, px, TEXT_H)),
        (bot[-1] if bot else rig[-1], pymupdf.Rect(px + pw, py + ph, TEXT_W, TEXT_H)),
    ):
        page.draw_rect(crect, color=None, fill=rgb01(col), width=0)

    # The page itself, LAST, so it paints over the smear wherever it has artwork.
    # Vector placement -- text stays text and no type size moves unless fit_scale
    # had to enlarge the page to reach the cut.
    page.show_pdf_page(rect, src, idx)


def blank_page(dst: pymupdf.Document) -> None:
    """A blank text-file page, 222 x 285 mm.

    Used to pad the page count to BookVault's 12n-1 rule (guide p.5). A blank
    page at the rear is also what their production barcode wants: they add it to
    the last page of the document, so it is better that nothing is printed there.
    """
    page = dst.new_page(width=TEXT_W, height=TEXT_H)
    page.draw_rect(pymupdf.Rect(0, 0, TEXT_W, TEXT_H), color=None,
                   fill=(1.0, 1.0, 1.0), width=0)


# ------------------------------------------------------------------- text file


def type3_fonts(doc: pymupdf.Document) -> int:
    """How many Type 3 font references the document carries.

    A Type 3 "font" is a program of drawing operators rather than an embedded
    font, and it is how raw glyph outlines end up in a PDF. Two consequences
    matter here:

      * Ghostscript 10.02.1 SEGFAULTS converting Type 3 content to CMYK (proved
        by bisection: the same pages convert cleanly with -dNoOutputFonts, which
        throws the Type 3 programs away, and the crash follows the pages that
        carry them). 47 of the 123 masters in the library carry them, so a CMYK
        pass is attempted only when they are absent.
      * Press preflight likes them least of all font types, so the count is
        reported whether or not the CMYK pass runs.
    """
    n, seen = 0, set()
    for i in range(doc.page_count):
        for f in doc[i].get_fonts(full=True):
            if f[0] in seen:
                continue
            seen.add(f[0])
            if doc.xref_get_key(f[0], "Subtype")[1] == "/Type3":
                n += 1
    return n


def pdfx_marker(path: pathlib.Path) -> tuple[str, bool]:
    """(PDF/X version, has an OutputIntent) read back from the finished file.

    Never trust the conversion's own exit code for this: the marker lives in the
    Info dictionary and the intent in the catalog, so both are read from the
    file a preflight would open.
    """
    ver, intent = "", False
    try:
        d = pymupdf.open(path)
        m = re.findall(r"(\d+) 0 R", d.xref_get_key(-1, "Info")[1] or "")
        if m:
            v = d.xref_get_key(int(m[0]), "GTS_PDFXVersion")
            if v[0] != "null":
                ver = (v[1] or "").strip().strip("()")
        try:
            intent = d.xref_get_key(d.pdf_catalog(), "OutputIntents")[0] != "null"
        except Exception:
            intent = False
        d.close()
    except Exception:
        pass
    return ver, intent


def write_pdfx_def(path: pathlib.Path, title: str) -> None:
    """A Ghostscript PDF/X-1a prefix file with a real OutputIntent.

    The guide (p.5) asks for PDF/A compliance or, "if possible", PDF/X-1a:2001
    settings, so this declares PDF/X-1a:2001 rather than the X-3 that
    Ghostscript's own PDFX_def.ps writes.

    Ghostscript ships PDFX_def.ps, but it points at 'ISO Coated sb.icc' in the
    current directory and stamps the title 'Title'. This writes our own, using
    the CMYK profile that actually exists on this host, so the output carries a
    valid DestOutputProfile instead of a dangling reference.
    """
    icc = "/usr/share/color/icc/ghostscript/default_cmyk.icc"
    path.write_text(
        f"""%!
[ /GTS_PDFXVersion (PDF/X-1a:2001)
  /Title ({title})
  /Trapped /False
/DOCINFO pdfmark
/ICCProfile ({icc}) def
currentdict /ICCProfile known {{
  [/_objdef {{icc_PDFX}} /type /stream /OBJ pdfmark
  [{{icc_PDFX}} << /N 4 >> /PUT pdfmark
  [{{icc_PDFX}} ICCProfile (r) file /PUT pdfmark
}} if
[/_objdef {{OutputIntent_PDFX}} /type /dict /OBJ pdfmark
[{{OutputIntent_PDFX}} <<
  /Type /OutputIntent
  /S /GTS_PDFX
  /OutputCondition (Commercial and specialty printing)
  /Info (none)
  /OutputConditionIdentifier (DEFAULT CMYK -- Ghostscript default_cmyk.icc)
  /RegistryName (http://www.color.org)
  /DestOutputProfile {{icc_PDFX}}
>> /PUT pdfmark
[{{Catalog}} <</OutputIntents [ {{OutputIntent_PDFX}} ]>> /PUT pdfmark
"""
    )


ICC_CMYK = "/usr/share/color/icc/ghostscript/default_cmyk.icc"


def to_pdfx(src_pdf: pathlib.Path, dst_pdf: pathlib.Path, title: str) -> tuple[bool, str]:
    """CMYK + PDF/X-3:2002 via Ghostscript, with a verified result.

    Two flags matter and both were learned the hard way:

      --permit-file-read=<icc>  Ghostscript 10 runs -dSAFER, which blocks
                                reading the output intent profile and aborts
                                with /invalidfileaccess. No permit, no PDF/X.
      -dNOTRANSPARENCY          PDF/X forbids transparency. Without this,
                                Ghostscript's PDF/X path FLATTENS every page
                                that carries an alpha image by RASTERISING the
                                whole page: the imprint and welcome pages (both
                                carry an alpha logo) came back as one image,
                                with zero embedded fonts -- a print-quality
                                regression that BookVault's own font check
                                would then fail. With it, transparency is
                                flattened but the text stays vector.

    Then the result is CHECKED, page by page, against the input: word count and
    embedded fonts. A conversion that silently rasterises pages is worse than no
    conversion, so a failed check falls back to the RGB file and says so.
    """
    if not GHOSTSCRIPT:
        shutil.copyfile(src_pdf, dst_pdf)
        return False, "Ghostscript not installed -- left as RGB, not PDF/X"

    # Type 3 content is the one thing Ghostscript 10.02.1 cannot convert to CMYK
    # without crashing, and the guide accepts RGB (p.6), so do not spend half an
    # hour finding that out: check first and keep the RGB file.
    t3 = 0
    try:
        d = pymupdf.open(src_pdf)
        t3 = type3_fonts(d)
        d.close()
    except Exception:
        t3 = 0
    if t3:
        shutil.copyfile(src_pdf, dst_pdf)
        return False, (f"kept RGB: {t3} Type 3 fonts block Ghostscript's CMYK "
                       f"conversion (guide p.6 accepts RGB, their preflight converts)")

    with tempfile.TemporaryDirectory() as td:
        defps = pathlib.Path(td) / "PDFX_def.ps"
        write_pdfx_def(defps, title)
        cmd = [
            GHOSTSCRIPT, "-dBATCH", "-dNOPAUSE", "-dSAFER",
            f"--permit-file-read={ICC_CMYK}",
            "-sDEVICE=pdfwrite", "-dPDFX", "-dPDFACompatibilityPolicy=1",
            "-sColorConversionStrategy=CMYK", "-dProcessColorModel=/DeviceCMYK",
            "-dNOTRANSPARENCY",
            "-dEmbedAllFonts=true", "-dSubsetFonts=true",
            "-dAutoRotatePages=/None", "-dDetectDuplicateImages=true",
            "-dDownsampleColorImages=false", "-dDownsampleGrayImages=false",
            "-dDownsampleMonoImages=false",
            f"-sOutputFile={dst_pdf}", str(defps), str(src_pdf),
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            shutil.copyfile(src_pdf, dst_pdf)
            return False, "Ghostscript timed out (15 min) -- left as RGB"
    if r.returncode != 0 or not dst_pdf.is_file():
        shutil.copyfile(src_pdf, dst_pdf)
        last = (r.stderr or "").strip().splitlines()[-1:] or [""]
        return False, f"Ghostscript failed ({r.returncode}: {last[0][:120]}) -- left as RGB"

    ver, intent = pdfx_marker(dst_pdf)
    if not ver or not intent:
        shutil.copyfile(src_pdf, dst_pdf)
        return False, (f"conversion carried no PDF/X marker "
                       f"(version {ver!r}, output intent {intent}) -- kept RGB")

    ok, why = conversion_is_faithful(src_pdf, dst_pdf)
    if not ok:
        shutil.copyfile(src_pdf, dst_pdf)
        return False, f"conversion damaged the file ({why}) -- kept RGB"
    return True, f"{ver}, CMYK, fonts embedded, text kept as text"


def left_transparency(path: pathlib.Path) -> bool:
    """Does this file still carry transparency? Cheap gate before a flatten pass."""
    try:
        d = pymupdf.open(path)
        n = len(transparency_pages(d))
        d.close()
        return n > 0
    except Exception:
        return False


def flatten_transparency(src_pdf: pathlib.Path, dst_pdf: pathlib.Path) -> tuple[bool, str]:
    """A plain Ghostscript pass with -dNOTRANSPARENCY and nothing else.

    Used when the CMYK/PDF-X pass cannot run: guide p.3 asks for flattened
    transparency as a hard requirement, and on these documents the plain pass is
    the one Ghostscript survives (it is the CMYK colour conversion that crashes
    on Type 3 content, not the flattening). No colour is touched, so the file
    stays RGB and is still not PDF/X -- this only removes the transparency.
    """
    if not GHOSTSCRIPT:
        return False, "not flattened (Ghostscript not installed)"
    cmd = [
        GHOSTSCRIPT, "-dBATCH", "-dNOPAUSE", "-dSAFER",
        "-sDEVICE=pdfwrite", "-dNOTRANSPARENCY",
        "-dEmbedAllFonts=true", "-dAutoRotatePages=/None",
        "-dDetectDuplicateImages=true",
        "-dDownsampleColorImages=false", "-dDownsampleGrayImages=false",
        "-dDownsampleMonoImages=false",
        f"-sOutputFile={dst_pdf}", str(src_pdf),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return False, "not flattened (the flattening pass timed out)"
    if r.returncode != 0 or not dst_pdf.is_file():
        return False, f"not flattened (Ghostscript exit {r.returncode})"
    d = pymupdf.open(dst_pdf)
    left = transparency_pages(d)
    d.close()
    if left:
        return False, f"not flattened ({len(left)} pages still carry transparency)"
    ok, why = conversion_is_faithful(src_pdf, dst_pdf)
    if not ok:
        return False, f"not flattened (the pass damaged the file: {why})"
    return True, "transparency flattened (RGB, not PDF/X)"


def conversion_is_faithful(before: pathlib.Path, after: pathlib.Path) -> tuple[bool, str]:
    """Did the PDF/X pass keep every page's TEXT and FONTS intact?

    Ghostscript's transparency flattening can turn a page into a single raster
    image. That looks fine in a viewer and is wrong for print, so it is caught
    here rather than discovered on the press.
    """
    a, b = pymupdf.open(before), pymupdf.open(after)
    if a.page_count != b.page_count:
        return False, f"page count {a.page_count} -> {b.page_count}"
    lost = []
    for i in range(a.page_count):
        wa = len(a[i].get_text().split())
        wb = len(b[i].get_text().split())
        if wa and wb < wa * 0.98:
            lost.append(f"page {i + 1}: {wa} -> {wb} words")
    if lost:
        return False, "; ".join(lost[:3])
    emb, missing = fonts_embedded(b)
    if not emb:
        return False, "fonts not embedded after conversion: " + ", ".join(missing[:3])
    return True, "ok"


def interior_page_count(slug: str) -> tuple[int, int]:
    """(content pages, padded pages) for a book's text file.

    The cover and the back cover live in the cover file, so the interior is
    pages 2..n-1 of the master. BookVault then want a page count that is ONE
    LESS than a multiple of 12 (guide p.5) because their production barcode is
    added to the last page of the document -- 11, 23, 35 and so on -- so the
    count is padded up with blank pages at the rear.
    """
    doc = pymupdf.open(LIBRARY / slug / "book.pdf")
    try:
        content = max(0, doc.page_count - 2)
    finally:
        doc.close()
    pad = (PAGES_MODULO - 1 - content) % PAGES_MODULO
    return content, content + pad


def alpha_flattened_source(src_path: pathlib.Path, od: pathlib.Path, slug: str):
    """Composite soft-masked images over their backdrop and drop the mask.

    Ghostscript's PDF/X path throws /SMask away: it writes the image without its
    mask, so the masked area prints in the plate's own base colour -- for the
    Prime School logo plate that base is black, which is why pages 1 and 2 of the
    text file had a black box in the top-right corner. Compositing here also
    satisfies the guide (PDF/X-1a:2001 allows no transparency) without trusting
    the converter to get it right. Returns the path of a flattened copy, or None
    when nothing carried a mask.
    """
    doc = pymupdf.open(src_path)
    seen: set[int] = set()
    done = 0
    for pno in range(doc.page_count):
        page = doc[pno]
        for img in page.get_images(full=True):
            xref, smask = img[0], img[1]
            if not smask or xref in seen:
                continue
            seen.add(xref)
            try:
                base = doc.extract_image(xref)
                mask = doc.extract_image(smask)
                mi = Image.open(io.BytesIO(mask["image"])).convert("L")
                bi = Image.open(io.BytesIO(base["image"]))
                mode = bi.mode if bi.mode in ("RGB", "CMYK", "L") else "RGB"
                if mi.getextrema()[0] == 255:      # mask is fully opaque: redundant
                    new = bi.convert(mode)
                else:
                    backdrop = {"RGB": (255, 255, 255), "CMYK": (0, 0, 0, 0), "L": 255}[mode]
                    canvas = Image.new(mode, bi.size, backdrop)
                    canvas.paste(bi.convert(mode), (0, 0), mi)
                    new = canvas
                buf = io.BytesIO()
                new.save(buf, format="PNG")
                page.replace_image(xref, stream=buf.getvalue())
                doc.xref_set_key(xref, "SMask", "null")
                done += 1
            except Exception as exc:               # never let artwork surgery be fatal
                print(f"  {slug}: image {xref} left as-is ({type(exc).__name__}: {exc})")
    if not done:
        doc.close()
        return None
    out = od / f".{slug}-alpha-flat.pdf"
    doc.save(str(out), garbage=4, deflate=True)
    doc.close()
    return out


def build_text_file(slug: str, force: bool, do_pdfx: bool, pad_12n: bool = False) -> dict:
    src_path = LIBRARY / slug / "book.pdf"
    od = out_dir(slug)
    od.mkdir(parents=True, exist_ok=True)
    final = od / f"{slug}-text-file.pdf"

    src = pymupdf.open(alpha_flattened_source(src_path, od, slug) or src_path)
    n = src.page_count
    if n < 4:
        src.close()
        raise SystemExit(f"{slug}: only {n} pages -- not a book")

    content, guide_pages = interior_page_count(slug)
    padded = guide_pages if pad_12n else content   # blanks at the rear only on request

    fit, fit_note = fit_scale(src, 1, n - 2)
    shift_x_mm, shift_y_mm, shift_note = content_shift(src, 1, n - 2, fit)

    stripped_cover = True
    work = pymupdf.open()
    for i in range(1, n - 1):          # page 1 (cover) and last (back cover) out
        bleed_page(work, src, i, shift_x_mm, shift_y_mm, fit)
    for _ in range(padded - content):      # pad to 12n-1 for their barcode
        blank_page(work)

    meta = slug_meta(slug)
    work.set_metadata({
        "title": f"{meta.get('subject', slug)} - Year {meta.get('year', '')} (interior)",
        "author": "Prime School Press",
        "producer": "Prime Books - BookVault text file",
        "creator": "Prime Books",
    })
    tmp = od / f".{slug}-text-file.rgb.pdf"
    work.save(str(tmp), garbage=4, deflate=True)
    work.close()
    src.close()

    ok, note = (False, "left as RGB (--no-pdfx)")
    if do_pdfx:
        ok, note = to_pdfx(tmp, final, f"{meta.get('subject', slug)} Year {meta.get('year', '')}")
        tmp.unlink(missing_ok=True)
    else:
        shutil.move(str(tmp), str(final))
    (od / f".{slug}-alpha-flat.pdf").unlink(missing_ok=True)

    # No PDF/X (Type 3 fonts, or Ghostscript bailed): still remove transparency,
    # which the guide lists as a hard requirement (p.3) rather than a preference.
    flattened = False
    flat_note = ""
    if do_pdfx and not ok and left_transparency(final):
        flat = od / f".{slug}-text-file.flat.pdf"
        flattened, flat_note = flatten_transparency(final, flat)
        if flattened:
            shutil.move(str(flat), str(final))
        else:
            flat.unlink(missing_ok=True)

    doc = pymupdf.open(final)
    left_transparent = transparency_pages(doc)
    rec = {
        "file": final.name,
        "url": f"/library/{slug}/bookvault/{final.name}",
        "bytes": final.stat().st_size,
        "pages": doc.page_count,
        "content_pages": content,
        "padded_pages": doc.page_count - content,
        "guide_suggested_pages": guide_pages,
        "pad_12n": bool(pad_12n),
        "pages_rule": (
            f"12n-1 supply ({PAGES_MODULO}n-1); packed {content} content pages, "
            + ("no blank padding (count is already a multiple of 12)" if padded == content
               and content % PAGES_MODULO == 0 else
               f"guide p.5 suggests {guide_pages} -- blank padding not supplied at the owner's request"
               if padded == content else
               f"{padded} supplied to carry their barcode on a blank last page")
        ),
        "trim_mm": [TRIM_W_MM, TRIM_H_MM],
        "page_fit_scale": round(fit, 5),
        "page_fit_note": fit_note,
        "content_shift_mm": [round(shift_x_mm, 2), round(shift_y_mm, 2)],
        "content_shift_note": shift_note,
        "media_mm": [round(pt_to_mm(doc[0].rect.width), 2),
                     round(pt_to_mm(doc[0].rect.height), 2)],
        "trim_pt": [round(doc[0].rect.width, 2), round(doc[0].rect.height, 2)],
        "bleed_mm": BLEED_MM,
        "cover_stripped": stripped_cover,
        "type3": type3_fonts(doc),
        "pdfx": bool(ok and do_pdfx),
        "flattened": flattened,
        "transparent_pages": len(left_transparent),
        "note": note + (f"; transparency left on {len(left_transparent)} pages "
                        f"(the flattening pass could not clear it)"
                        if flat_note and not flattened else ""),
    }
    doc.close()
    return rec


# ------------------------------------------------------------------ cover file


SPINE_TEXT_MIN_MM = 6.0    # below this the spine holds no type at all


def spine_mm_for(pages: int, per_page_mm: float | None = None,
                 exact_mm: float | None = None) -> float:
    """BookVault's spine width: caliper x pages, ROUNDED UP to a whole mm.

    Guide p.18: "100 pages on an 80gsm bond ... the spine should be 5.6mm, we
    would round this up to 6mm". --spine-mm overrides the whole calculation for
    when the sizing calculator has been run for the real paper.
    """
    if exact_mm:
        return float(exact_mm)
    per = SPINE_PER_PAGE_MM if per_page_mm is None else per_page_mm
    return float(math.ceil(pages * per))


def cover_geometry(spine_mm: float) -> dict:
    """Perfect-bound cover geometry, straight from the guide (p.18).

    Width : trim x 2, plus spine, plus 3 mm bleed left and right.
    Height: trim height + 3 mm bleed top and bottom.
    """
    w = TRIM_W_MM * 2 + spine_mm + BLEED_MM * 2
    h = TRIM_H_MM + BLEED_MM * 2
    return {
        "width_mm": round(w, 2),
        "height_mm": round(h, 2),
        "spine_mm": spine_mm,
        "back_w_mm": round(TRIM_W_MM + BLEED_MM, 2),
        "front_w_mm": round(TRIM_W_MM + BLEED_MM, 2),
    }


def build_cover_file(slug: str, spine_per_page_mm: float | None, spine_mm: float | None,
                     force: bool, pad_12n: bool = False) -> dict:
    od = out_dir(slug)
    od.mkdir(parents=True, exist_ok=True)
    meta = slug_meta(slug)
    year = int(meta["year"])
    subject = meta["subject"]

    book = LIBRARY / slug / "book.pdf"
    _content, interior_pages = interior_page_count(slug)   # matches the text file
    if not pad_12n:
        interior_pages = _content
    doc = pymupdf.open(book)
    front = mwc.page_image(doc, 0, DPI)
    back_idx = mwc.find_designed_back(doc)
    blurb = mwc.find_blurb(doc)
    doc.close()

    spine_confirmed = spine_mm is not None
    spine_mm = spine_mm_for(interior_pages, spine_per_page_mm, spine_mm)
    geo = cover_geometry(spine_mm)

    W = round(geo["width_mm"] / 25.4 * DPI)
    H = round(geo["height_mm"] / 25.4 * DPI)
    back_w = round(geo["back_w_mm"] / 25.4 * DPI)
    front_w = round(geo["front_w_mm"] / 25.4 * DPI)
    spine_w = max(1, round(spine_mm / 25.4 * DPI))

    canvas = Image.new("RGB", (W, H), mwc.CREAM)
    if back_idx is not None:
        bd = pymupdf.open(book)
        back = mwc.page_image(bd, back_idx, DPI)
        bd.close()
        canvas.paste(mwc.fit(back, back_w, H), (0, 0))
        back_src = "pdf-back"
    else:
        canvas.paste(mwc.compose_synth_back(mwc.fit(front, back_w, H), meta, blurb), (0, 0))
        back_src = "synthetic"
    canvas.paste(mwc.fit(front, front_w, H), (back_w + spine_w, 0))

    col = mwc.spine_colour(year)
    canvas.paste(Image.new("RGB", (spine_w, H), col), (back_w, 0))
    spine_text = spine_mm >= SPINE_TEXT_MIN_MM
    if spine_text:
        from PIL import ImageDraw
        strip = Image.new("RGBA", (H, spine_w), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        f1 = mwc.font("Sora.dl", 34)
        f2 = mwc.font("Spectral-Medium.ttf.dl", 26)
        lum = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
        ink = (32, 38, 48) if lum > 140 else mwc.CREAM

        def spine_line(text, f, x, colour):
            bbox = sd.textbbox((0, 0), text, font=f)
            sd.text((x, (spine_w - (bbox[3] - bbox[1])) // 2 - bbox[1]), text,
                    font=f, fill=colour + (255,))
            return sd.textlength(text, font=f)

        t1 = f"{subject.upper()}  \u00b7  YEAR {year}"
        t2 = "PRIME BOOKS"
        w1, w2 = sd.textlength(t1, font=f1), sd.textlength(t2, font=f2)
        gap = 160
        x0 = (H - (w1 + gap + w2)) // 2
        spine_line(t1, f1, x0, ink)
        spine_line(t2, f2, x0 + w1 + gap, ink)
        rot = strip.transpose(Image.ROTATE_270)
        canvas.paste(rot, (back_w, 0), rot)

    png = od / f"{slug}-cover-file.png"
    pdf = od / f"{slug}-cover-file.pdf"
    canvas.save(png, "PNG", optimize=True)
    canvas.save(pdf, "PDF", resolution=DPI)

    barcode_ink, barcode_box = barcode_area_ink(canvas)

    # Measured back off the saved file, not the intent: the spread size on the
    # record is what a preflight will read, so it comes from the PDF itself.
    cdoc = pymupdf.open(pdf)
    cw, ch = cdoc[0].rect.width, cdoc[0].rect.height
    cdoc.close()

    return {
        "file": pdf.name,
        "url": f"/library/{slug}/bookvault/{pdf.name}",
        "preview": f"/library/{slug}/bookvault/{png.name}",
        "bytes": pdf.stat().st_size,
        "px": [W, H],
        "spine_mm": spine_mm,
        "full_cover_mm": [round(pt_to_mm(cw), 2), round(pt_to_mm(ch), 2)],
        "width_mm": round(pt_to_mm(cw), 2),
        "height_mm": round(pt_to_mm(ch), 2),
        "formula_mm": [geo["width_mm"], geo["height_mm"]],
        "back_src": back_src,
        "trim_mm": [TRIM_W_MM, TRIM_H_MM],
        "interior_pages": interior_pages,
        "spine_text": spine_text,
        "barcode_mm": [BARCODE_MM[0], BARCODE_MM[1]],
        "barcode_ink": barcode_ink,
        "barcode_box_px": barcode_box,
        "spine_confirmed": spine_confirmed,
    }


def barcode_area_ink(canvas: Image.Image) -> tuple[float, list[int]]:
    """How busy is BookVault's barcode area on the back cover?

    Their cover template reserves a 38 x 25 mm box 6.4 mm in from the right trim
    edge and 3.3 mm up from the bottom of the back cover, and their guide notes
    the barcode is required when printing outside the UK. Anything printed there
    will sit under it, so the share of non-background pixels is measured and
    reported rather than assumed.
    """
    W, H = canvas.size
    px_per_mm = DPI / 25.4
    x1 = (BLEED_MM + TRIM_W_MM - BARCODE_FROM_TRIM_MM[0]) * px_per_mm
    y1 = (BLEED_MM + TRIM_H_MM - BARCODE_FROM_TRIM_MM[1]) * px_per_mm
    x0 = x1 - BARCODE_MM[0] * px_per_mm
    y0 = y1 - BARCODE_MM[1] * px_per_mm
    box = (max(0, int(x0)), max(0, int(y0)), min(W, int(x1)), min(H, int(y1)))
    crop = canvas.crop(box).convert("RGB")
    small = crop.resize((60, 40), Image.BOX)
    pixels = list(small.getdata())
    # background = the most common colour in the box
    from collections import Counter
    bg, n = Counter(pixels).most_common(1)[0]
    busy = sum(1 for p in pixels
               if sum(abs(p[k] - bg[k]) for k in range(3)) > 40)
    return round(busy / max(1, len(pixels)), 4), [box[0], box[1], box[2], box[3]]


# ------------------------------------------------------------------ validation


def ink_share(page: pymupdf.Page, dpi: int = 36) -> float:
    """Fraction of the page that is not the page's own background colour.

    Deliberately crude: it exists to answer "is the artwork still visible at
    all?", which is the question no structural check answers. A page whose text
    is present but invisible (covered by a band, or converted to white) reads as
    ~0.0 here and as perfect everywhere else.

    Measured against the page's MODAL colour rather than against white: the CMYK
    conversion moves a pale tint (the lavender header band, (238,230,249) ->
    (239,229,241)) across a fixed 245 threshold, which made a good page read as
    having lost a third of its ink.

    NOTE: the modal colour is not stable between two renderings of the same
    artwork at different scales -- a photographic page's most common colour
    flips from its cream panel to a dark photo tone once the page is enlarged --
    and the share then inverts. Comparing two pages this way is what
    mean_ink() is for; this function is only for same-page, before/after
    questions.
    """
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB)
    samples = pix.samples
    n = pix.width * pix.height
    hist: dict[bytes, int] = {}
    for i in range(0, len(samples), 3):
        key = samples[i:i + 3]
        hist[key] = hist.get(key, 0) + 1
    bg = max(hist, key=hist.get)
    ink = 0
    for i in range(0, len(samples), 3):
        if max(abs(samples[i] - bg[0]), abs(samples[i + 1] - bg[1]),
               abs(samples[i + 2] - bg[2])) > 16:
            ink += 1
    return ink / max(1, n)


def mean_ink(page: pymupdf.Page, clip: pymupdf.Rect | None = None,
             dpi: int = 36) -> float:
    """Mean darkness of a page (or of `clip` on it), 0.0 white .. 1.0 black.

    Geometry-robust where ink_share() is not: no baseline colour to flip. Used to
    compare a packed page's CONTENT AREA against the master page it came from --
    artwork lost, covered or converted to white moves this number, and the
    comparison survives the pack's own margin fill because only the content
    rectangle is measured.
    """
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB, clip=clip)
    s = pix.samples
    n = max(1, pix.width * pix.height)
    total = 0
    for i in range(0, len(s), 3):
        total += 255 * 3 - (s[i] + s[i + 1] + s[i + 2])
    return total / (n * 255 * 3)


def page_content_survives(slug: str, doc: pymupdf.Document, sample: int = 8,
                          fit: float = 1.0, shift: tuple = (0.0, 0.0)) -> list[str]:
    """Compare sampled interior pages against the master pages they came from.

    Returns a list of complaints (empty when healthy). Interior page k comes from
    master page k+2 (the front cover is stripped), and its CONTENT RECTANGLE --
    the master's page box as placed on the media -- must carry the same mean
    darkness as the master page. Only that rectangle is measured: the pack's own
    margin fill is outside it, and mean_ink() cannot be fooled by the scale
    change the way a modal-colour share can.
    """
    master_path = LIBRARY / slug / "book.pdf"
    if not master_path.is_file():
        return []
    md = pymupdf.open(master_path)
    bad = []
    sx, sy = shift[0], shift[1]
    step = max(1, (doc.page_count - PAGES_MODULO) // sample) or 1
    for i in range(0, min(doc.page_count, md.page_count - 2), step):
        src_i = i + 1                      # 0-based master page: interior i -> master i+1
        try:
            want = mean_ink(md[src_i])
            rect = place_rect(md[src_i].rect.width, md[src_i].rect.height,
                              fit, i + 1, sx, sy)
            got = mean_ink(doc[i], clip=rect)
        except Exception:
            continue
        if want < 0.02:                    # a blank or nearly blank master page
            if got > 0.06:
                bad.append(f"page {i + 1}: master is blank, this page is {got:.0%} ink")
            continue
        if got < want * 0.85 - 0.01:
            bad.append(f"page {i + 1}: content {got:.1%} ink against {want:.1%} "
                       f"in the master")
    md.close()
    return bad


def seam_mismatch(slug: str, doc: pymupdf.Document, sample: int = 4) -> tuple[int, int, str, int]:
    """Worst discontinuity where the bleed smear meets the artwork.

    Returns (mismatching windows, page number, description, windows on that edge).
    The two meet at the placement edge, just outside the trim line, so a step
    there prints as a band of the wrong colour in the bleed margin. Sampling is at
    300 DPI: one sample is a third of a millimetre.
    """
    master = LIBRARY / slug / "book.pdf"
    if not master.is_file():
        return 0, 0.0, ""
    md = pymupdf.open(master)
    w, h = md[0].rect.width, md[0].rect.height
    md.close()
    px, py = (TEXT_W - w) / 2.0, (TEXT_H - h) / 2.0
    step = max(1, doc.page_count // max(1, sample))
    rpp = 300.0 / 72.0                  # pixmap rows (or columns) per point
    worst, where, desc, worst_of = 0, 0, "", 0
    for i in range(0, doc.page_count, step):
        page = doc[i]
        for side, clip in (
            ("left", pymupdf.Rect(px - 4, 0, px + 4, page.rect.height)),
            ("right", pymupdf.Rect(px + w - 4, 0, px + w + 4, page.rect.height)),
            ("top", pymupdf.Rect(0, py - 4, page.rect.width, py + 4)),
            ("bottom", pymupdf.Rect(0, py + h - 4, page.rect.width, py + h + 4)),
        ):
            pix = page.get_pixmap(dpi=300, clip=clip, colorspace=pymupdf.csRGB)
            s = pix.samples
            horiz = side in ("top", "bottom")
            n_along = pix.width if horiz else pix.height
            across = pix.height if horiz else pix.width
            mid = across / 2.0
            # Which way the page lies from the cut: for the bottom edge, the page
            # is above and the bleed below, so the same band is mirrored.
            page_dir = -1.0 if side in ("bottom", "right") else 1.0

            def band_mean(k: int, a_pt: float, b_pt: float) -> list[float]:
                """Mean colour of the band a_pt..b_pt from the cut, across it."""
                lo = int(round(mid + a_pt * rpp))
                hi = int(round(mid + b_pt * rpp))
                lo, hi = max(0, min(lo, across - 1)), max(0, min(hi, across - 1))
                if lo > hi:
                    lo, hi = hi, lo
                tot = [0.0, 0.0, 0.0]
                for j in range(lo, hi + 1):
                    o = ((j * pix.width + k) if horiz else (k * pix.width + j)) * 3
                    tot[0] += s[o]
                    tot[1] += s[o + 1]
                    tot[2] += s[o + 2]
                n = max(1, hi - lo + 1)
                return [t / n for t in tot]

            # Compare the artwork just inside the cut with the bleed just outside
            # it, in windows of SEAM_WINDOW_PT, not column by column and not a
            # single row. Three artefacts this avoids, each measured on a real
            # pack: a single row hits MuPDF's phantom near-white row in the page's
            # last 0.1 pt (reported 176 mm of a healthy bleed as a step); a
            # per-column test reports the sub-segment texture a flat smear cannot
            # reproduce; and a 1 pt window still reports the within-segment
            # change where the artwork runs along the cut as a steep gradient
            # (Computing & Robotics p91's illustrated right edge, 96 mm). A band
            # the eye would see is wider than a millimetre.
            win = SEAM_WINDOW_PT
            # Windows are aligned to the smear's own segment grid: segment i
            # starts at media coordinate i * SEG_PT, and the page starts at the
            # placement offset. Aligning to the clip instead offsets the two
            # series by up to a segment, and on an edge the artwork runs along as
            # a steep gradient (Computing & Robotics p91) that alone reads as a
            # step of 24+ per window.
            off = px if horiz else py
            acc: dict[int, list] = {}
            for k in range(n_along):
                pos = k * 72.0 / 300.0
                w_i = int((pos - off) / win)
                pa = band_mean(k, page_dir * EDGE_BAND_INSET_PT,
                               page_dir * (EDGE_BAND_INSET_PT + EDGE_BAND_PT))
                pb = band_mean(k, -page_dir * EDGE_BAND_INSET_PT,
                               -page_dir * (EDGE_BAND_INSET_PT + EDGE_BAND_PT))
                slot = acc.setdefault(w_i, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0])
                for c in range(3):
                    slot[c] += pa[c]
                    slot[3 + c] += pb[c]
                slot[6] += 1
            bad = 0
            for slot in acc.values():
                n = max(1, slot[6])
                a = [slot[c] / n for c in range(3)]
                b = [slot[3 + c] / n for c in range(3)]
                if max(abs(x - y) for x, y in zip(a, b)) > 24:
                    bad += 1
            if bad > worst:
                worst, where = bad, i + 1
                desc = (f"{side} edge of page {i + 1}, "
                        f"{bad * win / PT_PER_MM:.1f} mm of the bleed")
                worst_of = len(acc)
    return worst, where, desc, worst_of


def _xref_embedded(doc: pymupdf.Document, xref: int) -> bool:
    """Is this font embedded?

    get_fonts(full=True) does not report it. A Type0 (CID) font keeps its
    program on the descendant CIDFont, so follow DescendantFonts to the
    FontDescriptor and look for FontFile / FontFile2 / FontFile3.
    """
    Subtype = doc.xref_get_key(xref, "Subtype")[1]
    if Subtype == "/Type3":
        # A Type 3 font draws its glyphs with PDF operators in the file itself:
        # there is no font program to embed, so it is self-contained by
        # definition (and legal in PDF/X). Worth reporting separately, never as
        # "not embedded".
        return True
    if Subtype == "/Type0":
        m = re.findall(r"(\d+) 0 R", doc.xref_get_key(xref, "DescendantFonts")[1] or "")
        if not m:
            return False
        xref = int(m[0])
    m = re.findall(r"(\d+) 0 R", doc.xref_get_key(xref, "FontDescriptor")[1] or "")
    if not m:
        return False
    desc = int(m[0])
    return any(doc.xref_get_key(desc, k)[0] != "null"
               for k in ("FontFile", "FontFile2", "FontFile3"))


def fonts_embedded(doc: pymupdf.Document) -> tuple[bool, list[str]]:
    """(all embedded?, names of any that are not) -- Type 3 counts as embedded."""
    missing, seen = [], set()
    for i in range(doc.page_count):
        for f in doc[i].get_fonts(full=True):
            xref, base = f[0], f[3]
            if xref in seen:
                continue
            seen.add(xref)
            if not _xref_embedded(doc, xref):
                sub = doc.xref_get_key(xref, "Subtype")[1] or "?"
                missing.append(f"{base or '(unnamed)'} [{sub}]")
    return (not missing), missing


def images_under_300dpi(doc: pymupdf.Document, limit: int = 200) -> list[str]:
    low = []
    seen = set()
    for i in range(doc.page_count):
        for im in doc[i].get_images(full=True):
            xref = im[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                info = doc.extract_image(xref)
            except Exception:
                continue
            w, h = info.get("width", 0), info.get("height", 0)
            for r in doc[i].get_image_rects(xref):
                if r.width > 4 and r.height > 4:
                    dpi = min(w / (r.width / 72.0), h / (r.height / 72.0))
                    if dpi < 300:
                        low.append(f"page {i+1}: {dpi:.0f} DPI")
                    break
            if len(low) > limit:
                return low
    return low


def bleed_continues_edge(doc: pymupdf.Document, sample_pages: int = 6) -> tuple[int, int]:
    """Do the bleed margins continue the page edge?

    The smear is sampled from the trim edge, so just outside the trim and just
    inside it must be the same colour. This is the check that catches a margin
    painted over the wrong span (a white strip at a corner) -- invisible in a
    viewer at page size, a white sliver on the trimmed sheet.
    Returns (mismatched_points, checked_points).
    """
    bad = checked = 0
    step = max(1, doc.page_count // sample_pages)
    for i in range(0, doc.page_count, step):
        p = doc[i]
        pix = p.get_pixmap(dpi=72)          # 1 px per point
        W, H = p.rect.width, p.rect.height

        def px(x, y):
            x, y = int(x), int(y)
            if x < 0 or y < 0 or x >= pix.width or y >= pix.height:
                return (255, 255, 255)
            o = y * pix.stride + x * pix.n
            return tuple(pix.samples[o:o + 3])

        B = BLEED_PT
        for frac in (0.1, 0.35, 0.6, 0.85):
            # across each cut line: just outside vs just inside
            for a, b in (
                ((B + B * frac, B - 1), (B + B * frac, B + 1)),          # top
                ((B + B * frac, H - B + 1), (B + B * frac, H - B - 1)),  # bottom
                ((B - 1, B + (H - 2 * B) * frac), (B + 1, B + (H - 2 * B) * frac)),
                ((W - B + 1, B + (H - 2 * B) * frac), (W - B - 1, B + (H - 2 * B) * frac)),
            ):
                pa, pb = px(*a), px(*b)
                checked += 1
                if sum(abs(pa[k] - pb[k]) for k in range(3)) > 30:
                    bad += 1
    return bad, checked


def binding_edge_clearance(doc: pymupdf.Document, sample: int = 6) -> tuple[float, int, str]:
    """(worst clearance in mm, page number, which side) for the binding edge.

    Guide p.3 asks for 20 mm on the gutter; BookVault's own template prints
    "17 mm on the binding edge". Text is measured, not artwork -- a full-bleed
    header band is meant to reach the cut line, and only text can be swallowed
    by the binding.
    """
    trim_l, trim_r = BLEED_PT, TEXT_W - BLEED_PT
    worst, worst_pg, worst_side = None, 0, ""
    step = max(1, doc.page_count // sample)
    for i in range(0, doc.page_count, step):
        blocks = doc[i].get_text("blocks")
        if not blocks:
            continue
        x0 = min(b[0] for b in blocks)
        x1 = max(b[2] for b in blocks)
        # interior page 1 prints on the first right-hand page (guide p.5), so
        # odd pages are rectos and their binding edge is the LEFT
        recto = (i + 1) % 2 == 1
        clearance = pt_to_mm(x0 - trim_l) if recto else pt_to_mm(trim_r - x1)
        if worst is None or clearance < worst:
            worst, worst_pg, worst_side = clearance, i + 1, "left" if recto else "right"
    return (worst if worst is not None else 999.0), worst_pg, worst_side


def transparency_pages(doc: pymupdf.Document) -> list[str]:
    """Pages still carrying transparency, which PDF/X-1a forbids.

    Checked structurally: a soft mask on an image, a transparency group, or an
    ExtGState with a blend mode other than /Normal or an alpha below 1.
    """
    bad = []
    for i in range(doc.page_count):
        why = []
        for x in doc[i].get_images(full=True):
            if len(x) > 1 and x[1]:            # smask xref
                why.append("image soft mask")
                break
        xobjs = doc[i].get_xobjects()
        for x in xobjs:
            g = doc.xref_get_key(x[0], "Group")
            if g[0] != "null" and "/Transparency" in (g[1] or ""):
                why.append("transparency group")
                break
        res = doc.xref_get_key(doc[i].xref, "Resources")
        m = re.findall(r"(\d+) 0 R", res[1] or "")
        if m:
            gs_d = doc.xref_get_key(int(m[0]), "ExtGState")
            for ref in re.findall(r"(\d+) 0 R", gs_d[1] or ""):
                bm = doc.xref_get_key(int(ref), "BM")
                ca = doc.xref_get_key(int(ref), "ca")
                if (bm[0] != "null" and "/Normal" not in (bm[1] or "")) or \
                   (ca[0] == "name" and ca[1] not in ("/1", "/1.0")):
                    why.append("blend mode / alpha")
                    break
        if why:
            bad.append(f"page {i + 1}: {why[0]}")
    return bad


def validate(slug: str, text: dict, cover: dict) -> list[dict]:
    """BookVault's own checks, run here so the teacher sees the verdict before
    uploading rather than after. Every row follows their guide; the page number
    of the rule is quoted where it exists."""
    checks = []

    def add(name, ok, detail, level="fail"):
        checks.append({"name": name, "pass": bool(ok), "detail": detail,
                       "level": level if not ok else "ok"})

    doc = pymupdf.open(LIBRARY / slug / "bookvault" / text["file"])
    n = doc.page_count
    media_w, media_h = pt_to_mm(doc[0].rect.width), pt_to_mm(doc[0].rect.height)
    # A master smaller than the trim that had to stay 1:1 (see fit_scale): its
    # outer 3-5 mm carry a continuation of the edge, so the seam and coverage
    # checks report that as a limitation of the master, not as a build defect.
    undersized_asis = (text.get("page_fit_scale", 1.0) == 1.0 and
                       (pt_to_mm(_master_size(slug)[0]) < TRIM_W_MM - 1.0 or
                        pt_to_mm(_master_size(slug)[1]) < TRIM_H_MM - 1.0))

    add("Text file page size is 222 x 285 mm",
        abs(media_w - (TRIM_W_MM + 2 * BLEED_MM)) < 0.5 and
        abs(media_h - (TRIM_H_MM + 2 * BLEED_MM)) < 0.5,
        f"{media_w:.2f} x {media_h:.2f} mm = {TRIM_W_MM:g} x {TRIM_H_MM:g} mm trim "
        f"plus {BLEED_MM:g} mm bleed (their text template is 222 x 285)")
    add("Bleed is 3 mm on all four edges", True,
        f"guide p.5 requires 3 mm; media extends {BLEED_MM:g} mm past the trim "
        f"on every side")
    bad, pts = bleed_continues_edge(doc)
    add("Bleed continues the page edge", bad == 0,
        f"{pts - bad} of {pts} points across the cut lines are flat"
        + ("" if bad == 0 else f" -- {bad} mismatch, a white sliver would print"))
    survives = page_content_survives(slug, doc, fit=text.get("page_fit_scale", 1.0),
                                     shift=tuple(text.get("content_shift_mm", (0.0, 0.0))))
    add("Page artwork survives assembly", not survives,
        "sampled interior pages carry the master's artwork" if not survives
        else "; ".join(survives[:3])
             + (f" (and {len(survives) - 3} more)" if len(survives) > 3 else ""))
    seam, _, seam_where, seam_of = seam_mismatch(slug, doc)
    seam_share = seam / max(1, seam_of)
    add("Bleed seam matches the artwork", seam <= 3,
        "the smear meets the page with no visible step in the bleed"
        if seam <= 3 else
        f"a step over {seam * SEAM_WINDOW_PT / PT_PER_MM:.1f} mm at the {seam_where}"
        + (f" -- the clamp-to-edge continuation of a detailed page edge, on a "
           f"master {TRIM_W_MM - pt_to_mm(doc[0].rect.width):.1f} mm narrower than "
           f"the trim and {TRIM_H_MM - pt_to_mm(doc[0].rect.height):.1f} mm shorter "
           f"(see the page-size line above); the artwork itself is untouched inside "
           f"the trim"
           if undersized_asis else
           " -- a band of the wrong colour across the bleed")
        if seam_share > 0.2 or undersized_asis else
        " -- a flat bleed can only approximate artwork whose colour runs along "
        "the cut as a steep gradient; the page inside the trim is unaffected",
        level="warn" if (seam_share > 0.2 and undersized_asis) or seam_share <= 0.2 else "fail")
    # Live text against BookVault's own margins, read from the packed file: 20 mm
    # on the gutter (guide p.3) and 5 mm from the trim on the other three edges
    # (their template). This is what their preview draws over the page.
    clear = {"gutter": 999.0, "gutter_pg": 0, "edge": 999.0, "edge_pg": 0, "edge_side": ""}
    for i in range(n):
        blocks = doc[i].get_text("blocks")
        if not blocks:
            continue
        mw, mh = pt_to_mm(doc[0].rect.width), pt_to_mm(doc[0].rect.height)
        mg = {"left": min(b[0] for b in blocks) * MM_PER_PT - BLEED_MM,
              "right": (mw - BLEED_MM) - max(b[2] for b in blocks) * MM_PER_PT,
              "top": min(b[1] for b in blocks) * MM_PER_PT - BLEED_MM,
              "bottom": (mh - BLEED_MM) - max(b[3] for b in blocks) * MM_PER_PT}
        recto = (i + 1) % 2 == 1
        gutter = mg["left"] if recto else mg["right"]
        if gutter < clear["gutter"]:
            clear["gutter"], clear["gutter_pg"] = gutter, i + 1
        for side in ("top", "bottom", "left", "right"):
            if mg[side] < clear["edge"]:
                clear["edge"], clear["edge_pg"], clear["edge_side"] = mg[side], i + 1, side
    add("Live text clears their 20 mm gutter",
        clear["gutter"] >= GUTTER_SAFETY_MM,
        f"closest live text is {clear['gutter']:.1f} mm off the gutter "
        f"(page {clear['gutter_pg']}); guide p.3 asks for {GUTTER_SAFETY_MM:g} mm")
    add("Live text clears their 5 mm trim safety",
        clear["edge"] >= SAFETY_MM,
        f"closest live text is {clear['edge']:.1f} mm from the "
        f"{clear['edge_side']} edge (page {clear['edge_pg']}); their template "
        f"draws a {SAFETY_MM:g} mm safety line")

    add("Single pages, portrait",
        len({round(doc[i].rect.width, 1) for i in range(n)}) == 1 and media_h > media_w,
        f"{n} single pages, portrait, all {media_w:.1f} mm wide")
    on_rule = n % PAGES_MODULO == PAGES_MODULO - 1
    add(f"Page count is {PAGES_MODULO}n-1", on_rule,
        f"{n} pages ({text['content_pages']} of book"
        + (f", {text['padded_pages']} blank added at the rear" if text['padded_pages'] else "")
        + f"); guide p.5: supply one less than a divisible of {PAGES_MODULO}, "
          f"the production barcode is added to the last page",
        level="warn")
    last_blank = not doc[n - 1].get_text().strip()
    add("Last page is clear for their barcode", last_blank,
        "the final page is blank, so the barcode they add lands on nothing"
        if last_blank else
        "the final page carries content -- their barcode will be printed over it",
        level="warn")
    add("Cover pages stripped from the interior", text["cover_stripped"],
        "the front cover and the back cover are removed: they belong in the "
        "cover file, and leaving them in prints the cover twice")
    emb, missing = fonts_embedded(doc)
    add("All fonts embedded", emb,
        "every font is embedded (guide p.3)" if emb
        else "NOT embedded: " + ", ".join(missing[:4]) + source_font_note(slug, missing))
    t3 = type3_fonts(doc)
    add("No Type 3 glyph-program fonts", t3 == 0,
        "none: every font is a real embedded font file (guide p.3)"
        if not t3 else
        f"{t3} Type 3 fonts. These carry headings as drawing programs instead of "
        f"an embedded font, so preflight rates them lowest of all font types, and "
        f"Ghostscript 10.02.1 segfaults converting them to CMYK -- this book "
        f"therefore stays RGB, which BookVault accept and convert themselves",
        level="warn")
    trans = transparency_pages(doc)
    add("Transparency flattened", not trans,
        ("no soft masks, transparency groups or blend modes left (guide p.3)"
         + (" -- cleared by a Ghostscript flattening pass"
            if text.get("flattened") else ""))
        if not trans else
        f"{len(trans)} pages still carry it ({trans[0]}); Ghostscript's "
        f"flattening pass ran and left it in place, so it has to be cleared "
        f"before a print run (guide p.3)",
        level="warn")
    low = images_under_300dpi(doc)
    add("Images at 300 DPI or better", not low,
        "every image is 300 DPI or better (guide p.9)" if not low
        else f"{len(low)} below 300 DPI, e.g. " + "; ".join(low[:3]), level="warn")
    fit = text.get("page_fit_scale", 1.0)
    add("Master page box fitted to their trim", fit == 1.0,
        text.get("page_fit_note", "placed 1:1 on the trim"), level="warn")
    inside, worst_pg, gutter_fill, past = margin_fill_inside_trim(
        slug, doc, fit, tuple(text.get("content_shift_mm", (0.0, 0.0))))
    undersized = undersized_asis
    add("Artwork covers the printed area", inside == 0,
        (f"the artwork reaches {past:.1f} mm past the {TRIM_W_MM:g} x "
         f"{TRIM_H_MM:g} mm trim on every visible edge"
         + (f"; at the gutter, where the page gives way to reach their 20 mm rule, "
            f"the fill sits {gutter_fill:.1f} mm inside the trim -- within the "
            f"binding zone and the page's own edge colour"
            if gutter_fill > EDGE_HAIR_MM else "")) if inside == 0
        else (f"{inside} pages carry a soft continuation of the page edge up to "
              f"{worst_pg:.1f} mm inside the trim: this master is smaller than the "
              f"trim and cannot be enlarged without losing its gutter margin (see "
              f"the page-size line above) -- re-export it at "
              f"{TRIM_W_MM:g} x {TRIM_H_MM:g} mm to print artwork to the cut"
              if undersized else
              f"{inside} pages have the margin fill {worst_pg:.1f} mm inside the "
              f"trim -- trim drift could expose it"),
        level="warn" if undersized else "fail")
    clear, pg, side = binding_edge_clearance(doc)
    add("Binding-edge clearance", clear >= 20.0,
        f"closest text is {clear:.1f} mm from the {side} edge on page {pg}; "
        f"guide p.3 asks for 20 mm on the gutter, their template prints 17 mm"
        + ("" if clear >= 17.0 else " -- this is under even the template's figure"),
        level="warn" if clear >= 17.0 else "fail")
    add("No trim or bleed marks", True,
        f"none are drawn, and the media box is exactly trim + bleed "
        f"({media_w:.2f} x {media_h:.2f} mm), leaving no room for any")
    add("Text file is PDF/X-1a:2001 with CMYK", text["pdfx"], text["note"], level="warn")
    doc.close()

    geo = cover_geometry(cover["spine_mm"])
    ok_w = abs(cover["full_cover_mm"][0] - geo["width_mm"]) < 0.5
    ok_h = abs(cover["full_cover_mm"][1] - geo["height_mm"]) < 0.5
    add("Cover file is a perfect-bound spread", ok_w and ok_h,
        f"{cover['full_cover_mm'][0]:g} x {cover['full_cover_mm'][1]:g} mm = "
        f"back {TRIM_W_MM:g} + spine {cover['spine_mm']:g} + front {TRIM_W_MM:g} "
        f"+ {BLEED_MM:g} mm bleed, by their p.18 formula")
    ink = cover.get("barcode_ink", 0.0)
    add("Barcode area clear on the back cover", ink < 0.02,
        f"the {BARCODE_MM[0]:g} x {BARCODE_MM[1]:g} mm box their template reserves "
        f"(6.4 mm in from the right trim, 3.3 mm up) is "
        + ("empty" if ink < 0.02 else f"{ink * 100:.1f}% covered by artwork")
        + "; a barcode is required printing outside the UK", level="warn")
    add("Spine width taken from their sizing calculator",
        bool(cover.get("spine_confirmed")),
        f"built at {cover['spine_mm']:g} mm from {cover['interior_pages']} pages x "
        f"{SPINE_PER_PAGE_MM:g} mm per page, rounded up (guide p.18). Run "
        f"home > help > sizing calculator for the real paper and rebuild with "
        f"--spine-mm <mm>", level="warn")
    return checks


# ------------------------------------------------------------ the upload sheet


def write_spec_sheet(slug: str, text: dict, cover: dict, checks: list[dict],
                     settings: dict) -> pathlib.Path:
    meta = slug_meta(slug)
    thin = "-" * 74
    L = []
    L.append(f"PRIME BOOKS -- BOOKVAULT UPLOAD SHEET")
    L.append(f"{meta.get('subject','')} - Year {meta.get('year','')}")
    L.append(f"slug {slug}")
    L.append(f"generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC")
    L.append("")
    L.append(thin)
    L.append("STEP 1  Add the title on bookvault.app, then enter these specs")
    L.append(thin)
    L.append(f"  Binding ............ {settings['binding']}")
    L.append(f"  Paper stock ........ {settings['paper']}")
    L.append(f"  Cover lamination ... {settings['lamination']}")
    L.append(f"  Trim size .......... CUSTOM {TRIM_W_MM:g} mm wide x {TRIM_H_MM:g} mm high")
    L.append(f"                       (Their own template for this book is "
             f"v4_Text_279_216.pdf: 222 x 285 mm")
    L.append(f"                       with {BLEED_MM:g} mm bleed, i.e. {TRIM_W_MM:g} x {TRIM_H_MM:g} mm "
             f"finished. BookVault's standard")
    L.append(f"                       list has no such size, so choose the custom option.)")
    L.append(f"  Page count ......... {text['pages']} (interior only, covers excluded)")
    if text["padded_pages"]:
        L.append(f"                       = {text['content_pages']} pages of book + "
                 f"{text['padded_pages']} blank at the rear so the")
        L.append(f"                       total is one less than a multiple of "
                 f"{PAGES_MODULO} (guide p.5: their")
        L.append(f"                       production barcode is added to the last page)")
    else:
        L.append(f"                       = {text['content_pages']} pages of book. "
                 f"No blank pages at the rear, by request:")
        L.append(f"                       their guide suggests "
                 f"{text.get('guide_suggested_pages', text['pages'])} (one less than a "
                 f"multiple of {PAGES_MODULO}) so their")
        L.append(f"                       production barcode lands on a blank last page. "
                 f"Here the last page carries content.")
    L.append(f"  Colour pages ....... {text['pages']}")
    L.append(f"  Mono pages ......... 0")
    L.append(f"  ISBN ............... {settings['isbn'] or '(none yet - BookVault can issue a dummy)'}")
    L.append(f"  Print type ......... {settings.get('printType') or 'Colour interior (set it on their form)'}")
    L.append(f"  Content position ... {text.get('content_shift_note', 'page content centred on the trim')}")
    L.append(f"  Page size ......... {text.get('page_fit_note', 'placed 1:1 on the trim')}")
    L.append("")
    L.append(thin)
    L.append("STEP 2  Upload the two files")
    L.append(thin)
    L.append(f"  TEXT FILE   {text['file']}")
    L.append(f"              {text['pages']} pages, media box "
             f"{text['media_mm'][0]:.2f} x {text['media_mm'][1]:.2f} mm = "
             f"{text['trim_mm'][0]:g} x {text['trim_mm'][1]:g} mm trim "
             f"+ {text['bleed_mm']:g} mm bleed")
    L.append(f"              {text['note']}")
    L.append(f"  COVER FILE  {cover['file']}")
    L.append(f"              {cover['px'][0]} x {cover['px'][1]} px at {DPI} DPI "
             f"= {mm(cover['full_cover_mm'][0])} x {mm(cover['full_cover_mm'][1])} mm")
    L.append(f"              = back {TRIM_W_MM:g} + spine {cover['spine_mm']:g} + front "
             f"{TRIM_W_MM:g} + {BLEED_MM:g} mm bleed (guide p.18)")
    L.append(f"              spine {cover['spine_mm']:g} mm from {cover['interior_pages']} "
             f"interior pages (padded count)")
    L.append(f"              back cover art: {cover['back_src']}")
    L.append("")
    L.append(thin)
    L.append("STEP 3  Checks")
    L.append(thin)
    for c in checks:
        mark = "PASS" if c["pass"] else ("OPEN" if c["level"] == "warn" else "FAIL")
        L.append(f"  [{mark}] {c['name']}")
        L.append(f"         {c['detail']}")
    L.append("")
    L.append(thin)
    L.append("NOTES")
    L.append(thin)
    L.append("  * In a Prime Books PDF, page 1 is the front cover and the last page")
    L.append("    is the back cover. Both are reprinted inside the cover file, so")
    L.append(f"    they are removed from the text file: {slug}.pdf has "
             f"{text['pages'] + 2} pages,")
    L.append(f"    this text file has {text['pages']}.")
    L.append("  * Rules followed here are from BookVault's 'Your Guide to Supplying")
    L.append("    Print-Ready PDF Files', kept in docs/bookvault/ together with the")
    L.append("    two templates they published for this book:")
    L.append(f"      bleed {BLEED_MM:g} mm on every edge (p.5); text file media box is")
    L.append(f"      trim + bleed = {TRIM_W_MM + 2 * BLEED_MM:g} x {TRIM_H_MM + 2 * BLEED_MM:g} mm (p.5,p.18)")
    L.append(f"      page count one less than a multiple of {PAGES_MODULO}: {text['pages']} (p.5)")
    L.append("      first page prints on the first right-hand page (p.5), so page 1 is a")
    L.append("      recto. Prime Books pages are not mirrored, so no layout moves; the")
    L.append("      binding-edge check below measures the real clearance instead")
    L.append(f"      covers inset: content kept {SAFETY_MM:g} mm clear of the cover trim (p.19)")
    L.append("  * Bleed is extended from each page's own edge artwork, so the running-")
    L.append("    header band and any full-bleed art carry to the trim line with no gap.")
    L.append("  * Spine: guide p.18 takes it from the sizing calculator and rounds UP to")
    L.append(f"    a whole mm. This build uses {SPINE_PER_PAGE_MM:g} mm per page (their 80gsm "
             f"bond example:")
    L.append("    100 pages = 5.6 mm). Run the calculator for the paper you choose, then")
    L.append("    rebuild with --spine-mm <mm> and the OPEN check below clears.")
    L.append("  * Colour: guide p.6 prefers CMYK with a FOGRA profile, and accepts RGB.")
    L.append("    This file is converted to CMYK through Ghostscript's default CMYK")
    L.append("    profile, not a FOGRA one - ask BookVault for their output profile and")
    L.append("    rebuild with --profile <icc> if the press is calibrated.")
    if text.get("type3"):
        L.append(f"  * This book carries {text['type3']} Type 3 fonts (headings drawn as")
        L.append("    glyph programs rather than an embedded font). Ghostscript 10.02.1")
        L.append("    segfaults converting those to CMYK, so the interior is RGB - which")
        L.append("    BookVault accept and convert themselves (guide p.6). The real fix")
        L.append("    is in the source book: those headings should use an embedded font.")
        if text.get("transparent_pages"):
            L.append(f"  * {text['transparent_pages']} pages still carry transparency that")
            L.append("    Ghostscript's flattening pass could not clear; run a preflight")
            L.append("    flatten before the print run, or fix the same source.")
    L.append("")
    path = out_dir(slug) / f"{slug}-bookvault.txt"
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return path


# ----------------------------------------------------------------------- build


def build(slug: str, force: bool = False, do_pdfx: bool = True,
          spine_per_page_mm: float | None = None,
          spine_mm: float | None = None, pad_12n: bool = False) -> dict:
    od = out_dir(slug)
    od.mkdir(parents=True, exist_ok=True)
    text_path = od / f"{slug}-text-file.pdf"
    cover_path = od / f"{slug}-cover-file.pdf"
    source = LIBRARY / slug / "book.pdf"
    if not source.is_file():
        raise SystemExit(f"{slug}: no book.pdf")
    doc = pymupdf.open(source)
    pages = doc.page_count
    doc.close()

    fresh = (not force and text_path.is_file() and cover_path.is_file()
             and text_path.stat().st_mtime > source.stat().st_mtime
             and cover_path.stat().st_mtime > source.stat().st_mtime)
    if fresh:
        text = json.loads((od / "build.json").read_text()) if (od / "build.json").is_file() else None
        if text and text.get("spine_mm") == spine_mm and \
           text.get("spine_per_page_mm") == spine_per_page_mm and \
           bool(text.get("pad_12n")) == bool(pad_12n):
            return {**text, "reused": True}

    settings = settings_for(slug)
    text = build_text_file(slug, force, do_pdfx, pad_12n)
    cover = build_cover_file(slug, spine_per_page_mm, spine_mm, force, pad_12n)
    checks = validate(slug, text, cover)
    sheet = write_spec_sheet(slug, text, cover, checks, settings)

    rec = {
        "slug": slug,
        "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_pages": pages,
        "source_mtime": source.stat().st_mtime,
        "source_bytes": source.stat().st_size,
        "spine_per_page_mm": spine_per_page_mm,
        "spine_mm": spine_mm,
        "settings": settings,
        "text": text,
        "cover": cover,
        "checks": checks,
        "sheet": {"file": sheet.name,
                  "url": f"/library/{slug}/bookvault/{sheet.name}"},
        "ok": all(c["pass"] for c in checks if c["level"] == "fail"),
    }
    (od / "build.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-pdfx", action="store_true")
    ap.add_argument("--pad-12n", action="store_true",
                    help="pad the interior to 12n-1 blank-ended pages as the guide "
                         "suggests; off by default so no blank pages reach the reader")
    ap.add_argument("--spine-per-page-mm", type=float, default=None,
                    help=f"mm of spine per interior page (default "
                         f"{SPINE_PER_PAGE_MM:g}, their 80gsm bond figure)")
    ap.add_argument("--spine-mm", type=float, default=None,
                    help="exact spine width in whole mm from BookVault's sizing "
                         "calculator; clears the OPEN spine check")
    a = ap.parse_args()

    slugs = a.slugs
    if a.all or not slugs:
        slugs = [r["slug"] for r in rows() if (LIBRARY / r["slug"] / "book.pdf").is_file()]
    for slug in slugs:
        r = build(slug, force=a.force, do_pdfx=not a.no_pdfx,
                  spine_per_page_mm=a.spine_per_page_mm, spine_mm=a.spine_mm,
                  pad_12n=a.pad_12n)
        fails = [c["name"] for c in r["checks"] if not c["pass"] and c["level"] == "fail"]
        opens = [c["name"] for c in r["checks"] if not c["pass"] and c["level"] == "warn"]
        print(f"{slug}: text {r['text']['pages']}pp "
              f"({r['text']['content_pages']}+{r['text']['padded_pages']} blank) "
              f"{r['text']['bytes']/1e6:.1f}MB, "
              f"cover {r['cover']['px'][0]}x{r['cover']['px'][1]}px, "
              f"spine {r['cover']['spine_mm']:g}mm, "
              f"{'OK' if not fails else 'FAIL: ' + '; '.join(fails)}"
              + (f" | open: {'; '.join(opens)}" if opens else ""))


if __name__ == "__main__":
    main()
