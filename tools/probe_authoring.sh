#!/usr/bin/env bash
# Can the reading assistant actually read and edit a manuscript in MEGA?
cd /c/Users/alexa/AppData/Local/hermes/profiles/primebooks-tutor || exit 1
KEY=$(grep '^API_SERVER_KEY=' .env | cut -d= -f2)
BASE=http://127.0.0.1:8643

SID=$(curl -s -m 20 -X POST $BASE/api/sessions \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"title\":\"authoring-probe-$(date +%s)\",\"model\":\"z-ai/glm-5.2\",\"provider\":\"openrouter\"}" \
  | python -c "import sys,json;print(json.load(sys.stdin)['session']['id'])")
echo "session: $SID"

ask() {
  echo
  echo "=== Q: $1"
  curl -sN -m 900 -X POST "$BASE/api/sessions/$SID/chat/stream" \
    -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
    -d "$(python -c "import json,sys;print(json.dumps({'input':sys.argv[1]}))" "$1")" \
  | python -c "
import sys, json
tools=[]; ans=''
for line in sys.stdin:
    line=line.rstrip('\n')
    if line.startswith('data:'):
        try: d=json.loads(line[5:].strip())
        except Exception: continue
        if 'tool_name' in d and d.get('tool_name') and d['tool_name']!='_thinking':
            t=d['tool_name']
            if not tools or tools[-1]!=t: tools.append(t)
        if d.get('completed') and d.get('content'): ans=d['content']
print('TOOLS USED:', ', '.join(tools) if tools else '(none)')
print('ANSWER:', ans[:700])
"
}

ask "Using your tools, list the markdown files in C:\\Users\\alexa\\Documents\\MEGA\\Projects\\Prime Books\\BOOKS\\3. Lower Secondary\\Year 07\\Humanities\\MARKDOWN and tell me how many there are."
ask "Read 06-SCHEME-MAP.md in that MARKDOWN folder and tell me the name of Unit 1."
