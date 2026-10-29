from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(question, hits, k=5):
    pairs = [(question, h["text"]) for h in hits]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, hits), key=lambda pair: pair[0], reverse=True)
    return [hit for score, hit in ranked[:k]]


if __name__ == "__main__":
    from retrievers import hybrid_search

    target = "nist_csf-p22-c3"
    for q in ["What does GV.SC-01 say?", "GV.SC-01"]:
        hits = hybrid_search(q, k=20)
        ids = [h["id"] for h in rerank(q, hits, k=20)]
        rank = ids.index(target) + 1 if target in ids else "not in top 20"
        print(q, "->", rank)