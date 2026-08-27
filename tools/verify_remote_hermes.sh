#!/usr/bin/env bash
# Prove a remote Hermes can back the Prime Books rail, BEFORE touching Vercel.
#
#   bash tools/verify_remote_hermes.sh http://34.1.2.3:8643 <API_KEY>
#
# Checks reachability, auth, the session endpoints the rail needs, a real
# streamed turn, and that the instance is NOT exposing a shell to the internet.
set -u
BASE="${1:-}"
KEY="${2:-}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "usage: bash tools/verify_remote_hermes.sh <base-url> <api-key>"
  exit 2
fi
BASE="${BASE%/}"
pass=0; fail=0
ok()   { echo "  ok   $1"; pass=$((pass+1)); }
bad()  { echo "  FAIL $1"; fail=$((fail+1)); }

echo "=== 1. reachable from this machine ==="
H=$(curl -s -m 15 "$BASE/health" 2>/dev/null)
if echo "$H" | grep -q '"status"'; then ok "GET /health -> $H"
else bad "no /health response (firewall? gateway down? wrong host/port?)"; echo "$H"; fi

echo "=== 2. the key is required and works ==="
UN=$(curl -s -m 15 -o /dev/null -w '%{http_code}' "$BASE/v1/capabilities")
[ "$UN" = "401" ] || [ "$UN" = "403" ] && ok "unauthenticated /v1/capabilities -> $UN" \
  || bad "unauthenticated /v1/capabilities -> $UN (expected 401/403; is it open?)"
CAP=$(curl -s -m 20 -H "Authorization: Bearer $KEY" "$BASE/v1/capabilities")
echo "$CAP" | grep -q 'session_create' && ok "authenticated, session_create advertised" \
  || bad "no session_create in capabilities (wrong key, or older build)"

echo "=== 3. NOT a public shell ==="
if echo "$CAP" | grep -qiE '"terminal"|"write_file"|"patch"'; then
  bad "this instance advertises terminal/file tools to the internet -> set platform_toolsets.api_server: [safe]"
else
  ok "no terminal/file tools advertised"
fi

echo "=== 4. a real session + streamed turn (what the rail does) ==="
SID=$(curl -s -m 25 -X POST "$BASE/api/sessions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"title\":\"pb-verify-$(date +%s)\",\"model\":\"${HERMES_MODEL:-z-ai/glm-5.2}\",\"provider\":\"${HERMES_PROVIDER:-openrouter}\"}" \
  | python -c "import sys,json
try: print(json.load(sys.stdin)['session']['id'])
except Exception: print('')" 2>/dev/null)
if [ -z "$SID" ]; then
  bad "could not create a session (check HERMES_MODEL is a real model id)"
else
  ok "session created: $SID"
  ANS=$(curl -sN -m 180 -X POST "$BASE/api/sessions/$SID/chat/stream" \
    -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
    -d '{"input":"Reply with exactly: RAIL-OK"}' \
    | python -c "
import sys, json
out=''
for l in sys.stdin:
    if l.startswith('data:'):
        try: d=json.loads(l[5:].strip())
        except Exception: continue
        if d.get('completed') and d.get('content'): out=d['content']
print(out.strip()[:60])")
  echo "$ANS" | grep -q "RAIL-OK" && ok "streamed a real answer: $ANS" \
    || bad "stream gave: '$ANS' (SSE blocked, or model/provider wrong)"
fi

echo
echo "passed $pass, failed $fail"
if [ "$fail" -eq 0 ]; then
  echo
  echo "Set these in Vercel, then redeploy:"
  echo "  HERMES_BASE_URL = $BASE"
  echo "  HERMES_API_KEY  = <the key you passed>"
  echo "  HERMES_MODEL    = ${HERMES_MODEL:-z-ai/glm-5.2}"
  echo "  HERMES_PROVIDER = ${HERMES_PROVIDER:-openrouter}"
fi
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
