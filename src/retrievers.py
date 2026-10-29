import json
import pickle

import chromadb
from sentence_transformers import SentenceTransformer

from fusion import rrf
from tokenizer import tokenize

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("policyqa")

with open("data/processed/bm25.pkl", "rb") as f:
    saved = pickle.load(f)
bm25 = saved["bm25"]
bm25_ids = saved["ids"]

with open("data/processed/chunks.json", encoding="utf-8") as f:
    chunks_by_id = {c["id"]: c for c in json.load(f)}


def vector_search(question, k=5):
    result = collection.query(
        query_embeddings=model.encode([question]).tolist(),
        n_results=k,
    )
    ids = result["ids"][0]
    texts = result["documents"][0]
    metas = result["metadatas"][0]

    hits = []
    for chunk_id, text, meta in zip(ids, texts, metas):
        hits.append({
            "id": chunk_id,
            "text": text,
            "source": meta["source"],
            "page": meta["page"],
        })
    return hits


def bm25_search(question, k=5):
    scores = bm25.get_scores(tokenize(question))
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    hits = []
    for i in top:
        chunk = chunks_by_id[bm25_ids[i]]
        hits.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"],
        })
    return hits

def hybrid_search(question, k=5, pool=20):
    vec = vector_search(question, k=pool)
    kw = bm25_search(question, k=pool)
    scores = rrf([vec, kw])
    by_id = {h["id"]: h for h in vec + kw}
    top_ids = sorted(scores, key=scores.get, reverse=True)[:k]
    return [by_id[i] for i in top_ids]


if __name__ == "__main__":
    target = "nist_csf-p22-c3"
    questions = ["What does GV.SC-01 say?", "GV.SC-01"]
    searches = [
        ("vector", vector_search),
        ("bm25", bm25_search),
        ("hybrid", hybrid_search),
    ]
    for q in questions:
        print("Q:", q)
        for name, search in searches:
            ids = [h["id"] for h in search(q, k=20)]
            rank = ids.index(target) + 1 if target in ids else "not in top 20"
            print(" ", name, rank)