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

--ref <image> keeps an EXISTING character on model. It sends the approved
character sheet to google/gemini-3-pro-image through the chat completions
endpoint as an image alongside the prompt, which is the only route that actually
holds the design: openai/gpt-image-2.5-sunburst accepts an "image" field on the
images endpoint and then silently ignores it, which is how a reference squirrel
comes back as a human child. Use --ref only for scene reuse; every new plate
stays on the images endpoint at quality medium.
"""
import argparse, base64, json, sys, urllib.request, urllib.error

ENV_PATH = "/root/.hermes/.env"
API = "https://openrouter.ai/api/v1/images/generations"
CHAT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-image-2.5-sunburst"
REF_MODEL = "google/gemini-3-pro-image"


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
    ap.add_argument("--ref", help="character sheet image to keep on model (uses %s)" % REF_MODEL)
    a = ap.parse_args()

    if a.ref:
        data = base64.b64encode(open(a.ref, "rb").read()).decode()
        mime = "image/png" if a.ref.lower().endswith(".png") else "image/jpeg"
        body = {
            "model": REF_MODEL,
            "modalities": ["image", "text"],
            "messages": [{"role": "user", "content": [
                {"type": "image_url",
                 "image_url": {"url": "data:%s;base64,%s" % (mime, data)}},
                {"type": "text", "text": a.prompt},
            ]}],
        }
        req = urllib.request.Request(CHAT, data=json.dumps(body).encode(), headers={
            "Authorization": "Bearer " + key(),
            "Content-Type": "application/json",
        })
        try:
            d = json.load(urllib.request.urlopen(req, timeout=600))
        except urllib.error.HTTPError as e:
            sys.exit("OpenRouter error %s: %s" % (e.code, e.read().decode()[:300]))
        msg = d["choices"][0]["message"]
        imgs = msg.get("images") or []
        if not imgs:
            sys.exit("No image in response: " + json.dumps(msg)[:300])
        raw = base64.b64decode(imgs[0]["image_url"]["url"].split(",", 1)[1])
        with open(a.out, "wb") as f:
            f.write(raw)
        print(a.out)
        return

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
