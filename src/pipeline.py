from retrievers import vector_search, hybrid_search
from reranker import rerank


def retrieve(question, mode="v3", k=5):
    if mode == "v1":
        return vector_search(question, k=k)
    if mode == "v2":
        return hybrid_search(question, k=k)
    if mode == "v3":
        hits = hybrid_search(question, k=20)
        return rerank(question, hits, k=k)
    raise ValueError("mode must be v1, v2 or v3")


if __name__ == "__main__":
    for mode in ["v1", "v2", "v3"]:
        ids = [h["id"] for h in retrieve("What does GV.SC-01 say?", mode, k=3)]
        print(mode, ids)