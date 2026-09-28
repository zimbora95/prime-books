
from PIL import Image
import numpy as np, cv2
im=Image.open("art/vignettes.png").convert("RGB"); W,H=im.size
x0,x1=W//3,2*W//3
reg=np.asarray(im.crop((x0,H//3,x1,H))).copy()
m=(reg.min(axis=2)<232).astype(np.uint8)
md=cv2.dilate(m,np.ones((7,7),np.uint8))
nl,lab,st,cen=cv2.connectedComponentsWithStats(md)
big=[i for i in range(1,nl) if st[i,cv2.CC_STAT_AREA]>300]
for i in big: print(i,st[i],cen[i])

for i,n in [(1,"v-comboio"),(2,"v-livros")]:
    b=reg.copy(); keep=(lab==i); b[~keep]=255
    ys,xs=np.where(keep&(m>0)); box=(max(xs.min()-8,0),max(ys.min()-8,0),min(xs.max()+8,b.shape[1]),min(ys.max()+8,b.shape[0]))
    Image.fromarray(b).crop(box).save(f"art/{n}.png"); print(n,box)
