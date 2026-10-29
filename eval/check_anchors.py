import json

with open("data/processed/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)
with open("eval/questions.json", encoding="utf-8") as f:
    questions = json.load(f)

for i, item in enumerate(questions, start=1):
    if item["anchor"] is None:
        continue
    anchor = item["anchor"].lower()
    n = sum(1 for c in chunks if anchor in c["text"].lower())
    print(i, n, item["anchor"])