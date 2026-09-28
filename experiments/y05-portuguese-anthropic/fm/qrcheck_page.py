
import pymupdf,cv2,numpy as np,sys
d=pymupdf.open(sys.argv[1]); pg=d[int(sys.argv[2])-1]; det=cv2.QRCodeDetector()
rs=[]
for x in pg.get_drawings():
    r=x['rect']
    if 35<r.width<60 and abs(r.width-r.height)<1 and not any(abs(r.x0-q.x0)<3 and abs(r.y0-q.y0)<3 for q in rs): rs.append(r)
rs.sort(key=lambda r:(round(r.y0),r.x0))
res=[]
for r in rs:
    pix=pg.get_pixmap(dpi=200,clip=r+(-8,-8,8,8)); a=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)[:,:,:3].copy()
    v,_,_=det.detectAndDecode(a); res.append((round(r.x0),round(r.y0),round(r.width,1),v))
print(len(rs),'codes;',sum(1 for x in res if x[3]),'decoded at 200 dpi (one crop per code)')
for x in res:
    if not x[3]: print('FAIL',x)
