#!/usr/bin/env python
"""Web-optimise a Prime Book PDF for the in-browser flipbook.

The masters in <MEGA project>/BOOKS/.../PDF/Output are print-grade (300dpi+,
the worst is 265 MB). pdf.js in a browser tab chokes long before that, so the
serving copy is re-encoded: every raster image is downsampled to the resolution
it is actually *placed* at (DPI target) and recompressed as JPEG. Vector text
and line art are never touched, so pages stay crisp at flipbook zoom.

Two things this deliberately does NOT do, both learned the hard way:

  * MuPDF's own Document.rewrite_images() is ~2x worse on size AND it
    corrupts page resource dictionaries ("cannot find Pattern resource
    P40"), which silently drops the gradient overlays behind white text on
    unit-opener pages. Measured on Y1 Computing & Robotics p138: mean
    pixel diff 34.1 with rewrite_images vs 1.3 with this per-image pass.
  * Images carrying a soft mask / alpha channel are left alone. JPEG has
    no alpha, so recompressing them turns transparent cut-outs into white
    boxes.

Usage:  python tools/webopt_pdf.py <src.pdf> <dst.pdf> [dpi] [quality]
"""
from __future__ import annotations

import io
import os
import sys

import fitz  # PyMuPDF

DPI_TARGET = 150
JPEG_QUALITY = 74
# Below this stored size an image is not worth a round-trip through PIL.
MIN_BYTES = 20 * 1024
# Only swap in the JPEG when it saves at least this fraction.
GAIN = 0.92


def optimise(
    src: str,
    dst: str,
    dpi: int = DPI_TARGET,
    quality: int = JPEG_QUALITY,
) -> dict:
    from PIL import Image

    doc = fitz.open(src)

    # xref -> (largest placement area, that rect, a page index showing it).
    # An image reused on many pages is encoded once, at the biggest size it
    # is ever drawn, so no placement ends up upscaled.
    boxes: dict[int, tuple[float, fitz.Rect, int]] = {}
    for pno in range(doc.page_count):
        page = doc[pno]
        for info in page.get_images(full=True):
            xref = info[0]
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                continue
            for r in rects:
                area = r.width * r.height
                if area > boxes.get(xref, (0.0, None, 0))[0]:
                    boxes[xref] = (area, r, pno)

    stats = {
        "pages": doc.page_count,
        "images": len(boxes),
        "recoded": 0,
        "skipped": 0,
        "kept_alpha": 0,
    }

    for xref, (_, box, pno) in boxes.items():
        try:
            raw = doc.extract_image(xref)
        except Exception:
            stats["skipped"] += 1
            continue

        data = raw.get("image") or b""
        if len(data) < MIN_BYTES:
            stats["skipped"] += 1
            continue

        # A soft mask means real transparency; JPEG would flatten it to white.
        if raw.get("smask"):
            stats["kept_alpha"] += 1
            continue

        want_w = max(1, int(round(box.width / 72.0 * dpi)))
        want_h = max(1, int(round(box.height / 72.0 * dpi)))

        try:
            img = Image.open(io.BytesIO(data))
            img.load()
        except Exception:
            stats["skipped"] += 1
            continue

        if img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info:
            stats["kept_alpha"] += 1
            continue
        if img.mode != "RGB":
            img = img.convert("RGB")

        if img.width > want_w or img.height > want_h:
            img = img.resize(
                (min(img.width, want_w), min(img.height, want_h)),
                Image.LANCZOS,
            )

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
        jpeg = buf.getvalue()
        if len(jpeg) >= len(data) * GAIN:
            stats["skipped"] += 1
            continue

        try:
            doc[pno].replace_image(xref, stream=jpeg)
            stats["recoded"] += 1
        except Exception:
            stats["skipped"] += 1

    doc.save(dst, garbage=4, deflate=True, deflate_images=False)
    doc.close()

    stats["src_mb"] = round(os.path.getsize(src) / 1048576, 1)
    stats["dst_mb"] = round(os.path.getsize(dst) / 1048576, 1)
    return stats


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    a_dpi = int(sys.argv[3]) if len(sys.argv) > 3 else DPI_TARGET
    a_q = int(sys.argv[4]) if len(sys.argv) > 4 else JPEG_QUALITY
    print(optimise(sys.argv[1], sys.argv[2], a_dpi, a_q))
