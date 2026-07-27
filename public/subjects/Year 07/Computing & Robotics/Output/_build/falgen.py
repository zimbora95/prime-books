"""fal.ai gpt-image-2 generator for Prime Books.
Usage: python falgen.py <jobs.json>
jobs.json = [{"name":"...", "prompt":"...", "size":"1024x1024"|"1536x1024"|"1024x1536"}]
Writes PNGs into the Images dir, skips ones already present.
"""
import os, sys, json, time, base64, pathlib, urllib.request, urllib.error
import concurrent.futures as cf

ENV = pathlib.Path(os.environ.get('LOCALAPPDATA', r'C:\Users\alexa\AppData\Local')) / 'hermes' / '.env'
KEY = None
for line in ENV.read_text(encoding='utf-8', errors='replace').splitlines():
    if line.startswith('FAL_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break
if not KEY:
    sys.exit('FAL_KEY not found')

ENDPOINT = 'https://fal.run/openai/gpt-image-2'
# fal's gpt-image-2 takes named size enums, NOT "1024x1024" pixel strings.
SIZES = {'square_hd', 'square', 'portrait_4_3', 'portrait_16_9',
         'landscape_4_3', 'landscape_16_9', 'auto'}
IMAGES = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(__file__).parent.parent / 'Images'
IMAGES.mkdir(parents=True, exist_ok=True)


def post(url, payload, timeout=600):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Key {KEY}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def gen(job):
    name = job['name']
    dest = IMAGES / f'{name}.png'
    if dest.exists() and dest.stat().st_size > 5000:
        return (name, 'skip', dest.stat().st_size)
    size = job.get('size', 'square_hd')
    if size not in SIZES:
        size = {'1024x1024': 'square_hd', '1536x1024': 'landscape_4_3',
                '1024x1536': 'portrait_4_3'}.get(size, 'square_hd')
    payload = {
        'prompt': job['prompt'],
        'image_size': size,
        'quality': 'medium',
        'num_images': 1,
        'output_format': 'png',
    }
    last = None
    for attempt in range(3):
        try:
            res = post(ENDPOINT, payload)
            imgs = res.get('images') or []
            if not imgs:
                last = f'no images: {str(res)[:200]}'
                continue
            u = imgs[0].get('url', '')
            if u.startswith('data:'):
                raw = base64.b64decode(u.split(',', 1)[1])
            else:
                with urllib.request.urlopen(u, timeout=300) as r:
                    raw = r.read()
            dest.write_bytes(raw)
            return (name, 'ok', len(raw))
        except urllib.error.HTTPError as e:
            last = f'HTTP {e.code}: {e.read()[:300].decode(errors="replace")}'
        except Exception as e:
            last = f'{type(e).__name__}: {e}'
        time.sleep(4 * (attempt + 1))
    return (name, 'FAIL', last)


def main():
    jobs = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
    results = []
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(gen, jobs):
            print(r, flush=True)
            results.append(r)
    bad = [r for r in results if r[1] == 'FAIL']
    print(f'\n=== {len(results)} jobs, {len(bad)} failed ===')
    for b in bad:
        print(b)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
