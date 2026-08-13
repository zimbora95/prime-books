#!/usr/bin/env bash
# Run this ON THE VM. It verifies the instance is fit to back the public rail,
# reading the key from the VM's own .env so the key never enters a chat.
#
#   curl -fsSL https://raw.githubusercontent.com/zimbora95/prime-books/main/tools/verify_on_vm.sh | bash
set -u
PORT=8643
ENV_FILE="$HOME/.hermes/.env"
BASE="http://127.0.0.1:$PORT"
MODEL="${HERMES_MODEL:-z-ai/glm-5.2}"
PROVIDER="${HERMES_PROVIDER:-openrouter}"

KEY=$(grep -E '^API_SERVER_KEY=' "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2-)
if [ -z "${KEY:-}" ]; then
  echo "FAIL no API_SERVER_KEY in $ENV_FILE"
  exit 1
fi

pass=0; fail=0
ok()  { echo "  ok   $1"; pass=$((pass+1)); }
bad() { echo "  FAIL $1"; fail=$((fail+1)); }

echo "=== 1. health ==="
curl -s -m 10 "$BASE/health" | grep -q '"status"' \
  && ok "gateway answering on $PORT" || bad "no /health"

echo "=== 2. capabilities the rail needs ==="
CAP=$(curl -s -m 20 -H "Authorization: Bearer $KEY" "$BASE/v1/capabilities")
for f in session_create session_chat_stream; do
  echo "$CAP" | grep -q "$f" && ok "$f advertised" || bad "$f MISSING"
done

echo "=== 3. NOT a public shell (the important one) ==="
TOOLS=$(curl -s -m 20 -H "Authorization: Bearer $KEY" "$BASE/v1/capabilities" \
  | python3 -c "
import sys, json
try: d = json.load(sys.stdin)
except Exception: print('?'); raise SystemExit
print(json.dumps(d))" 2>/dev/null)
if echo "$TOOLS" | grep -qiE '\"(terminal|write_file|patch|execute_code)\"'; then
  bad "terminal/file tools reachable from the internet"
else
  ok "no terminal/file tools advertised"
fi
grep -A6 'platform_toolsets:' "$HOME/.hermes/config.yaml" 2>/dev/null \
  | grep -qE '^\s+-\s+safe' && ok "config pins api_server to [safe]" \
  || bad "api_server toolset is not [safe] in config.yaml"

echo "=== 4. one real streamed turn ==="
SID=$(curl -s -m 25 -X POST "$BASE/api/sessions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"title\":\"pb-vm-verify-$(date +%s)\",\"model\":\"$MODEL\",\"provider\":\"$PROVIDER\"}" \
  | python3 -c "
import sys, json
try: print(json.load(sys.stdin)['session']['id'])
except Exception: print('')")
if [ -z "$SID" ]; then
  bad "could not create a session (is $MODEL a valid model id for $PROVIDER?)"
else
  ok "session created"
  ANS=$(curl -sN -m 180 -X POST "$BASE/api/sessions/$SID/chat/stream" \
    -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
    -d '{"input":"Reply with exactly: RAIL-OK"}' \
    | python3 -c "
import sys, json
out=''
for l in sys.stdin:
    if l.startswith('data:'):
        try: d=json.loads(l[5:].strip())
        except Exception: continue
        if d.get('completed') and d.get('content'): out=d['content']
print(out.strip()[:60])")
  echo "$ANS" | grep -q "RAIL-OK" && ok "model answered: $ANS" \
    || bad "stream returned: '$ANS'"
fi

echo
echo "passed $pass, failed $fail"
if [ "$fail" -eq 0 ]; then
  cat <<EOF

READY. In Vercel set:
  HERMES_BASE_URL = http://$(curl -s -m 5 -H 'Metadata-Flavor: Google' \
    http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip):$PORT
  HERMES_MODEL    = $MODEL
  HERMES_PROVIDER = $PROVIDER
  HERMES_API_KEY  = (read it with: grep API_SERVER_KEY $ENV_FILE )
Then REDEPLOY: Vercel only picks up new variables on a fresh deployment.
EOF
fi
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
