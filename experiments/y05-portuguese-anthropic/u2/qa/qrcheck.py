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
for p,v in sorted(found): print(p+24, v)
