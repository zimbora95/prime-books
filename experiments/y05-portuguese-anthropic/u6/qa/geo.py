
import build, subprocess, re, os, json, html as H, sys
# usage: geo.py PAGE "sel1" "sel2" ...
pg=int(sys.argv[1]); sels=sys.argv[2:]
JS = """<script>window.addEventListener('load',()=>{setTimeout(()=>{const px=96/25.4;const mm=v=>Math.round(v/px*10)/10;const out=[];
const p=document.querySelectorAll('.page')[%d];const R=p.getBoundingClientRect();
%s.forEach(s=>{p.querySelectorAll(s).forEach((e,i)=>{const b=e.getBoundingClientRect();out.push([s,i,mm(b.left-R.left),mm(b.top-R.top),mm(b.right-R.left),mm(b.bottom-R.top),(e.textContent||'').trim().slice(0,40)])})});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},500)})</script>""" % (pg-113, json.dumps(sels))
html = open("build/unit.html").read()
open("build/chk3.html", "w").write(html.replace("</body>", JS + "</body>"))
r = subprocess.run([build.CHROME, "--headless", "--no-sandbox", "--disable-gpu","--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + os.path.abspath("build/chk3.html")],capture_output=True, text=True, timeout=600)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
for row in json.loads(H.unescape(m.group(1))): print(row)
