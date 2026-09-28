#!/bin/bash
cd /root/prime-books/experiments/y05-portuguese-anthropic
run_one() { n="$1"; [ -f "jobs/logs/$n.done" ] && exit 0
  hermes chat -Q --query-file "jobs/$n.md" -m anthropic/claude-opus-5.5 --provider openrouter \
    -t web,terminal,file,code_execution,vision,image_gen,tts --yolo --run-budget 10800 \
    > "jobs/logs/$n.log" 2>&1
  echo "exit $? $(date +%H:%M)" > "jobs/logs/$n.done"; }
export -f run_one
xargs -P 3 -I{} bash -c 'run_one {}' <<< u6
echo DONE > jobs/logs/ALL6.done
