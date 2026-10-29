import json
import sys

sys.path.insert(0, "src")
from pipeline import retrieve

K = 3
MODES = ["v1", "v2", "v3"]

with open("data/processed/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)
with open("eval/questions.json", encoding="utf-8") as f:
    questions = json.load(f)


def answerable(item):
    anchor = item["anchor"].lower()
    return any(c["source"] == item["source"] and anchor in c["text"].lower() for c in chunks)


def is_hit(item, hits):
    anchor = item["anchor"].lower()
    return any(h["source"] == item["source"] and anchor in h["text"].lower() for h in hits)


scored = []
for item in questions:
    if item["type"] == "out_of_scope":
        continue
    if answerable(item):
        scored.append(item)
    else:
        print("skipped (anchor not in text):", item["q"])

print("scored:", len(scored))

for mode in MODES:
    counts = {"id": [0, 0], "concept": [0, 0]}
    for item in scored:
        hit = is_hit(item, retrieve(item["q"], mode, k=K))
        counts[item["type"]][0] += int(hit)
        counts[item["type"]][1] += 1
    hit_total = counts["id"][0] + counts["concept"][0]
    total = counts["id"][1] + counts["concept"][1]
    print(
        mode,
        f"top-{K}: {hit_total}/{total}",
        f"| id {counts['id'][0]}/{counts['id'][1]}",
        f"| concept {counts['concept'][0]}/{counts['concept'][1]}",
    )