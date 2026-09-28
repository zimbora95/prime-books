"""Contact sheets: python sheet.py <pngdir> <outprefix> [per=6] [first=1]"""
import sys, os, glob
from PIL import Image
d, out = sys.argv[1], sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 6
files = sorted(glob.glob(os.path.join(d, "*.png")))
ims = [Image.open(f) for f in files]
w, h = ims[0].size
sc = 0.5 if per > 6 else 0.62
cols = 6 if per > 6 else 3
tw, th = int(w * sc), int(h * sc)
for s in range(0, len(ims), per):
    grp = ims[s:s + per]
    rows = (len(grp) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols + 8 * (cols + 1), th * rows + 8 * (rows + 1)), "#555")
    for k, im in enumerate(grp):
        sheet.paste(im.resize((tw, th)), (8 + (k % cols) * (tw + 8), 8 + (k // cols) * (th + 8)))
    sheet.save(f"{out}{s // per + 1:02d}.png")
    print(f"{out}{s // per + 1:02d}.png", [os.path.basename(f) for f in files[s:s + per]])
