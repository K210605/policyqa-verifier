
def rrf(result_lists, k=60):
    scores={}
    for hits in result_lists:
        for rank, hit in enumerate(hits, start=1):
            scores[hit["id"]] = scores.get(hit["id"],0) + 1/(k+rank)
    return scores

if __name__ == "__main__":
    vector = [{"id": "A"},{"id": "B"},{"id":"C"}]
    bm25 = [{"id": "B"},{"id":"D"},{"id":"A"}]
    print(rrf([vector,bm25]))

