#!/usr/bin/env python
"""Render page 1 of each serving PDF in public/ to a 1024x1536 cover JPG in public/covers/.
The 3D book face and card covers are 2:3; the books are 210x270mm (7:9), so we centre-crop
the page width (~15mm each side) to fill the face. Run after copy-books.sh."""
import os, sys, glob

import fitz  # PyMuPDF

PUB = r"C:\Users\alexa\Documents\GitHub\prime-books\public"
OUT = os.path.join(PUB, "covers")
os.makedirs(OUT, exist_ok=True)

TARGET_W, TARGET_H = 1024, 1536

ok = fail = skip = 0
for pdf in sorted(glob.glob(os.path.join(PUB, "PrimeBooks *.pdf"))):
    base = os.path.splitext(os.path.basename(pdf))[0]
    dst = os.path.join(OUT, base + ".jpg")
    if os.path.exists(dst):
        print(f"SKIP {base}.jpg (exists)")
        skip += 1
        continue
    try:
        doc = fitz.open(pdf)
        page = doc[0]
        r = page.rect  # ~595.28 x 793.70 pt for 210x270mm
        clip_w = r.height * TARGET_W / TARGET_H
        x0 = (r.width - clip_w) / 2
        clip = fitz.Rect(x0, 0, x0 + clip_w, r.height)
        zoom = TARGET_W / clip_w
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
        try:
            pix.save(dst)  # PyMuPDF >= 1.19 writes .jpg natively
        except Exception:
            from PIL import Image

            Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(
                dst, "JPEG", quality=85
            )
        doc.close()
        kb = os.path.getsize(dst) // 1024
        print(f"OK   {base}.jpg  {pix.width}x{pix.height}  {kb}KB")
        ok += 1
    except Exception as e:
        print(f"FAIL {base}: {e}")
        fail += 1
print(f"=== covers ok={ok} fail={fail} skip={skip} ===")
