# Unit 4 layout probe: prints each page's top-level blocks with top/height in mm (run after build.py)
import os, re, json, subprocess, html as H, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import build
JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const mm=v=>Math.round(v/96*25.4*10)/10;const out=[];
document.querySelectorAll('.page').forEach((p,i)=>{const r=p.getBoundingClientRect();const rows=[];
[...p.children].forEach(c=>{const b=c.getBoundingClientRect();rows.push([(c.className||c.tagName).slice(0,24),mm(b.top-r.top),mm(b.height)]);
 if(c.classList.contains('act')||c.classList.contains('play')||c.classList.contains('grid2')){[...c.children].forEach(d=>{const e=d.getBoundingClientRect();rows.push(['  '+(d.className||d.tagName).slice(0,22),mm(e.top-r.top),mm(e.height)])})}});
out.push([i+81,rows])});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},500)})</script>"""
html = open("build/unit.html").read()
open("build/probe.html", "w").write(html.replace("</body>", JS + "</body>"))
r = subprocess.run(build.chrome_base() + ["--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + os.path.abspath("build/probe.html")], capture_output=True, text=True, timeout=420)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
want = {int(a) for a in sys.argv[1:]}
for pg, rows in json.loads(H.unescape(m.group(1))):
    if want and pg not in want:
        continue
    print("== page", pg)
    for c, t, h in rows:
        print(f"   {c:26s} top {t:6.1f}  h {h:6.1f}  bottom {t + h:6.1f}")
