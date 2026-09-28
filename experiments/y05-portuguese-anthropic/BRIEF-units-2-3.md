# Brief — Português · Year 5 (experiment `y05-portuguese-anthropic`), Units 2 and 3

The book is a premium, illustrated pt-PT (European Portuguese) textbook for Cambridge-international pupils aged 9–10
whose first language is Portuguese. Unit 1 is DONE and published — it is the design reference for everything:

- Source:  `experiments/y05-portuguese-anthropic/src/unit.html` (HTML/CSS, `{{…}}` tokens) and `build.py`
  (tokens → `build/unit.html` → Playwright Chromium PDF → `build/png/NN.png`), `metrics.py` (per-page DOM
  overflow/collision probe), `audio_scripts.py` (edge-tts pt-PT tracks). Rendered pages: `build/png/01..24.png`
  — LOOK at several of them before designing anything.
- Python with every dependency (edge-tts, segno, pillow, cv2, pymupdf, playwright): `/root/.hermes/cache/scratch/exp-venv/bin/python`.
- Fonts in `fonts/` (Fraunces etc.) — reuse; do not add new families.

## Non-negotiables (same as Unit 1)
- A4 portrait, the SAME type system, colours (ink navy #1C2536, vermilion, ochre, sage, bottle green, cream paper),
  folio/tab system, activity numbering style, bronze/prata/ouro difficulty keys, gecko mascot «Mourinha» speech
  bubbles (reuse `art/mou-*.png`), boxes, rule lines, QR blocks. Each unit has its own accent within the palette.
- Every page full and composed — no dead white bands, no overflow, nothing colliding; content bottom ≤ ~270 mm.
- Art: hand-painted gouache + coloured pencil, mid-century European picture-book manner, visible paper grain,
  flat matte colour, same palette, pure white backgrounds for spot art, NO text in images. Generate with
  image_generate; generate multi-panel sheets (2×2 / 3×3) and crop them for character/style consistency;
  review every image with vision_analyze before using it. Put art in your unit folder's `art/`.
- pt-PT only (acordo ortográfico: «ação», «facto», «receção»), polished; no Brazilianisms. Facts must be true
  — web-check them (legends, biographies, places) and cite sources in small print as Unit 1 does.
- Copyrighted works («O Rapaz de Bronze», Sophia de Mello Breyner Andresen; «Ynari, a Menina das Cinco Tranças»,
  Ondjaki; José Jorge Letria poems): ONLY short quoted extracts of a few lines each (≤ ~4 lines), attributed,
  plus your OWN summaries and activities. The whole book is read in class. Public-domain / traditional texts
  (Lenda do Galo de Barcelos) may be retold in full in your own words.
- Audio: edge-tts pt-PT voices (pt-PT-RaquelNeural, pt-PT-DuarteNeural…), same approach as `audio_scripts.py`.
  Only ORIGINAL or public-domain text is recorded — never record copyrighted extracts.
  File names MUST be prefixed with your unit: `u2-01-….mp3` / `u3-01-….mp3`. They will be served at
  `https://prime-books-pi.vercel.app/library/y05-portuguese-anthropic/audio/<file>`; teacher solutions at
  `https://prime-books-pi.vercel.app/library/y05-portuguese-anthropic/solucoes-u2.html` (or `-u3`). Write that
  solutions page too (see `site/solucoes.html` for the Unit 1 model), in your unit folder `site/`.
- QR codes: segno, WITH a viewBox (see `qr_svg` in Unit 1 `build.py` — the viewBox fix matters) and a 4-module
  quiet zone. After building, decode every QR from the PDF at 200 dpi with cv2.QRCodeDetector on tiled crops
  (see how, below) and report each decoded URL.
- Folios continue the book: Unit 1 = pp. 1–24. Unit 2 = pp. 25–64 (40 pages). Unit 3 = pp. 65–80 (16 pages).
  Page count must be exactly that (even), no blank pages. Fonts must be embedded (check with pymupdf get_fonts).

## Workspace rules
- Work ONLY inside your folder: `experiments/y05-portuguese-anthropic/u2/` or `.../u3/` (copy/adapt `build.py`,
  `metrics.py`, `audio_scripts.py`, and the CSS from `src/unit.html` into it; relative paths to `../fonts` and
  `../art/mou-*.png` are fine). Do NOT modify Unit 1 files, anything under `public/`, or git. Never commit/push.
- Output: `<folder>/build/unit.pdf`, `<folder>/build/png/NN.png`, `<folder>/audio/*.mp3`, `<folder>/site/solucoes-uN.html`.

## QA loop (mandatory before you report)
1. `metrics.py` clean: no overflow past the right margin, no content/bubble collisions, no page under-filled.
2. Contact sheets (6 pages each) + vision_analyze on EVERY page as a strict art director: collisions, clipping,
   empty boxes, awkward white space, illegible titles, image with text in it, cropped heads. Fix and rebuild
   until clean. 3. QR decode test. 4. Font embed check. 5. Proof-read all Portuguese once more.

QR decode snippet:
```python
import pymupdf,cv2,numpy as np
d=pymupdf.open("build/unit.pdf");det=cv2.QRCodeDetector();found=set()
for i,pg in enumerate(d):
    W,H=pg.rect.width,pg.rect.height
    for ty in range(8):
        for tx in range(4):
            clip=pymupdf.Rect(tx*W/4-40,ty*H/8-40,(tx+1)*W/4+40,(ty+1)*H/8+40)&pg.rect
            pix=pg.get_pixmap(dpi=200,clip=clip);a=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)[:,:,:3].copy()
            v,_,_=det.detectAndDecode(a)
            if v: found.add((i+1,v))
print(sorted(found))
```
