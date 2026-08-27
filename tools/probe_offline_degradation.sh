#!/usr/bin/env bash
# Prove the rail degrades honestly when Hermes is unreachable (the state a
# public deployment is in until HERMES_BASE_URL points somewhere real).
cd /c/Users/alexa/Documents/GitHub/prime-books || exit 1

cp .env.local .env.local.bak
printf 'HERMES_BASE_URL=http://127.0.0.1:9\nHERMES_API_KEY=dummy-unreachable-key\nHERMES_MODEL=z-ai/glm-5.2\nHERMES_PROVIDER=openrouter\n' > .env.local
echo "pointed at a dead port; waiting for vite to reload config..."
sleep 9
echo -n "health says: "
curl -s -m 10 http://127.0.0.1:5173/hermes/health
echo
cp .env.local.bak .env.local
rm -f .env.local.bak
echo "restored .env.local; waiting for reload..."
sleep 9
echo -n "health says: "
curl -s -m 10 http://127.0.0.1:5173/hermes/health
echo
