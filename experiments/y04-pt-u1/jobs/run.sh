#!/bin/bash
# Detached job runner: survives chat turns. Usage: nohup setsid jobs/run.sh &
cd /root/prime-books/experiments/y04-pt-u1
run_one() { n="$1"; [ -f "jobs/logs/$n.done" ] && exit 0
  hermes chat -Q --query-file "jobs/$n.md" -m anthropic/claude-opus-5.5 --provider openrouter \
    -t web,terminal,file,code_execution,vision,image_gen,tts --yolo --run-budget 5400 > "jobs/logs/$n.log" 2>&1
  echo "exit $? $(date +%H:%M)" > "jobs/logs/$n.done"; }
export -f run_one
xargs -P 7 -I{} bash -c 'run_one {}' < jobs/order.txt
echo ALL-DONE $(date +%H:%M) > jobs/logs/ALL.done
