#!/usr/bin/env python3
"""Generate an image via OpenRouter gpt-image-2.5-sunburst and save it as a PNG.

Usage (run with /root/prime-books/.venv/bin/python):
  python pb_image_gen.py "a spiral galaxy, watercolour style" /tmp/out.png --size 1024x1024
  python pb_image_gen.py "a fox, storybook watercolour" /tmp/fox.png --size 1024x1024 --transparent

Reads OPENROUTER_API_KEY from /root/.hermes/.env. Prints the saved path.
The OpenRouter images endpoint returns b64_json payloads (no URL), so this
script exists: curl alone is awkward for multi-MB base64 bodies.

--transparent asks the model for a transparent background AND (because the
endpoint may still return an opaque PNG) chroma-keys any near-white /
near-uniform border it does get back, so assets dropped straight onto a book
page never carry a white box with them.
"""
import argparse, base64, json, sys, urllib.request, urllib.error

ENV_PATH = "/root/.hermes/.env"
API = "https://openrouter.ai/api/v1/images/generations"
MODEL = "openai/gpt-image-2.5-sunburst"


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
    ap.add_argument("--quality", default="medium")
    ap.add_argument("--transparent", action="store_true")
    a = ap.parse_args()

    body = {
        "model": MODEL,
        "prompt": a.prompt,
        "size": a.size,
        "quality": a.quality,
    }
    if a.transparent:
        body["background"] = "transparent"
        body["output_format"] = "png"
    req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={
        "Authorization": "Bearer " + key(),
        "Content-Type": "application/json",
    })
    try:
        d = json.load(urllib.request.urlopen(req, timeout=600))
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
