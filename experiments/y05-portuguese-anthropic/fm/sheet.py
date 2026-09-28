
from PIL import Image
import glob,sys
def sheet(files,out,cols=4,w=420):
    ims=[Image.open(f).convert("RGB") for f in files]
    ims=[i.resize((w,round(i.height*w/i.width))) for i in ims]
    h=max(i.height for i in ims); rows=(len(ims)+cols-1)//cols
    S=Image.new("RGB",(cols*w+(cols+1)*8,rows*h+(rows+1)*8),(90,90,90))
    for k,i in enumerate(ims): S.paste(i,(8+(k%cols)*(w+8),8+(k//cols)*(h+8)))
    S.save(out)
if __name__=="__main__":
    out=sys.argv[1]; cols=int(sys.argv[2]); sheet(sys.argv[3:],out,cols)
