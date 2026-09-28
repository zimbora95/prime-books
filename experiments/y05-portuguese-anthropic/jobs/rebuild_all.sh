#!/bin/bash
# Rebuild every unit after the static-font swap, sequentially (the host is loaded).
R=/root/prime-books/experiments/y05-portuguese-anthropic
PY=/root/.hermes/cache/scratch/exp-venv/bin/python
cd $R && echo "u1 start $(date +%T)" && timeout 900 $PY build.py > jobs/logs/rebuild-u1.log 2>&1; echo "u1 exit $?"
for u in u2 u3 u4 u5 u6 u7; do
  cd $R/$u && echo "$u start $(date +%T)" && timeout 1500 $PY build.py > $R/jobs/logs/rebuild-$u.log 2>&1; echo "$u exit $?"
done
cd $R && $PY - <<'E'
import pymupdf
for u in ["build","u2/build","u3/build","u4/build","u5/build","u6/build","u7/build"]:
    d=pymupdf.open(u+"/unit.pdf");fs={}
    for i,p in enumerate(d):
        for x in p.get_fonts():
            n=x[3].split("+")[-1] or "(noname)"; fs.setdefault((x[2],n),[]).append(i+1)
    print(u,d.page_count,{k:v[:6] for k,v in fs.items()})
E
echo REBUILD-DONE
