#!/usr/bin/env python3
"""Generate an image via fal.ai (FAL_KEY) and save as PNG.

Usage:
  pb_image_gen_fal.py "<prompt>" /tmp/out.png [--size 1024x1024] [--transparent]

Model: openai/gpt-image-2.5/sunburst/text-to-image (fal.ai endpoint id:
openai/gpt-image-2.5-sunburst-text-to-image). background: "transparent" is
supported in the advanced settings.
"""
import argparse, base64, json, sys, urllib.request, urllib.error, time

ENV_PATH = "/root/.hermes/profiles/primebooks-authoring/.env"
API = "https://fal.run/openai/gpt-image-2.5/sunburst/text-to-image"

def key():
    for line in open(ENV_PATH):
        if line.startswith("FAL_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("FAL_KEY not found in " + ENV_PATH)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("out")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--transparent", action="store_true")
    a = ap.parse_args()
    w, h = a.size.split("x")
    body = {
        "prompt": a.prompt,
        "image_size": {"width": int(w), "height": int(h)},
        "output_format": "png",
        "background": "transparent" if a.transparent else "opaque",
    }
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
        headers={"Authorization": "Key " + key(), "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=300)
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:800]); sys.exit(1)
    data = json.loads(r.read())
    # fal returns images list with b64_json or url
    imgs = data.get("images") or []
    if not imgs:
        print("no images in response:", json.dumps(data)[:500]); sys.exit(1)
    item = imgs[0]
    if item.get("b64_json"):
        raw = base64.b64decode(item["b64_json"])
    elif item.get("url"):
        raw = urllib.request.urlopen(item["url"], timeout=120).read()
    else:
        print("no usable image payload"); sys.exit(1)
    open(a.out, "wb").write(raw)
    print(a.out)

if __name__ == "__main__":
    main()
