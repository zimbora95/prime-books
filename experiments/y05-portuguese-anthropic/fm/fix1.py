
from PIL import Image
import numpy as np
im=np.asarray(Image.open("art/v-comboio.png").convert("RGB")).copy()
x1,y1,x2,y2=40,244,52,270
box=im[y1:y2,x1:x2].astype(int)
L=box.mean(axis=2); red=(box[:,:,0]>140)&(box[:,:,0]-box[:,:,2]>60)
print("dark px",(L<110).sum(),"red px",red.sum())
med=np.median(box[red],axis=0)
for y in range(y1,y2):
    for x in range(x1,x2):
        p=im[y,x].astype(int)
        if p.mean()<130 and not (p[0]>140): im[y,x]=np.clip(med+np.random.randint(-8,8,3),0,255)
Image.fromarray(im).save("art/v-comboio.png")
Image.fromarray(im).crop((0,200,160,330)).resize((640,520)).save("ref/zoom.png")
