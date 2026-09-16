#!/usr/bin/env python3
"""Run the house gate over the eight Year 1 books the fleet built.

They are parked outside the library (a card must never write a master), so the
gate is called directly rather than through the manifest.
"""
import importlib.util
import json
import sys
from datetime import datetime, timezone

spec = importlib.util.spec_from_file_location(
    "sc", "/root/prime-books/tools/standards_check.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)
lk = sc.lock()

SLUGS = ["y01-art-and-design", "y01-computing-and-robotics", "y01-english",
         "y01-german-a1a2", "y01-global-perspectives", "y01-mathematics",
         "y01-music-and-drama", "y01-science"]
rows = []
for slug in SLUGS:
    path = "/root/pb-y1-fleet-output/%s/book.pdf" % slug
    r = sc.check(path, slug + "-standard", lk, 1)
    rows.append(r)
    print("%-26s pp %-3s ok %-5s items-vs-plates %s"
          % (slug, r["pages"], r["ok"],
             [x["page"] for x in r["facts"].get("task_pages_items_and_plates_differ", [])]))
    for x in r["failures"]:
        if "plate" not in x:
            print("      FAIL:", x[:160])
json.dump({"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
           "books": rows}, open("/tmp/stdcheck-y1-fleet.json", "w"), indent=1)
clean = [r["slug"] for r in rows if r["ok"]]
print("\n%d/%d pass the gate as it now stands: %s" % (len(clean), len(rows), clean))
sys.exit(0)
