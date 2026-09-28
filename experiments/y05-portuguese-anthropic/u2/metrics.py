"""Per-page DOM probe for Unit 2: content bottom, Mourinha-tip top, max right, overlaps.
Run after build.py:  python metrics.py
Page is 297 mm tall; content must end <= 270 mm (and above any absolutely placed tip);
right edge <= 194 mm (A4 210 mm - 16 mm margin)."""
import os, re, json, subprocess, html as H
import build

JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{const mm=v=>Math.round(v/96*25.4*10)/10;const out=[];
document.querySelectorAll('.page').forEach((p,i)=>{const r=p.getBoundingClientRect();let bot=0,right=0,left=999;let tipTop=null;const iss=[];
const tips=[...p.querySelectorAll('.tip.abs,.abs')];
tips.forEach(t=>{const b=t.getBoundingClientRect();tipTop=tipTop===null?b.top-r.top:Math.min(tipTop,b.top-r.top)});
p.querySelectorAll('*').forEach(el=>{if(el.closest('.folio,.tab,.run,.p-open,.abs,.bleed'))return;if(el.closest('svg')&&el.tagName!=='svg')return;const b=el.getBoundingClientRect();if(!b.height||!b.width)return;
 if(true){bot=Math.max(bot,b.bottom-r.top);right=Math.max(right,b.right-r.left);left=Math.min(left,b.left-r.left)}
 if(el.scrollWidth>el.clientWidth+2&&getComputedStyle(el).overflowX!=='visible'&&el.tagName!=='svg')iss.push('HCLIP '+(el.className||el.tagName));
 if(el.scrollHeight>el.clientHeight+2&&getComputedStyle(el).overflowY==='hidden'&&!el.classList.contains('page'))iss.push('VCLIP '+(el.className||el.tagName));});
out.push([p.querySelector('.folio')?p.querySelector('.folio').textContent:'-',mm(bot),tipTop===null?null:mm(tipTop),mm(left),mm(right),[...new Set(iss)].slice(0,4)])});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},600)})</script>"""

src = os.path.join(build.BUILD, "unit.html")
chk = os.path.join(build.BUILD, "chk.html")
open(chk, "w").write(open(src).read().replace("</body>", JS + "</body>"))
r = subprocess.run([build.CHROME, "--no-sandbox", "--disable-gpu",
                    "--virtual-time-budget=10000", "--window-size=794,1123", "--dump-dom", "file://" + chk],
                   capture_output=True, text=True, timeout=240)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
print("folio  bottom  tipTop  left  right  issues   (limits: bottom<=270 & < tipTop-2, left>=14, right<=196)")
for f, bot, tip, left, right, iss in json.loads(H.unescape(m.group(1))):
    flag = []
    if bot > 270: flag.append("LOW")
    if tip is not None and bot > tip - 2: flag.append("HITS-TIP")
    if right > 196: flag.append("RIGHT")
    if left < 14: flag.append("LEFT")
    if bot < 240 and tip is None: flag.append("UNDERFILLED?")
    if tip is not None and tip - bot > 30: flag.append("GAP-ABOVE-TIP?")
    print(f"{f:>4} {bot:7} {str(tip):>7} {left:6} {right:6}  {' '.join(flag)} {iss if iss else ''}")
