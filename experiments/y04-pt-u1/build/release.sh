#!/bin/bash
# Full release pipeline for Rua das Palavras: build -> covers -> web/print PDF -> publish -> checks.
set -e
cd /root/prime-books/experiments/y04-pt-u1/build
PY=/root/prime-books/.venv/bin/python
$PY build.py --dpi 110 > /root/.hermes/cache/scratch/full.json 2>&1
if grep -qE "inner overflow|OVERLAP" /root/.hermes/cache/scratch/full.json; then
  grep -E "inner overflow|OVERLAP" /root/.hermes/cache/scratch/full.json; echo "STOP: layout errors"; exit 1
fi
$PY finalize.py
gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite -dCompatibilityLevel=1.6 -dPDFSETTINGS=/printer \
  -dColorImageResolution=300 -dGrayImageResolution=300 -dDownsampleColorImages=true \
  -dColorImageDownsampleType=/Bicubic -dAutoFilterColorImages=false -dColorImageFilter=/DCTEncode -dJPEGQ=88 \
  -dEmbedAllFonts=true -dSubsetFonts=true -sOutputFile=book-web-300.pdf book-final.pdf
D=/root/prime-books/public/library/y04-portuguese-anthropic
cp book-web-300.pdf $D/book.pdf
cd /root/prime-books
$PY - <<'EOF'
import pymupdf, json, os, re, cv2, numpy as np
from PIL import Image
D='public/library/y04-portuguese-anthropic'
d=pymupdf.open(f'{D}/book.pdf')
bad=[f for p in d for f in p.get_fonts(full=True) if f[1]=='n/a' or f[2]=='Type3']
print('pages', d.page_count, 'bad fonts', len(bad), 'sizes', {(round(p.rect.width), round(p.rect.height)) for p in d})
det=cv2.QRCodeDetector()
for n in (9,14,54,92,93,104):
    pix=d[n-1].get_pixmap(dpi=300); img=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)[:,:,:3].copy()
    ok,v,_,_=det.detectAndDecodeMulti(img); print('QR', n, [x for x in (v or []) if x])
print('vercel in text:', 'vercel' in ''.join(p.get_text() for p in d))
def shot(i,out):
    pix=d[i].get_pixmap(dpi=110); im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples).resize((900,1165),Image.LANCZOS); im.save(out,'WEBP',quality=86)
shot(0,f'{D}/cover.webp'); shot(0,f'{D}/preview/01.webp'); shot(1,f'{D}/preview/02.webp'); shot(d.page_count-1,f'{D}/preview/last.webp')
mb=round(os.path.getsize(f'{D}/book.pdf')/1e6,2)
p='public/library.json'; t=open(p).read()
i=t.index('"slug": "y04-portuguese-anthropic"'); j=t.index('"preview"',i)
seg=re.sub(r'"mb": [0-9.]+,',f'"mb": {mb},',t[i:j]); seg=re.sub(r'"pages": \d+,',f'"pages": {d.page_count},',seg)
t=t[:i]+seg+t[j:]; json.loads(t); open(p,'w').write(t); print('published mb', mb)
EOF
.venv/bin/python tools/make_bookvault_files.py y04-portuguese-anthropic --force > /root/.hermes/cache/scratch/bv.log 2>&1
tail -2 /root/.hermes/cache/scratch/bv.log
