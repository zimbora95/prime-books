"""Contact sheet: python sheet.py out.png a.png b.png ... (3 columns)."""
import sys
from PIL import Image


def sheet(files, out, cols=3, w=620):
    ims = [Image.open(f).convert("RGB") for f in files]
    h = int(ims[0].height * w / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * w + (cols + 1) * 12, rows * (h + 12) + 12), "#555")
    for i, im in enumerate(ims):
        S.paste(im.resize((w, h), Image.LANCZOS), (12 + (i % cols) * (w + 12), 12 + (i // cols) * (h + 12)))
    S.save(out)


if __name__ == "__main__":
    sheet(sys.argv[2:], sys.argv[1])
