"""Q5 QA probe: per-page text collisions, text escaping its box, clipped overflow, answer-line pitch.
Run after build.py:  python q5probe.py [page ...]"""
import build, re, os, json, sys, html as H

JS = r"""<script>window.addEventListener('load',()=>{setTimeout(()=>{
const MM=v=>Math.round(v/96*25.4*10)/10;const out=[];
function textRects(root){const res=[];const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){if(!n.textContent.trim())continue;const el=n.parentElement;const cs=getComputedStyle(el);
  if(cs.visibility==='hidden'||cs.display==='none')continue;const r=document.createRange();r.selectNodeContents(n);
  for(const b of r.getClientRects()){if(b.width<1||b.height<1)continue;res.push({el,b,t:n.textContent.trim().slice(0,40)})}}return res}
function boxAnc(el,page){let a=el.parentElement;while(a&&a!==page){const s=getComputedStyle(a);
 if((parseFloat(s.borderTopWidth)>0&&parseFloat(s.borderLeftWidth)>0)||(s.backgroundColor!=='rgba(0, 0, 0, 0)'&&s.backgroundColor!=='transparent'))return a;a=a.parentElement}return null}
const lab=e=>(e.tagName+'.'+(e.className&&e.className.baseVal===undefined?e.className:'')).slice(0,40);
document.querySelectorAll('.page').forEach((p,i)=>{const pr=p.getBoundingClientRect();const iss=[];
 const tr=textRects(p);
 // text-text collisions between different text nodes' elements
 for(let a=0;a<tr.length;a++)for(let b=a+1;b<tr.length;b++){const A=tr[a].b,B=tr[b].b;
  const ox=Math.min(A.right,B.right)-Math.max(A.left,B.left),oy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);
  if(ox>1.5&&oy>Math.min(A.height,B.height)*0.35)iss.push('TXT×TXT "'+tr[a].t+'" / "'+tr[b].t+'" '+MM(ox)+'x'+MM(oy)+'mm')}
 // text over images (content imgs)
 p.querySelectorAll('img').forEach(im=>{if(im.closest('.p-open'))return;const I=im.getBoundingClientRect();
  tr.forEach(t=>{const A=t.b;const ox=Math.min(A.right,I.right)-Math.max(A.left,I.left),oy=Math.min(A.bottom,I.bottom)-Math.max(A.top,I.top);
   if(ox>1&&oy>1)iss.push('TXT×IMG "'+t.t+'" on '+im.getAttribute('src').split('/').pop())})});
 // text escaping its bordered/filled box
 tr.forEach(t=>{const bx=boxAnc(t.el,p);if(!bx)return;const R=bx.getBoundingClientRect();const A=t.b;
  if(A.left<R.left-0.5||A.right>R.right+0.5||A.top<R.top-0.5||A.bottom>R.bottom+0.5)iss.push('ESCAPE "'+t.t+'" from '+lab(bx)+' by '+MM(Math.max(R.left-A.left,A.right-R.right,R.top-A.top,A.bottom-R.bottom))+'mm')});
 // text out of the page safe area
 tr.forEach(t=>{const A=t.b;if(t.el.closest('.p-open,.tab,.folio'))return;if(A.right>pr.right-12*96/25.4+0.5||A.left<pr.left+12*96/25.4-0.5||A.bottom>pr.bottom-14*96/25.4)iss.push('MARGIN "'+t.t+'"')});
 // clipped overflow
 p.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e);if(s.overflow==='hidden'||s.overflowX==='hidden'||s.overflowY==='hidden'){
  if(e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2)iss.push('CLIP '+lab(e)+' '+(e.scrollWidth-e.clientWidth)+'/'+(e.scrollHeight-e.clientHeight)+'px')}});
 // answer-line pitch: consecutive .ln in same parent, and first .ln vs preceding text
 const pitches=[];p.querySelectorAll('.ln').forEach(l=>{const r=l.getBoundingClientRect();pitches.push(MM(r.height))});
 const pv=[...new Set(pitches)].sort((a,b)=>a-b);
 // box/box overlap among block-level siblings of distinct subtrees (tips, qr, boxes, acts)
 const blocks=[...p.querySelectorAll('.act,.box,.tip,.qr,.tint,.rule,.grid2>div,.wag,.tools,.pass,.refl,.mala,.stn,.plan,.ticket,.cars,.letter,.dit,table')];
 for(let a=0;a<blocks.length;a++)for(let b=a+1;b<blocks.length;b++){const X=blocks[a],Y=blocks[b];if(X.contains(Y)||Y.contains(X))continue;
  const A=X.getBoundingClientRect(),B=Y.getBoundingClientRect();const ox=Math.min(A.right,B.right)-Math.max(A.left,B.left),oy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);
  if(ox>1&&oy>1)iss.push('BOX×BOX '+lab(X)+' / '+lab(Y)+' '+MM(ox)+'x'+MM(oy))}
 out.push({page:i+97,lines:pv,issues:[...new Set(iss)].slice(0,40)})});
const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre)},800)})</script>"""

here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "build", "unit.html")).read()
chk = os.path.join(here, "build", "q5probe.html")
open(chk, "w").write(src.replace("</body>", JS + "</body>"))
r = build.chrome(["--virtual-time-budget=9000", "--window-size=794,1123", "--dump-dom", "file://" + chk],
                 capture_output=True, text=True, timeout=480)
m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
want = {int(a) for a in sys.argv[1:]}
for row in json.loads(H.unescape(m.group(1))):
    if want and row["page"] not in want:
        continue
    print(row["page"], "line heights(mm):", row["lines"])
    for s in row["issues"]:
        print("   ", s)
