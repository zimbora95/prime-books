#!/usr/bin/env bash
# Give the spawned Hermes an LLM provider.
#
# Symptom this fixes: /api/sessions/<id>/chat/stream emits
#   event: error  {"message": "No LLM provider configured. Run `hermes model` ..."}
# and the non-streaming /chat returns 500. The spawn installed Hermes but no
# OpenRouter credential reached /root/.hermes/, so every turn dies before the
# model is called. Per-session model/provider pins cannot rescue it: with no
# credential there is nothing to authenticate with.
#
#   curl -fsSL https://raw.githubusercontent.com/zimbora95/prime-books/main/tools/fix_spawn_provider.sh | bash -s -- sk-or-v1-YOURKEY
set -u
ORKEY="${1:-${OPENROUTER_API_KEY:-}}"
MODEL="${2:-z-ai/glm-5.2}"
ENV_FILE="$HOME/.hermes/.env"
CFG="$HOME/.hermes/config.yaml"

if [ -z "$ORKEY" ]; then
  cat <<'USAGE'
Need an OpenRouter API key.

  1. https://openrouter.ai/keys  ->  create key  (starts sk-or-v1-)
  2. Re-run:
     curl -fsSL https://raw.githubusercontent.com/zimbora95/prime-books/main/tools/fix_spawn_provider.sh | bash -s -- sk-or-v1-YOURKEY

Or, if the spawn already stored one somewhere, look for it:
     grep -rIl 'sk-or-v1' /root /etc 2>/dev/null | head
USAGE
  exit 2
fi

mkdir -p "$HOME/.hermes"
python3 - "$ENV_FILE" "$ORKEY" <<'PY'
import re, sys, pathlib
path, key = sys.argv[1], sys.argv[2]
p = pathlib.Path(path)
txt = p.read_text() if p.exists() else ""
line = f"OPENROUTER_API_KEY={key}"
if re.search(r"^OPENROUTER_API_KEY=.*$", txt, re.M):
    txt = re.sub(r"^OPENROUTER_API_KEY=.*$", line, txt, flags=re.M)
else:
    txt = txt.rstrip("\n") + "\n" + line + "\n"
p.write_text(txt.lstrip("\n"))
print("wrote OPENROUTER_API_KEY to", path)
PY

# Pin provider + model at the instance level too, so a session that omits them
# still resolves. Keys stay in .env; config.yaml holds no secret.
python3 - "$CFG" "$MODEL" <<'PY'
import pathlib, re, sys
p, model = pathlib.Path(sys.argv[1]), sys.argv[2]
txt = p.read_text() if p.exists() else ""
for key, val in (("provider", "openrouter"), ("model", model)):
    if re.search(rf"^{key}:.*$", txt, re.M):
        txt = re.sub(rf"^{key}:.*$", f"{key}: {val}", txt, flags=re.M)
    else:
        txt = f"{key}: {val}\n" + txt
p.write_text(txt)
print("pinned provider: openrouter, model:", model)
PY

hermes gateway restart >/dev/null 2>&1 || hermes gateway install >/dev/null 2>&1 || true
sleep 10

PORT=8643
KEY=$(grep -E '^API_SERVER_KEY=' "$ENV_FILE" | head -1 | cut -d= -f2-)
echo
echo "=== does a real turn work now? ==="
SID=$(curl -s -m 25 -X POST "http://127.0.0.1:$PORT/api/sessions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"title\":\"provider-fix-$(date +%s)\",\"model\":\"$MODEL\",\"provider\":\"openrouter\"}" \
  | python3 -c "
import sys, json
try: print(json.load(sys.stdin)['session']['id'])
except Exception: print('')")
if [ -z "$SID" ]; then
  echo "  FAIL could not create a session"
  exit 1
fi
curl -sN -m 180 -X POST "http://127.0.0.1:$PORT/api/sessions/$SID/chat/stream" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"input":"Reply with exactly: PROVIDER-OK"}' \
  | python3 -c "
import sys, json
err, final, acc = '', '', ''
for line in sys.stdin:
    if not line.startswith('data:'):
        continue
    try: d = json.loads(line[5:].strip())
    except Exception: continue
    if d.get('tool_name'):
        continue
    if isinstance(d.get('message'), str) and 'provider' in d['message'].lower():
        err = d['message']
    if isinstance(d.get('delta'), str):
        acc += d['delta']
    if d.get('content'):
        final = d['content']
out = (final or acc).strip()
if err:
    print('  FAIL still no provider:', err)
elif 'PROVIDER-OK' in out:
    print('  ok   model answered:', out[:60])
else:
    print('  ??   got:', repr(out[:120]))
"
