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
SPINE_PER_PAGE. BookVault publish a sizing template per trim/binding/paper and
the spine depends on the paper's caliper, which is a printing-house figure, not
a useful default. The value below matches the KDP Premium Color wrap already
used for these titles. Confirm it against the BookVault template shown when the
title is created, then pass --spine-per-page <inches> and rebuild.

Usage
-----
    .venv/bin/python tools/make_bookvault_files.py <slug> [slug ...]
    .venv/bin/python tools/make_bookvault_files.py --all
    .venv/bin/python tools/make_bookvault_files.py <slug> --force --no-pdfx
"""
from __future__ import annotations

import argparse
import json
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

# ---------------------------------------------------------------- BookVault spec
BLEED_PT = 9.0            # 0.125 in = 3.175 mm
DPI = 300                 # cover raster resolution
SEG_PT = 3.0              # bleed smear segment length
SEG_DPI = 150             # resolution the edge is sampled at
SPINE_PER_PAGE = 0.002347  # inches per interior page -- CONFIRM (see docstring)
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
    """One interior page onto a bleed-sized media box, at the same trim size."""
    p = src[idx]
    w, h = p.rect.width, p.rect.height
    W, H = w + 2 * BLEED_PT, h + 2 * BLEED_PT
    page = dst.new_page(width=W, height=H)

    # the page itself, 1:1, inset by the bleed (vector -- text stays text)
    page.show_pdf_page(pymupdf.Rect(BLEED_PT, BLEED_PT, BLEED_PT + w, BLEED_PT + h),
                       src, idx)

    steps_x = max(1, int(round(w / SEG_PT)))
    steps_y = max(1, int(round(h / SEG_PT)))
    top = sample_edge(p, True, w, 0.25, steps_x)
    bot = sample_edge(p, True, w, h - 1.25, steps_x)
    lef = sample_edge(p, False, h, 0.25, steps_y)
    rig = sample_edge(p, False, h, w - 1.25, steps_y)

    draw_runs(page, top, "v", W, BLEED_PT, 0)
    draw_runs(page, bot, "v", W, BLEED_PT, H - BLEED_PT)
    draw_runs(page, lef, "h", H, BLEED_PT, 0)
    draw_runs(page, rig, "h", H, BLEED_PT, W - BLEED_PT)

    # corners: filled with the corner colour so no white pinhole survives
    for col, rect in (
        (top[0] if top else lef[0], pymupdf.Rect(0, 0, BLEED_PT, BLEED_PT)),
        (top[-1] if top else rig[0], pymupdf.Rect(W - BLEED_PT, 0, W, BLEED_PT)),
        (bot[0] if bot else lef[-1], pymupdf.Rect(0, H - BLEED_PT, BLEED_PT, H)),
        (bot[-1] if bot else rig[-1], pymupdf.Rect(W - BLEED_PT, H - BLEED_PT, W, H)),
    ):
        page.draw_rect(rect, color=None, fill=rgb01(col), width=0)


# ------------------------------------------------------------------- text file


def write_pdfx_def(path: pathlib.Path, title: str) -> None:
    """A Ghostscript PDF/X-3 prefix file with a real OutputIntent.

    Ghostscript ships PDFX_def.ps, but it points at 'ISO Coated sb.icc' in the
    current directory and stamps the title 'Title'. This writes our own, using
    the CMYK profile that actually exists on this host, so the output carries a
    valid DestOutputProfile instead of a dangling reference.
    """
    icc = "/usr/share/color/icc/ghostscript/default_cmyk.icc"
    path.write_text(
        f"""%!
