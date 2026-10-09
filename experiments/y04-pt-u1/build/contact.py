import sys
from PIL import Image, ImageDraw
files=sys.argv[2:]; out=sys.argv[1]
W=900; tiles=[]
for f in files:
    im=Image.open(f).convert('RGB'); im.thumbnail((W,W)); tiles.append((f,im))
cols=2; rows=(len(tiles)+1)//2
cw=W; ch=max(t[1].height for t in tiles)+30
sheet=Image.new('RGB',(cols*cw,rows*ch),'white'); d=ImageDraw.Draw(sheet)
for i,(f,im) in enumerate(tiles):
    x=(i%cols)*cw; y=(i//cols)*ch
    sheet.paste(im,(x,y+30)); d.text((x+5,y+5),f.split('/')[-1],fill='black')
sheet.save(out)
