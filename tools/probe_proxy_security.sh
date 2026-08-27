#!/usr/bin/env bash
# Security probes for the Prime Books reading-assistant proxy.
# Each must FAIL to reach Hermes, or the trust boundary is broken.
cd /c/Users/alexa/Documents/GitHub/prime-books || exit 1

echo "1) unknown verb (arbitrary endpoint attempt):"
curl -s -m 8 -o /tmp/p1.txt -w "   /hermes/runs -> HTTP %{http_code}\n" \
  -X POST http://127.0.0.1:5173/hermes/runs \
  -H "Content-Type: application/json" -d '{"input":"hi"}'
echo "   body: $(head -c 120 /tmp/p1.txt)"

echo "2) path traversal in sessionId:"
curl -s -m 8 -X POST http://127.0.0.1:5173/hermes/chat \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"../../v1/runs","input":"x"}' | head -c 160
echo

echo "3) key leakage in proxy responses:"
KEY=$(grep HERMES_API_KEY .env.local | cut -d= -f2)
if curl -s -m 8 http://127.0.0.1:5173/hermes/health | grep -q "$KEY"; then
  echo "   LEAK: key present in response"
else
  echo "   OK: key absent from proxy response"
fi

echo "4) is .env.local served as a static file?"
curl -s -m 8 -o /tmp/p4.txt -w "   /.env.local -> HTTP %{http_code}\n" \
  http://127.0.0.1:5173/.env.local
if grep -q "HERMES_API_KEY" /tmp/p4.txt 2>/dev/null; then
  echo "   LEAK: key downloadable over HTTP"
else
  echo "   OK: no key in body"
fi

echo "5) does the key appear anywhere in the served page?"
if curl -s -m 8 http://127.0.0.1:5173/ | grep -q "$KEY"; then
  echo "   LEAK: key in index.html"
else
  echo "   OK: key absent from index.html"
fi
