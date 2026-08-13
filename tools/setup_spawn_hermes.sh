#!/usr/bin/env bash
# Run this INSIDE the spawn SSH session (spawn hermes gcp drops you there).
# It turns that Hermes into a public reading-assistant backend for
# prime-books-pi.vercel.app, then prints the two values Vercel needs.
set -u

PORT=8643
ENV_FILE="$HOME/.hermes/.env"
CFG="$HOME/.hermes/config.yaml"
mkdir -p "$HOME/.hermes"

# 1. A long random key. This is the only thing standing between the internet
#    and this agent, so it is generated, not chosen.
KEY=$(head -c 36 /dev/urandom | base64 | tr -d '/+=' | cut -c1-48)

# 2. API server on 0.0.0.0: bound to 127.0.0.1 it is unreachable from Vercel.
#    API_SERVER_MODEL_NAME is deliberately NOT set: it defaults to the profile
#    name and gets sent to the provider as a literal model id, which fails with
#    "400 <profile> is not a valid model ID".
python3 - "$ENV_FILE" "$KEY" "$PORT" <<'PY'
import re, sys, pathlib
path, key, port = sys.argv[1], sys.argv[2], sys.argv[3]
p = pathlib.Path(path)
txt = p.read_text() if p.exists() else ""
want = {
    "API_SERVER_ENABLED": "true",
    "API_SERVER_HOST": "0.0.0.0",
    "API_SERVER_PORT": port,
    "API_SERVER_KEY": key,
}
for k, v in want.items():
    line = f"{k}={v}"
    if re.search(rf"^{k}=.*$", txt, re.M):
        txt = re.sub(rf"^{k}=.*$", line, txt, flags=re.M)
    else:
        txt = txt.rstrip("\n") + "\n" + line + "\n"
txt = re.sub(r"^API_SERVER_MODEL_NAME=.*$\n?", "", txt, flags=re.M)
p.write_text(txt.lstrip("\n"))
print("wrote", path)
PY

# 3. READ-ONLY toolset for the public surface. This agent is reachable from the
#    internet: it must not have terminal or file tools.
python3 - "$CFG" <<'PY'
import sys, pathlib, re
p = pathlib.Path(sys.argv[1])
txt = p.read_text() if p.exists() else ""
block = (
    "platform_toolsets:\n"
    "  # Public reading assistant: reachable from the internet, so NO terminal\n"
    "  # and NO file tools. It answers about the page a reader is on.\n"
    "  api_server:\n"
    "    - safe\n"
)
if "platform_toolsets:" in txt:
    txt = re.sub(
        r"^platform_toolsets:\n(?:[ \t]+.*\n|\n)*", block, txt, count=1, flags=re.M
    )
else:
    txt = txt.rstrip("\n") + "\n\n" + block
p.write_text(txt)
print("wrote", sys.argv[1])
PY

# 4. Start it so it survives this SSH session ending.
hermes gateway install >/dev/null 2>&1 || hermes gateway restart >/dev/null 2>&1 || true
sleep 8

IP=$(curl -s -m 10 -H 'Metadata-Flavor: Google' \
  http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip 2>/dev/null)
[ -z "$IP" ] && IP=$(curl -s -m 10 https://api.ipify.org 2>/dev/null)

echo
echo "=== local health check ==="
curl -s -m 8 "http://127.0.0.1:$PORT/health" || echo "  NOT RESPONDING - run: hermes gateway status"
echo
echo "=================================================================="
echo "PASTE THESE TO HERMES:"
echo
echo "  HERMES_BASE_URL = http://$IP:$PORT"
echo "  HERMES_API_KEY  = $KEY"
echo "=================================================================="
echo
echo "STILL TO DO on your laptop (GCP blocks inbound ports by default):"
echo "  gcloud compute firewall-rules create hermes-api \\"
echo "    --allow tcp:$PORT --source-ranges 0.0.0.0/0 \\"
echo "    --description 'Prime Books reading assistant'"
