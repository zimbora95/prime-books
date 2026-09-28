"""Print the model the book matter is built from (QA aid)."""
import sys

import build as B

M = B.model()
what = sys.argv[1:] or ["units", "qrs", "gloss", "read", "refs"]
if "units" in what:
    for u in M["units"]:
        print("\n##", u["n"], u["title"], "| built:", u["built"])
        for e in u["entries"]:
            print("  ", e["page"], e["label"], "|", " · ".join(e["subs"])[:170])
if "qrs" in what:
    print()
    for q in M["qrs"]:
        print(q["page"], q["title"], "|", q["short"][:100], "|", q["label"][:80])
if "gloss" in what:
    print()
    for p in M["gloss_pages"]:
        for g in p:
            print(g["page"], "PROV" if g["provisional"] else "    ", g["term"], "—", g["def"][:90])
if "read" in what:
    print()
    for r in M["readings"]:
        print(r)
if "refs" in what:
    print()
    for k, v in M["refs"].items():
        for s in v:
            print(k, s[:160])
