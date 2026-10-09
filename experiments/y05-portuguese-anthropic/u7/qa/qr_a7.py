
import pymupdf,cv2,numpy as np
d=pymupdf.open("build/unit.pdf");det=cv2.QRCodeDetector();found=set()
for i,pg in enumerate(d):
    W,H=pg.rect.width,pg.rect.height
    for ty in range(8):
        for tx in range(4):
            clip=pymupdf.Rect(tx*W/4-40,ty*H/8-40,(tx+1)*W/4+40,(ty+1)*H/8+40)&pg.rect
            pix=pg.get_pixmap(dpi=200,clip=clip);a=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)[:,:,:3].copy()
            v,_,_=det.detectAndDecode(a)
            if v: found.add((i+129,v))
for f in sorted(found): print("QR",*f)
fonts=sorted({(f[1],f[2],f[3]) for pg in d for f in pg.get_fonts()})
print("types",sorted({f[1] for f in fonts}),"n",len(fonts))
import re
print("families",sorted({re.sub(r"^[A-Z]{6}\+","",f[2]).split("-")[0] for f in fonts}))
txt="".join(pg.get_text() for pg in d)
for w in ("vercel","audio/","Year ","Ouvir","ouvir","áudio"): print(w,txt.count(w))
print("pages",d.page_count)
