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
                at_pt: float, steps: int) -> list[tuple[int, int, int]]:
    """Average the page's outermost sliver into `steps` colour samples.

    Averaging is done by PIL's BOX resize (C speed). Hand-rolling the loop in
    Python made this 60x slower and is why protos took minutes per book.
    """
    if horizontal:
        clip = pymupdf.Rect(0, at_pt, length_pt, at_pt + 1.0)
    else:
        clip = pymupdf.Rect(at_pt, 0, at_pt + 1.0, length_pt)
    pix = page.get_pixmap(clip=clip, dpi=SEG_DPI)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if not horizontal:
        im = im.transpose(Image.ROTATE_90)   # scan along the edge, not across
    im = im.resize((max(1, steps), 1), Image.BOX)
    return [tuple(im.getpixel((x, 0)))[:3] for x in range(im.width)]


def smear_columns(page: pymupdf.Page, horizontal: bool, offset_pt: float,
                  src_len_pt: float, media_len_pt: float, at_pt: float,
                  steps_pt: float) -> list[tuple[int, int, int]]:
    """Edge colours mapped into MEDIA coordinates, with the ends clamped.

    The page sits 1:1 inside a slightly larger media box, so media row r shows
    source row r - offset_pt. The smear has to follow that mapping: sampling the
    edge in the page's own coordinates and stretching the result across the
    margin shifts every abrupt edge in the artwork (a rule, a band bottom) by the
    offset, and the seam then shows a band of the wrong colour. Ends clamp to the
    first/last edge sample, which is what a bleed smear does at a corner.
    """
    n_media = max(1, int(round(media_len_pt / steps_pt)))
    n_src = max(1, int(round(src_len_pt / steps_pt)))
    cols = sample_edge(page, horizontal, src_len_pt, at_pt, n_src)
    first, last = cols[0], cols[-1]
    out = []
    for i in range(n_media):
        # the media segment's CENTRE mapped into source space, then the sample
        # that contains it: floor, not round -- rounding picks the neighbouring
        # sample half the time and puts a 1 pt step at every abrupt edge.
        j = int((i + 0.5) * steps_pt - offset_pt)
        out.append(first if j < 0 else last if j >= n_src else cols[j])
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


def bleed_page(dst: pymupdf.Document, src: pymupdf.Document, idx: int) -> None:
    """One interior page onto BookVault's text-file media, 222 x 285 mm.

    The master is 612 x 792 pt (US Letter); BookVault's trim is 216 x 279 mm,
    which is 612.28 x 790.87 pt. Rather than rescale the page -- and with it
    every type size in the book -- the page is placed 1:1 centred on the trim
    box and the leftover margin is filled with the edge smear, so the artwork
    still reaches the cut line on all four sides.
    """
    p = src[idx]
    w, h = p.rect.width, p.rect.height
    page = dst.new_page(width=TEXT_W, height=TEXT_H)

    # centred on the trim box, 1:1 (vector -- text stays text, no rescaling)
    px, py = (TEXT_W - w) / 2.0, (TEXT_H - h) / 2.0
    page.show_pdf_page(pymupdf.Rect(px, py, px + w, py + h), src, idx)

    top = smear_columns(p, True, px, w, TEXT_W, 0.25, SEG_PT)
    bot = smear_columns(p, True, px, w, TEXT_W, h - 1.25, SEG_PT)
    lef = smear_columns(p, False, py, h, TEXT_H, 0.25, SEG_PT)
    rig = smear_columns(p, False, py, h, TEXT_H, w - 1.25, SEG_PT)

    # each margin is painted to its own extent: the placement is centred, so
    # the top and bottom strips are not the same thickness as the sides.
    # ARGUMENT ORDER IS (extent, thickness, start) -- swapping the last two
    # paints a page-sized band over the artwork (white interiors, caught by
    # page_content_survives()).
    draw_runs(page, top, "v", TEXT_W, py, 0)
    draw_runs(page, bot, "v", TEXT_W, TEXT_H - (py + h), py + h)
    draw_runs(page, lef, "h", TEXT_H, px, 0)
    draw_runs(page, rig, "h", TEXT_H, TEXT_W - (px + w), px + w)

    # corners: filled with the corner colour so no white pinhole survives
    for col, rect in (
        (top[0] if top else lef[0], pymupdf.Rect(0, 0, px, py)),
        (top[-1] if top else rig[0], pymupdf.Rect(px + w, 0, TEXT_W, py)),
        (bot[0] if bot else lef[-1], pymupdf.Rect(0, py + h, px, TEXT_H)),
        (bot[-1] if bot else rig[-1], pymupdf.Rect(px + w, py + h, TEXT_W, TEXT_H)),
    ):
        page.draw_rect(rect, color=None, fill=rgb01(col), width=0)


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


