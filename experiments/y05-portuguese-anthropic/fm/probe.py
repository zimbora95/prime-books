
import pymupdf, json, re, sys
def pages_info(pdf):
    d=pymupdf.open(pdf); out=[]
    for i,pg in enumerate(d):
        W,H=pg.rect.width,pg.rect.height
        spans=[]
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines",[]):
                for s in l["spans"]:
                    t=s["text"].strip()
                    if t: spans.append((s["bbox"],s["size"],t,s["font"],s["flags"]))
        run=[s for s in spans if s[0][3]<34]
        runL=" ".join(s[2] for s in run if s[0][0]<W/2); runR=" ".join(s[2] for s in run if s[0][0]>=W/2)
        fol=[s[2] for s in spans if s[0][1]>H-40 and re.fullmatch(r"\d{1,3}|[ivxlc]+",s[2])]
        body=[s for s in spans if 34<=s[0][3]<H-40]
        mx=max([s[1] for s in body],default=0)
        h1=" ".join(s[2] for s in body if s[1]>=mx-0.5 and s[1]>=20)
        out.append(dict(i=i+1,runL=runL,runR=runR,folio=fol,h1=h1[:90],h1size=round(mx,1)))
    return out
if __name__=="__main__":
    for r in pages_info(sys.argv[1]): print(r)
