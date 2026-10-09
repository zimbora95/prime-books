"""y06-art-and-design back cover: repair the white knockout bars baked into the
full-page raster back-cover art.

The bars are the residue of a redaction-with-white-fill performed on a page whose
background is one full-page image (the documented pymupdf trap). Strategy:
tone-matched vertical donor clone -- for every masked pixel take the pixel the
same number of rows away (a clean band of the SAME image, never a patched row),
then correct the donor block's row mean to the target row's own unmasked mean so
the patch keeps the wash's texture at the right tone. Feather the patch border.
"""
import numpy as np
from PIL import Image, ImageFilter

SRC = '/tmp/y06ad/back_art.png'
OUT = '/root/prime-books/tools/out/y06ad/back_art_repaired.png'

im = Image.open(SRC).convert('L')
a = np.asarray(im).astype(np.float32)
H, W = a.shape
sc = W / 612.0

white = a > 248
mask = np.asarray(Image.fromarray((white * 255).astype(np.uint8))
                  .filter(ImageFilter.MaxFilter(5))) > 0
print('mask px', int(mask.sum()), 'of', mask.size)

rm = np.where(mask, np.nan, a)
rowmean = np.nanmean(rm, axis=1)

# pick the shortest vertical shift whose donor rows are fully clean; prefer the
# donor BELOW the bands (-d) so the patch borrows the neighbouring wall texture
cand = []
for d in range(-(H - 1), H):
    if int((mask & np.roll(mask, d, axis=0)).sum()) == 0:
        cand.append(d)
cand.sort(key=lambda v: (abs(v), v))
neg = [v for v in cand if v <= 0]
d = neg[0] if neg else cand[0]
print('chosen shift', d)

src = np.roll(a, d, axis=0)
srcmean = np.roll(rowmean, d)
patched = a.copy()
rows = np.where(mask.any(axis=1))[0]
for y in rows:
    cols = mask[y]
    if not cols.any():
        continue
    don = src[y][cols]
    corr = rowmean[y] - srcmean[y]
    if not np.isfinite(corr):
        corr = 0.0
    patched[y][cols] = don + corr

# feather only the 3px ring of the former mask so no straight edge survives
ring = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                  .filter(ImageFilter.MaxFilter(7))) > 0
ring = ring & ~np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                          .filter(ImageFilter.MinFilter(7))) > 0
blur = np.asarray(Image.fromarray(patched.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)
patched = np.where(ring, blur, patched)

out = Image.fromarray(np.clip(patched, 0, 255).astype(np.uint8))
b = np.asarray(out).astype(np.float32)
# kill any residual pure-white pixel so the patch can never read as a knockout
b[mask] = np.minimum(b[mask], 245.0)
out = Image.fromarray(np.clip(b, 0, 255).astype(np.uint8))
out.save(OUT)
b = np.asarray(out).astype(np.float32)

# ---- verification ----
print('white residue inside mask (>248):', int((b[mask] > 248).sum()))
print('dark residue inside mask (<200):', int((b[mask] < 200).sum()))
print('patched min/mean inside mask: %.1f / %.2f' % (b[mask].min(), b[mask].mean()))
# row-mean continuity: compare patched row mean against the mean of the 12 clean
# rows above and below each band -> no visible step
bands = []
on = False
for y in range(H):
    if mask[y].any() and not on:
        on, y0 = True, y
    elif not mask[y].any() and on:
        on = False
        bands.append((y0, y - 1))
print('bands', bands)
for y0, y1 in bands:
    above = rowmean[max(0, y0 - 12):y0].mean()
    below = rowmean[y1 + 1:y1 + 13].mean()
    inside = b[y0:y1 + 1].mean()
    print('band %d-%d page y %.1f-%.1f inside %.2f above %.2f below %.2f delta %.2f'
          % (y0, y1, y0 / sc, y1 / sc, inside, above, below, inside - (above + below) / 2))
# untouched zones must be byte-identical to the original
diff = np.abs(b - a)
print('max change outside mask+ring: %.1f' % diff[~(mask | ring)].max())
