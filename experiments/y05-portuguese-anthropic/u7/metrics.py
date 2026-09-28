"""Per-page DOM probe for Unit 7: content bottom, tip top, max right, overflowing leaves.
Run after build.py:  python metrics.py
"""
import html as H, json, os, re, subprocess
import build

JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const mm=v=>Math.round(v/96*25.4*10)/10;const out=[];
document.querySelectorAll('.page').forEach((p,i)=>{const r=p.getBoundingClientRect();let bot=0,right=0,tipTop=null,over=[];
p.querySelectorAll('.tip,[style*="bottom:21mm"]').forEach(t=>{const b=t.getBoundingClientRect();tipTop=tipTop===null?b.top-r.top:Math.min(tipTop,b.top-r.top)});
p.querySelectorAll('*').forEach(el=>{if(el.closest('.folio,.tab,.run,.p-open,.tip,[style*="bottom:21mm"]'))return;const b=el.getBoundingClientRect();if(!b.height)return;
  if(el.scrollHeight>el.clientHeight+2&&getComputedStyle(el).overflow==='hidden'&&!el.classList.contains('panel')&&!el.classList.contains('face'))over.push('CLIP '+(el.className||el.tagName));
  if(el.children.length)return;bot=Math.max(bot,b.bottom-r.top);right=Math.max(right,b.right-r.left);
  if(b.right>r.right-11*96/25.4)over.push('RIGHT '+(el.className||el.tagName)+' '+mm(b.right-r.left))});
out.push([i+1,mm(bot),tipTop===null?null:mm(tipTop),mm(right),[...new Set(over)].slice(0,6)])});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},800)})</script>"""

src = os.path.join(build.BUILD, "unit.html")
chk = os.path.join(build.BUILD, "chk.html")
open(chk, "w").write(open(src).read().replace("</body>", JS + "</body>"))
r = subprocess.run([build.CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", f"--user-data-dir={build.PROFILE}-m",
                    "--virtual-time-budget=10000", "--window-size=794,1123", "--dump-dom", "file://" + chk],
                   capture_output=True, text=True, timeout=1500)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
print("page folio contentBottom tipTop maxRight issues   (usable bottom ~270-280, tip must be below content)")
for p, bot, tip, right, iss in json.loads(H.unescape(m.group(1))):
    flag = ""
    if tip is not None and bot > tip - 2:
        flag += " COLLIDES-WITH-TIP"
    if bot > 281:
        flag += " TOO-LOW"
    print(p, build.FIRST_FOLIO + p - 1, bot, tip, right, iss, flag)
