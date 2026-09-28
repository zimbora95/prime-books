"""Contact sheets, 6 pages each: build/sheet-1.jpg .. sheet-3.jpg"""
import glob, os
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
pngs = sorted(glob.glob(os.path.join(here, "build", "png", "*.png")))
for k in range(0, len(pngs), 6):
    ims = [Image.open(f).convert("RGB").resize((620, 877)) for f in pngs[k:k + 6]]
    sheet = Image.new("RGB", (3 * 630 + 10, 2 * 887 + 10), "#888")
    for j, im in enumerate(ims):
        sheet.paste(im, (10 + (j % 3) * 630, 10 + (j // 3) * 887))
    sheet.save(os.path.join(here, "build", f"sheet-{k // 6 + 1}.jpg"), quality=85)
print("ok")
