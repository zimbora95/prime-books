#!/usr/bin/env python3
"""Generate an image via OpenRouter gpt-image-2 and save it as a PNG.

Usage (run with /root/prime-books/.venv/bin/python):
  python pb_image_gen.py "a spiral galaxy, watercolour style" /tmp/out.png --size 1024x1024

Reads OPENROUTER_API_KEY from /root/.hermes/.env. Prints the saved path.
The OpenRouter images endpoint returns b64_json payloads (no URL), so this
script exists: curl alone is awkward for multi-MB base64 bodies.
"""
import argparse, base64, json, sys, urllib.request, urllib.error

ENV_PATH = "/root/.hermes/.env"
API = "https://openrouter.ai/api/v1/images/generations"
MODEL = "openai/gpt-image-2"


def key():
    for line in open(ENV_PATH):
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("OPENROUTER_API_KEY not found in " + ENV_PATH)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("out")
    ap.add_argument("--size", default="1024x1024")
    a = ap.parse_args()

    body = json.dumps({
        "model": MODEL,
        "prompt": a.prompt,
        "size": a.size,
        "quality": "medium",  # cost/speed sweet spot per user preference
    }).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": "Bearer " + key(),
        "Content-Type": "application/json",
    })
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit("OpenRouter error %s: %s" % (e.code, e.read().decode()[:300]))
    item = (d.get("data") or [{}])[0]
    b64 = item.get("b64_json")
    if not b64:
        sys.exit("No image in response: " + json.dumps(d)[:300])
    raw = base64.b64decode(b64)
    with open(a.out, "wb") as f:
        f.write(raw)
    print(a.out)


if __name__ == "__main__":
    main()
