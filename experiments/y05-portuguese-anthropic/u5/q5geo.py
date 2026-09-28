"""Q5 geometry dump: python q5geo.py PAGE 'css selector' ['css selector' ...]  -> rects in mm (page-relative)."""
import build, re, os, json, sys, html as H
page = int(sys.argv[1]); sels = sys.argv[2:]
JS = """<script>window.addEventListener('load',()=>{setTimeout(()=>{const MM=v=>Math.round(v/96*25.4*10)/10;
const p=document.querySelectorAll('.page')[%d];const pr=p.getBoundingClientRect();const out=[];
%s.forEach(s=>{p.querySelectorAll(s).forEach((e,i)=>{const r=e.getBoundingClientRect();
out.push([s,i,MM(r.left-pr.left),MM(r.top-pr.top),MM(r.right-pr.left),MM(r.bottom-pr.top),MM(r.height),(e.textContent||'').trim().slice(0,38)])})});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},800)})</script>""" % (page - 97, json.dumps(sels))
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "build", "unit.html")).read()
chk = os.path.join(here, "build", "q5geo.html")
open(chk, "w").write(src.replace("</body>", JS + "</body>"))
r = build.chrome(["--virtual-time-budget=9000", "--window-size=794,1123", "--dump-dom", "file://" + chk],
                 capture_output=True, text=True, timeout=480)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
for row in json.loads(H.unescape(m.group(1))):
    L, T, R, B, h = row[2:7]
    print(row[0], row[1], "x %.1f–%.1f  y %.1f–%.1f  h %.1f" % (L, R, T, B, h), "|", row[7].replace("\n", " ")[:38])
