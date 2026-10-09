import pymupdf,cv2,numpy as np,re
d=pymupdf.open("build/unit.pdf");det=cv2.QRCodeDetector();found=set()
for i,pg in enumerate(d):
    W,H=pg.rect.width,pg.rect.height
    for ty in range(8):
        for tx in range(4):
            clip=pymupdf.Rect(tx*W/4-40,ty*H/8-40,(tx+1)*W/4+40,(ty+1)*H/8+40)&pg.rect
            pix=pg.get_pixmap(dpi=200,clip=clip);a=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)[:,:,:3].copy()
            v,_,_=det.detectAndDecode(a)
            if v: found.add((i+113,v))
print("QR decoded:",sorted(found))
print("pages",d.page_count,d[0].rect)
fonts={(f[2],f[3].split('+')[-1]) for p in d for f in p.get_fonts()};print("font types",{t for t,_ in fonts},"families",sorted({re.sub(r'-.*','',n) for _,n in fonts}))
txt=" ".join(p.get_text() for p in d)
for k in ["vercel","audio/","Year ","http","www.","áudio","QR"]: print(k, txt.count(k))
print("links",[l.get('uri') for p in d for l in p.get_links()])
