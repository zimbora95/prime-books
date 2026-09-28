
from PIL import Image
def sheet(nums,out):
    ims=[Image.open(f'build/p{i:02d}.png') for i in nums]; w,h=ims[0].size
    s=Image.new('RGB',(w*4+30,h*2+10),'#555')
    for k,im in enumerate(ims): s.paste(im,((k%4)*(w+10),(k//4)*(h+10)))
    s.save(out)
pp=list(range(31,75))
for j in range(0,len(pp),8): sheet(pp[j:j+8],f'build/u2s{j//8+1}.png')
print('ok')