def build_text_file(slug: str, force: bool, do_pdfx: bool) -> dict:
    src_path = LIBRARY / slug / "book.pdf"
    od = out_dir(slug)
    od.mkdir(parents=True, exist_ok=True)
    final = od / f"{slug}-text-file.pdf"

    src = pymupdf.open(src_path)
    n = src.page_count
    if n < 4:
        src.close()
        raise SystemExit(f"{slug}: only {n} pages -- not a book")

    content, padded = interior_page_count(slug)

    stripped_cover = True
    work = pymupdf.open()
    for i in range(1, n - 1):          # page 1 (cover) and last (back cover) out
        bleed_page(work, src, i)
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
        "pages_rule": f"12n-1 ({PAGES_MODULO} x {doc.page_count // PAGES_MODULO + (1 if doc.page_count % PAGES_MODULO else 0)} - 1)",
        "trim_mm": [TRIM_W_MM, TRIM_H_MM],
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
                     force: bool) -> dict:
    od = out_dir(slug)
    od.mkdir(parents=True, exist_ok=True)
    meta = slug_meta(slug)
    year = int(meta["year"])
    subject = meta["subject"]

    book = LIBRARY / slug / "book.pdf"
    _content, interior_pages = interior_page_count(slug)   # padded: matches the text file
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
    """Fraction of the page that is not near-white (0.0 - 1.0).

    Deliberately crude: it exists to answer "is the artwork still visible at
    all?", which is the question no structural check answers. A page whose text
    is present but invisible (covered by a band, or converted to white) reads as
    ~0.0 here and as perfect everywhere else.
    """
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB)
    samples = pix.samples
    n = pix.width * pix.height
    white = 0
    for i in range(0, len(samples), 3):
        if samples[i] > 245 and samples[i + 1] > 245 and samples[i + 2] > 245:
            white += 1
    return 1.0 - white / max(1, n)


