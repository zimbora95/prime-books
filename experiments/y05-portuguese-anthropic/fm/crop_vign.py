
from PIL import Image, ImageFilter
import numpy as np, cv2
im=Image.open("art/vignettes.png").convert("RGB"); W,H=im.size
names=["v-gabinete","v-galo","v-poesia","v-teatro","v-comboio","v-avaliacao","v-jogos","v-livros","v-mourinha"]
for k,n in enumerate(names):
    r,c=divmod(k,3)
    cell=im.crop((c*W//3,r*H//3,(c+1)*W//3,(r+1)*H//3))
    a=np.asarray(cell).astype(np.uint8); m=(a.min(axis=2)<232).astype(np.uint8)
    md=cv2.dilate(m,np.ones((25,25),np.uint8))
    nl,lab,st,_=cv2.connectedComponentsWithStats(md)
    j=1+np.argmax(st[1:,cv2.CC_STAT_AREA])
    keep=(lab==j)
    # white out everything else
    b=a.copy(); b[~keep]=255
    ys,xs=np.where(keep&(m>0)); box=(max(xs.min()-8,0),max(ys.min()-8,0),min(xs.max()+8,cell.width),min(ys.max()+8,cell.height))
    Image.fromarray(b).crop(box).save(f"art/{n}.png"); print(n,box, nl-1)
