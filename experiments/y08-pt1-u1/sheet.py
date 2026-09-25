
from PIL import Image
def sheet(nums,out):
    ims=[Image.open(f'build/p{i:02d}.png') for i in nums]; w,h=ims[0].size
    s=Image.new('RGB',(w*4+30,h*((len(ims)+3)//4)+10*((len(ims)+3)//4)),'#555')
    for k,im in enumerate(ims): s.paste(im,((k%4)*(w+10),(k//4)*(h+10)))
    s.save(out)
sheet(range(9,17),'build/sheet2.png'); sheet(range(17,25),'build/sheet3.png'); sheet([1,2,3,25,26,27,28,4],'build/sheet4.png')
