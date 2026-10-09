#!/bin/sh
# Re-cut every stale BookVault wrap, in two workers (2 cores), humanities first.
# Worker A: the two humanities backs + the rest of Y7-9.  Worker B: Y1-6 + Y10-13.
cd /root/prime-books || exit 1
PY=/root/prime-books/.venv/bin/python
mkdir -p /root/pbwork-vault

A="y08-humanities y09-humanities \
y07-art-and-design y07-computing-and-robotics y07-computing-structured y07-english \
y07-global-perspectives y07-mathematics y07-physical-education y07-portuguese-1st \
y07-portuguese-2nd y07-science y07-spanish \
y08-art-and-design y08-english y08-mathematics y08-physical-education \
y08-portuguese-2nd y08-science y08-spanish \
y09-art-and-design y09-english y09-mathematics y09-music-and-drama \
y09-physical-education y09-portuguese y09-portuguese-2nd y09-science y09-spanish"

B="y01-art-and-design y01-computing-and-robotics y01-english y01-german-a1a2 \
y01-global-perspectives y01-mathematics y01-music-and-drama y01-physical-education \
y01-physical-education-standard y01-science y01-spanish-a1a2 \
y02-art-and-design y02-computing-and-robotics y02-english y02-german-b1b2 \
y02-global-perspectives y02-music-and-drama y02-physical-education y02-science \
y03-art-and-design y03-computing-and-robotics y03-global-perspectives y03-mathematics \
y03-physical-education y03-portuguese \
y04-art-and-design y04-computing-and-robotics y04-english y04-global-perspectives \
y04-mathematics y04-physical-education y04-portuguese y04-science \
y05-art-and-design y05-english y05-global-perspectives y05-mathematics \
y05-physical-education y05-portuguese \
y06-art-and-design y06-global-perspectives y06-mathematics y06-physical-education \
y06-portuguese \
y10-business-btec-l2 y10-physical-education y10-portuguese-1st \
y10-portuguese-1st-igcse y10-spanish-1st-igcse \
y11-physical-education y11-portuguese-1st \
y12-physical-education y12-portuguese-a-level y12-spanish-a-level \
y13-physical-education"

PB_WRAP_STATUS=/root/pbwork-vault/wrap_status_A.json \
  $PY tools/sweep_bookvault_wraps.py $A > /root/pbwork-vault/wrap_A.log 2>&1 &
echo "worker A pid $!"
PB_WRAP_STATUS=/root/pbwork-vault/wrap_status_B.json \
  $PY tools/sweep_bookvault_wraps.py $B > /root/pbwork-vault/wrap_B.log 2>&1 &
echo "worker B pid $!"
wait
echo "=== both workers done $(date '+%F %T') ==="
tail -3 /root/pbwork-vault/wrap_A.log
tail -3 /root/pbwork-vault/wrap_B.log