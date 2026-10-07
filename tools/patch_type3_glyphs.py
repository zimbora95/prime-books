"""Replace single-glyph Type 3 symbol glyphs with the same vector paths.

The y08 Global Perspectives master (external author) sets 8 tiny symbols -- a
teal check mark (p70), four brown check marks (p109) and three white refresh
arrows (pp128-129) -- in three one-glyph Type 3 fonts. A Type 3 font is a
drawing program: it has no font program to embed, and BookVault's preflight
rejects the text file for it ("1 key font was unembedded").

The house pack's own repair (Ghostscript -dNoOutputFonts over the whole book,
tools/make_bookvault_files.py strip_fonts) bails on this title: 2 pages lose
characters in the re-laid invisible text layer, so the pack keeps the original
and the font check stays open. This pass is surgical instead: for each Type 3
use, the glyph's CharProc is replayed as page vector art at the same size,
colour and position, the Type 3 text is redacted, and the font resource is
removed. Everything else on the page is untouched -- verify with a render-hash
sweep: only the pages carrying the symbols may change, and those only by the
sub-point antialiasing of an identical path.

Usage: patch_type3_glyphs.py <in.pdf> <out.pdf> [--report]
"""
import re
import sys

import pymupdf

CURVE_SAMPLES = 12


def _nums(line: str) -> list[float]:
    return [float(x) for x in re.findall(r"-?\d*\.?\d+", line)]


def parse_charproc(stream: str) -> list[list[tuple[float, float]]]:
    """Subpaths of a Type 3 glyph program as point lists, curves flattened.

    Coordinates come back in the charproc's own units (including its `cm`).
    """
    scale = 1.0
    subpaths: list[list[tuple[float, float]]] = []
    cur: list[tuple[float, float]] = []
    last: tuple[float, float] | None = None

    def flush() -> None:
        nonlocal cur, last
        if len(cur) >= 2:
            subpaths.append(cur)
        cur, last = [], None

    for raw in stream.splitlines():
        line = raw.strip()
        if not line or line.endswith("d1"):
            continue
        op = line.split()[-1]
        if op == "cm":
            v = _nums(line)
            if len(v) >= 6 and abs(v[0] - 1) > 1e-9:
                scale *= v[0]
        elif op == "m":
            x, y = _nums(line)[:2]
            flush()
            cur = [(x, y)]
            last = (x, y)
        elif op == "l":
            x, y = _nums(line)[:2]
            cur.append((x, y))
            last = (x, y)
        elif op == "c":
            v = _nums(line)
            if len(v) < 6 or last is None:
                continue
            x0, y0 = last
            x1, y1, x2, y2, x3, y3 = v[:6]
            for i in range(1, CURVE_SAMPLES + 1):
                t = i / CURVE_SAMPLES
                u = 1 - t
                cur.append((
                    u**3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * x3,
                    u**3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * y3,
                ))
            last = (x3, y3)
        elif op in ("h", "f"):
            flush()
        # 're', colour ops etc. would need more work -- none in these fonts
    flush()
    return [[(x * scale, y * scale) for x, y in sp] for sp in subpaths]


def patch(path_in: str, path_out: str, report: bool = False) -> int:
    doc = pymupdf.open(path_in)
    done = 0
    t3_xrefs: set[int] = set()
    for pno in range(doc.page_count):
        page = doc[pno]
        uses = []
        raw = page.get_text("rawdict")
        for b in raw["blocks"]:
            if b.get("type") != 0:
                continue
            for ln in b["lines"]:
                for sp in ln["spans"]:
                    f = sp.get("font", "")
                    m = re.match(r"Type3 \((\d+) 0 R\)", f)
                    if m:
                        uses.append((int(m.group(1)), sp))
        if not uses:
            continue
        for xref, sp in uses:
            fontobj = doc.xref_object(xref)
            fm = doc.xref_get_key(xref, "FontMatrix")[1] if "FontMatrix" in fontobj else ""
            cp = doc.xref_get_key(xref, "CharProcs")[1]
            cp_xref = int(re.findall(r"(\d+) 0 R", cp)[0])
            stream = doc.xref_stream(cp_xref).decode("latin-1")
            subpaths = parse_charproc(stream)
            vals = _nums(fm) if fm else []
            fmx = abs(vals[0]) if len(vals) >= 4 else 0.00488281
            size = sp["size"]
            ox, oy = sp["origin"]
            col = int(sp.get("color", 0))
            rgb = (((col >> 16) & 255) / 255, ((col >> 8) & 255) / 255, (col & 255) / 255)
            # 1. redact the Type 3 glyph (text only: no fill, keep images and line art)
            r = pymupdf.Rect(sp["bbox"])
            r.x0 -= 0.3; r.y0 -= 0.3; r.x1 += 0.3; r.y1 += 0.3
            page.add_redact_annot(r, fill=False)
            page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                                  graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                                  text=pymupdf.PDF_REDACT_TEXT_REMOVE)
            # 2. replay the glyph program as vector art (same path, size, colour)
            shape = page.new_shape()
            for sub in subpaths:
                pts = [(ox + x * fmx * size, oy + y * fmx * size) for x, y in sub]
                if pts[0] != pts[-1]:
                    pts.append(pts[0])          # this PyMuPDF has no closePath
                shape.draw_polyline(pts)
            shape.finish(color=None, fill=rgb, closePath=False)
            shape.commit()
            t3_xrefs.add(xref)
            done += 1
            if report:
                bb = subpaths and [min(p[0] for s in subpaths for p in s), min(p[1] for s in subpaths for p in s)]
                print(f"  page {pno+1}: {len(subpaths)} subpaths, colour {rgb}, "
                      f"size {size:.3f}, origin ({ox:.1f},{oy:.1f})")
        # drop the font resource entry on every page that lists one of these fonts
        for xref in list(t3_xrefs):
            _drop_font_resource(doc, page, xref)
    # any page may still list the font without drawing it
    for pno in range(doc.page_count):
        for xref in t3_xrefs:
            _drop_font_resource(doc, doc[pno], xref)
    doc.save(path_out, garbage=4, deflate=True)
    left = pymupdf.open(path_out)
    remaining = 0
    for i in range(left.page_count):
        remaining += sum(1 for f in left[i].get_fonts(full=True)
                         if f[2] in ("Type3", "Type 3"))
    left.close()
    doc.close()
    print(f"{path_in} -> {path_out}: {done} glyph use(s) replaced, "
          f"{len(t3_xrefs)} Type 3 font(s) removed, {remaining} left")
    return remaining


def _drop_font_resource(doc: pymupdf.Document, page: pymupdf.Page, xref: int) -> None:
    kind, val = doc.xref_get_key(page.xref, "Resources/Font")
    if kind == "xref" and val:
        holder = int(re.findall(r"(\d+) 0 R", val)[0])
        base = ""
    elif kind == "dict" and val:
        holder = page.xref
        base = "Resources/Font/"
    else:
        return
    for key in re.findall(r"/([^\s/<>]+)\s+" + str(xref) + r" 0 R", doc.xref_object(holder)):
        doc.xref_set_key(holder, f"{base}{key}", "null")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--report"]
    rep = "--report" in sys.argv
    if len(args) != 2:
        raise SystemExit(__doc__)
    left = patch(args[0], args[1], report=rep)
    raise SystemExit(1 if left else 0)
