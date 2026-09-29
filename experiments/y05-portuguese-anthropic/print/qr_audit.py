import pymupdf, cv2, numpy as np, re, subprocess, sys
det = cv2.QRCodeDetector()
units = [("build", 24), ("u2/build", 40), ("u3/build", 16), ("u4/build", 16), ("u5/build", 16), ("u6/build", 16), ("u7/build", 16)]
allurls = set()
for u, exp in units:
    d = pymupdf.open(u + "/unit.pdf"); found = {}
    txt = " ".join(p.get_text() for p in d)
    for i, pg in enumerate(d):
        W, H = pg.rect.width, pg.rect.height
        for ty in range(8):
            for tx in range(4):
                clip = pymupdf.Rect(tx*W/4-40, ty*H/8-40, (tx+1)*W/4+40, (ty+1)*H/8+40) & pg.rect
                pix = pg.get_pixmap(dpi=200, clip=clip)
                a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
                v, _, _ = det.detectAndDecode(a)
                if v: found[v] = i + 1
    print(u, d.page_count, "(exp", exp, ") QRs", len(found), "vercel", sum("vercel" in x for x in found),
          "| text vercel:", txt.count("vercel"), "Year:", len(re.findall(r"\bYear\b", txt, re.I)), "faixa:", txt.lower().count("faixa"), flush=True)
    for x, p in sorted(found.items(), key=lambda t: t[1]):
        print("   p%d" % p, x[:120]); allurls.add(x)
print("HTTP:")
for x in sorted(allurls):
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "-m", "25", "-A", "Mozilla/5.0", "-w", "%{http_code}", x], capture_output=True, text=True)
    print(" ", r.stdout, x[:120], flush=True)
