"""Per-page DOM probe for Unit 5: content bottom, tip top and max right (mm). Run after build.py."""
import build, re, os, json, html as H
JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const mm=v=>Math.round(v/96*25.4*10)/10;const out=[];
document.querySelectorAll('.page').forEach((p,i)=>{const r=p.getBoundingClientRect();let bot=0,right=0;let tipTop=null;
p.querySelectorAll('.tip,[style*="bottom:21mm"],[style*="bottom:19mm"]').forEach(t=>{if(t.closest('.grid2')&&!t.style.position)return;const b=t.getBoundingClientRect();tipTop=tipTop===null?b.top-r.top:Math.min(tipTop,b.top-r.top)});
p.querySelectorAll('*').forEach(el=>{if(el.closest('.folio,.tab,.run,.p-open,[style*="bottom:21mm"],[style*="bottom:19mm"]'))return;const b=el.getBoundingClientRect();if(!b.height||el.children.length)return;bot=Math.max(bot,b.bottom-r.top);right=Math.max(right,b.right-r.left)});
out.push([i+97,mm(bot),tipTop===null?null:mm(tipTop),mm(right)])});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},600)})</script>"""
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "build", "unit.html")).read()
chk = os.path.join(here, "build", "chk.html")
open(chk, "w").write(src.replace("</body>", JS + "</body>"))
r = build.chrome(["--virtual-time-budget=9000", "--window-size=794,1123", "--dump-dom", "file://" + chk],
                 capture_output=True, text=True, timeout=480)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
print("page contentBottom tipTop maxRight  (page 297x210; target bottom 262-272, right<=194)")
for row in json.loads(H.unescape(m.group(1))):
    flag = ""
    if row[1] < 255: flag += "  UNDERFILLED"
    if row[1] > 274: flag += "  LOW"
    if row[2] and row[1] > row[2] - 2: flag += "  HITS-TIP"
    if row[3] > 194.5: flag += "  RIGHT"
    print(row, flag)
