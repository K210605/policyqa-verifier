import json 
import chromadb
from sentence_transformers import SentenceTransformer

def build_index():
    with open("data/processed/chunks.json",encoding="utf-8") as f:
        chunks = json.load(f)

    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "page": c["page"]} for c in chunks]
    print(len(ids), len(set(ids)))
    print(metadatas[0])
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection("policyqa")

    collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
    print("indexed:", collection.count())

if __name__ == "__main__":
    build_index()