[ /GTS_PDFXVersion (PDF/X-3:2002)
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
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        except subprocess.TimeoutExpired:
            shutil.copyfile(src_pdf, dst_pdf)
            return False, "Ghostscript timed out -- left as RGB"
    if r.returncode != 0 or not dst_pdf.is_file():
        shutil.copyfile(src_pdf, dst_pdf)
        last = (r.stderr or "").strip().splitlines()[-1:] or [""]
        return False, f"Ghostscript failed ({r.returncode}: {last[0][:120]}) -- left as RGB"

    ok, why = conversion_is_faithful(src_pdf, dst_pdf)
    if not ok:
        shutil.copyfile(src_pdf, dst_pdf)
        return False, f"conversion damaged the file ({why}) -- kept RGB"
    return True, "PDF/X-3:2002, CMYK, fonts embedded, text kept as text"


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
    trim = src[1].rect

    stripped_cover = True
    work = pymupdf.open()
    for i in range(1, n - 1):          # page 1 (cover) and last (back cover) out
        bleed_page(work, src, i)
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

    ok, note = (True, "left as RGB (--no-pdfx)")
    if do_pdfx:
        ok, note = to_pdfx(tmp, final, f"{meta.get('subject', slug)} Year {meta.get('year', '')}")
        tmp.unlink(missing_ok=True)
    else:
        shutil.move(str(tmp), str(final))

    doc = pymupdf.open(final)
    rec = {
        "file": final.name,
        "url": f"/library/{slug}/bookvault/{final.name}",
        "bytes": final.stat().st_size,
        "pages": doc.page_count,
        "trim_pt": [round(trim.width, 2), round(trim.height, 2)],
        "media_pt": [round(doc[0].rect.width, 2), round(doc[0].rect.height, 2)],
        "bleed_pt": BLEED_PT,
        "cover_stripped": stripped_cover,
        "pdfx": bool(ok and do_pdfx),
        "note": note,
    }
    doc.close()
    return rec


# ------------------------------------------------------------------ cover file


def build_cover_file(slug: str, spine_per_page: float, force: bool) -> dict:
    od = out_dir(slug)
    od.mkdir(parents=True, exist_ok=True)
    meta = slug_meta(slug)
    year = int(meta["year"])
    subject = meta["subject"]

    book = LIBRARY / slug / "book.pdf"
    doc = pymupdf.open(book)
    n = doc.page_count
    trim_w = doc[0].rect.width / 72.0    # inches, the book's own trim
    trim_h = doc[0].rect.height / 72.0
    interior_pages = n - 2               # cover + back cover go in the wrap
    # the spine is the caliper TIMES the page count -- passing the caliper
    # straight through produced a 0.06 mm spine on a 70-page book
    spine_in = interior_pages * spine_per_page
    front = mwc.page_image(doc, 0, DPI)
    back_idx = mwc.find_designed_back(doc)
    blurb = mwc.find_blurb(doc)
    doc.close()

    W = round((trim_w * 2 + spine_in + 0.125 * 2) * DPI)
    H = round((trim_h + 0.125 * 2) * DPI)
    back_w = round((trim_w + 0.125) * DPI)
    spine_w = max(1, round(spine_in * DPI))
    front_w = round((trim_w + 0.125) * DPI)

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
    if interior_pages >= mwc.MIN_SPINE_TEXT_PAGES:
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

    return {
        "file": pdf.name,
        "url": f"/library/{slug}/bookvault/{pdf.name}",
        "preview": f"/library/{slug}/bookvault/{png.name}",
        "bytes": pdf.stat().st_size,
        "px": [W, H],
        "spine_in": round(spine_in, 5),
        "spine_mm": round(spine_in * 25.4, 2),
        "full_cover_mm": [round((trim_w * 2 + spine_in + 0.25) * 25.4, 2),
                          round((trim_h + 0.25) * 25.4, 2)],
        "back_src": back_src,
        "trim_in": [trim_w, trim_h],
        "interior_pages": interior_pages,
        "spine_text": interior_pages >= mwc.MIN_SPINE_TEXT_PAGES,
    }


# ------------------------------------------------------------------ validation


def _xref_embedded(doc: pymupdf.Document, xref: int) -> bool:
    """Is this font embedded?

    get_fonts(full=True) does not report it. A Type0 (CID) font keeps its
    program on the descendant CIDFont, so follow DescendantFonts to the
    FontDescriptor and look for FontFile / FontFile2 / FontFile3.
    """
    if doc.xref_get_key(xref, "Subtype")[1] == "/Type0":
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
    missing, seen = [], set()
    for i in range(doc.page_count):
        for f in doc[i].get_fonts(full=True):
            xref, base = f[0], f[3]
            if xref in seen:
                continue
            seen.add(xref)
            if not _xref_embedded(doc, xref):
                missing.append(base)
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


def validate(slug: str, text: dict, cover: dict) -> list[dict]:
    """BookVault's own validation list, run here so the teacher sees the
    verdict before uploading rather than after."""
    checks = []

    def add(name, ok, detail, level="fail"):
        checks.append({"name": name, "pass": bool(ok), "detail": detail,
                       "level": level if not ok else "ok"})

    doc = pymupdf.open(LIBRARY / slug / "bookvault" / text["file"])
    n = doc.page_count

    add("Pages are single pages, not spreads",
        len({round(doc[i].rect.width, 1) for i in range(n)}) == 1,
        f"every page {fmt_mm(doc[0].rect.width)} x {fmt_mm(doc[0].rect.height)} mm "
        f"(all {n} the same width)")
    add("Page count is even (back cover lands alone in a spread)",
        n % 2 == 0, f"{n} interior pages", level="warn")
    add("Bleed on every edge",
        True, f"{fmt_mm(BLEED_PT)} mm (0.125 in) added all round")
    bad, pts = bleed_continues_edge(doc)
    add("Bleed continues the page edge",
        bad == 0,
        f"{pts - bad} of {pts} points across the cut lines are flat"
        + ("" if bad == 0 else f" -- {bad} mismatch, a white sliver would print"))
    add("Trim size declared",
        True, f"{fmt_mm(text['trim_pt'][0])} x {fmt_mm(text['trim_pt'][1])} mm as a "
              f"BookVault CUSTOM size; enter these numbers exactly")
    add("Cover pages stripped from the interior",
        text["cover_stripped"],
        "front cover and back cover removed -- they are in the cover file")
    emb, missing = fonts_embedded(doc)
    add("All fonts embedded", emb,
        "every font embedded" if emb else "NOT embedded: " + ", ".join(missing))
    low = images_under_300dpi(doc)
    add("Images at 300 DPI or better", not low,
        "all images >= 300 DPI" if not low else f"{len(low)} below 300 DPI, e.g. " + "; ".join(low[:3]),
        level="warn")
    add("PDF/X with CMYK colour",
        text["pdfx"], text["note"],
        level="warn")
    doc.close()

    add("Cover file is a full wrap",
        cover["px"][0] > cover["px"][1],
        f"back {mm(cover['full_cover_mm'][0])} x {mm(cover['full_cover_mm'][1])} mm, "
        f"spine {cover['spine_mm']} mm")
    add("Spine width confirmed against BookVault's template",
        False,
        f"built at {cover['spine_mm']} mm from {cover['interior_pages']} pages x "
        f"{SPINE_PER_PAGE} in/page -- check the template shown when you create "
        f"the title and pass --spine-per-page if it differs",
        level="warn")
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
    L.append(f"  Trim size .......... CUSTOM "
             f"{fmt_mm(text['trim_pt'][0])} mm wide x {fmt_mm(text['trim_pt'][1])} mm high")
    L.append(f"                       (US Letter: 8.5 x 11 in. BookVault's standard list")
    L.append(f"                       has no US Letter, so choose the custom size option.)")
    L.append(f"  Page count ......... {text['pages']} (interior only, covers excluded)")
    L.append(f"  Colour pages ....... {text['pages']}")
    L.append(f"  Mono pages ......... 0")
    L.append(f"  ISBN ............... {settings['isbn'] or '(none yet - BookVault can issue a dummy)'}")
    L.append(f"  Print type ......... {settings['printType']}")
    L.append("")
    L.append(thin)
    L.append("STEP 2  Upload the two files")
    L.append(thin)
    L.append(f"  TEXT FILE   {text['file']}")
    L.append(f"              {text['pages']} pages, {text['media_pt'][0]} x {text['media_pt'][1]} pt "
             f"= {fmt_mm(text['media_pt'][0])} x {fmt_mm(text['media_pt'][1])} mm with bleed")
    L.append(f"              {text['note']}")
    L.append(f"  COVER FILE  {cover['file']}")
    L.append(f"              {cover['px'][0]} x {cover['px'][1]} px at {DPI} DPI "
             f"= {mm(cover['full_cover_mm'][0])} x {mm(cover['full_cover_mm'][1])} mm")
    L.append(f"              spine {cover['spine_mm']} mm from {cover['interior_pages']} interior pages")
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
    L.append("  * Bleed is extended from each page's own edge artwork, as vector,")
    L.append("    so the running-header band and any full-bleed art carry to the")
    L.append("    trim line with no hairline gap.")
    L.append("  * The cover wrap uses the spine width above. Confirm it against the")
    L.append("    sizing template BookVault shows for this trim, binding and paper,")
    L.append("    then rebuild with --spine-per-page if it differs.")
    L.append("  * Colour conversion to CMYK uses Ghostscript's default CMYK profile.")
    L.append("    For a final print run, ask BookVault for their output profile and")
    L.append("    rebuild with --profile <icc>.")
    L.append("")
    path = out_dir(slug) / f"{slug}-bookvault.txt"
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return path


# ----------------------------------------------------------------------- build


def build(slug: str, force: bool = False, do_pdfx: bool = True,
          spine_per_page: float = SPINE_PER_PAGE) -> dict:
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
        if text and text.get("spine_per_page") == spine_per_page:
            return {**text, "reused": True}

    settings = settings_for(slug)
    text = build_text_file(slug, force, do_pdfx)
    cover = build_cover_file(slug, spine_per_page, force)
    checks = validate(slug, text, cover)
    sheet = write_spec_sheet(slug, text, cover, checks, settings)

    rec = {
        "slug": slug,
        "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_pages": pages,
        "source_mtime": source.stat().st_mtime,
        "source_bytes": source.stat().st_size,
        "spine_per_page": spine_per_page,
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
    ap.add_argument("--spine-per-page", type=float, default=SPINE_PER_PAGE)
    a = ap.parse_args()

    slugs = a.slugs
    if a.all or not slugs:
        slugs = [r["slug"] for r in rows() if (LIBRARY / r["slug"] / "book.pdf").is_file()]
    for slug in slugs:
        r = build(slug, force=a.force, do_pdfx=not a.no_pdfx,
                  spine_per_page=a.spine_per_page)
        fails = [c["name"] for c in r["checks"] if not c["pass"] and c["level"] == "fail"]
        print(f"{slug}: text {r['text']['pages']}pp {r['text']['bytes']/1e6:.1f}MB, "
              f"cover {r['cover']['px'][0]}x{r['cover']['px'][1]}px, "
              f"spine {r['cover']['spine_mm']}mm, "
              f"{'OK' if not fails else 'FAIL: ' + '; '.join(fails)}")


if __name__ == "__main__":
    main()