def page_content_survives(slug: str, doc: pymupdf.Document, sample: int = 8) -> list[str]:
    """Compare sampled interior pages against the master pages they came from.

    Returns a list of complaints (empty when healthy). The interior page k is
    master page k+2 (the front cover is stripped), and its ink share should be at
    least the master's minus what the trim does to it -- a little slack is given
    for the 3 mm bleed and the centred placement.
    """
    master_path = LIBRARY / slug / "book.pdf"
    if not master_path.is_file():
        return []
    md = pymupdf.open(master_path)
    bad = []
    step = max(1, (doc.page_count - PAGES_MODULO) // sample) or 1
    for i in range(0, min(doc.page_count, md.page_count - 2), step):
        src_i = i + 1                      # 0-based master page: interior i -> master i+1
        try:
            want = ink_share(md[src_i])
            got = ink_share(doc[i])
        except Exception:
            continue
        if want < 0.02:                    # a blank or nearly blank master page
            if got > 0.05:
                bad.append(f"page {i + 1}: master is blank, this page is {got:.0%} ink")
            continue
        if got < want * 0.8:
            bad.append(f"page {i + 1}: {got:.1%} ink against {want:.1%} in the master")
    md.close()
    return bad


def seam_mismatch(slug: str, doc: pymupdf.Document, sample: int = 4) -> tuple[int, float, str]:
    """Worst discontinuity where the bleed smear meets the artwork.

    Returns (mismatching samples, page number, description). The two meet at the
    placement edge, just outside the trim line, so a step there prints as a band
    of the wrong colour in the bleed margin. Sampling is at 300 DPI: one sample
    is a third of a millimetre.
    """
    master = LIBRARY / slug / "book.pdf"
    if not master.is_file():
        return 0, 0.0, ""
    md = pymupdf.open(master)
    w, h = md[0].rect.width, md[0].rect.height
    md.close()
    px, py = (TEXT_W - w) / 2.0, (TEXT_H - h) / 2.0
    step = max(1, doc.page_count // max(1, sample))
    worst, where, desc = 0, 0, ""
    for i in range(0, doc.page_count, step):
        page = doc[i]
        for side, clip in (
            ("left", pymupdf.Rect(px - 3, 0, px + 3, page.rect.height)),
            ("right", pymupdf.Rect(px + w - 3, 0, px + w + 3, page.rect.height)),
            ("top", pymupdf.Rect(0, py - 3, page.rect.width, py + 3)),
            ("bottom", pymupdf.Rect(0, py + h - 3, page.rect.width, py + h + 3)),
        ):
            pix = page.get_pixmap(dpi=300, clip=clip, colorspace=pymupdf.csRGB)
            s, n3 = pix.samples, pix.width * 3
            mid = pix.width // 2
            mrow = pix.height // 2          # top/bottom clips are 6 pt tall
            rows = pix.height if side in ("left", "right") else pix.width
            bad = 0
            for k in range(rows):
                if side in ("left", "right"):
                    a = s[k * n3 + (mid - 2) * 3: k * n3 + (mid - 2) * 3 + 3]
                    b = s[k * n3 + (mid + 2) * 3: k * n3 + (mid + 2) * 3 + 3]
                else:
                    x = k
                    a = s[(mrow - 2) * n3 + x * 3: (mrow - 2) * n3 + x * 3 + 3]
                    b = s[(mrow + 2) * n3 + x * 3: (mrow + 2) * n3 + x * 3 + 3]
                if max(abs(x - y) for x, y in zip(a, b)) > 24:
                    bad += 1
            if bad > worst:
                worst, where = bad, i + 1
                desc = f"{side} edge of page {i + 1}, {bad / 300 * 25.4:.1f} mm of the bleed"
    return worst, where, desc


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
    survives = page_content_survives(slug, doc)
    add("Page artwork survives assembly", not survives,
        "sampled interior pages carry the master's artwork" if not survives
        else "; ".join(survives[:3])
             + (f" (and {len(survives) - 3} more)" if len(survives) > 3 else ""))
    seam, _, seam_where = seam_mismatch(slug, doc)
    add("Bleed seam matches the artwork", seam <= 8,
        "the smear meets the page with no visible step in the bleed"
        if seam <= 8 else
        f"a step of {seam / 300 * 25.4:.1f} mm at the {seam_where} -- it sits in "
        f"the bleed margin, but it should be flat")
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
        else "NOT embedded: " + ", ".join(missing[:4]))
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
    L.append(f"  Colour pages ....... {text['pages']}")
    L.append(f"  Mono pages ......... 0")
    L.append(f"  ISBN ............... {settings['isbn'] or '(none yet - BookVault can issue a dummy)'}")
    L.append(f"  Print type ......... {settings.get('printType') or 'Colour interior (set it on their form)'}")
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
          spine_mm: float | None = None) -> dict:
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
           text.get("spine_per_page_mm") == spine_per_page_mm:
            return {**text, "reused": True}

    settings = settings_for(slug)
    text = build_text_file(slug, force, do_pdfx)
    cover = build_cover_file(slug, spine_per_page_mm, spine_mm, force)
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
                  spine_per_page_mm=a.spine_per_page_mm, spine_mm=a.spine_mm)
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
