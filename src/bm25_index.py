import json
import pickle
from rank_bm25 import BM25Okapi
from tokenizer import tokenize


def build_bm25():
    with open("data/processed/chunks.json", encoding="utf-8") as f:
        chunks = json.load(f)

    ids = [c["id"] for c in chunks]
    tokenized = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)

    with open("data/processed/bm25.pkl", "wb") as f:
        pickle.dump({"bm25": bm25, "ids": ids}, f)
    print("bm25 indexed:", len(ids))


if __name__ == "__main__":
    build_bm25()