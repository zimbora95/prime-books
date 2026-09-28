"""Contact sheets: python qa_sheet.py [first last]  -> qa/sheet-<first>-<last>.jpg (3 per row)."""
import os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
png = os.path.join(HERE, "build", "png")
pages = sorted(int(f[:-4]) for f in os.listdir(png) if f.endswith(".png"))
a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (pages[0], pages[-1])
sel = [p for p in pages if a <= p <= b]
ims = [Image.open(os.path.join(png, f"{p}.png")).convert("RGB") for p in sel]
w, h = ims[0].size
cols = min(3, len(ims)); rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w + (cols + 1) * 20, rows * h + (rows + 1) * 20), (120, 116, 106))
for i, im in enumerate(ims):
    sheet.paste(im, (20 + (i % cols) * (w + 20), 20 + (i // cols) * (h + 20)))
os.makedirs(os.path.join(HERE, "qa"), exist_ok=True)
out = os.path.join(HERE, "qa", f"sheet-{a}-{b}.jpg")
sheet.save(out, quality=85)
print(out, sheet.size)
