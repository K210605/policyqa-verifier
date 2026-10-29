import json
from loader import load_pdf
def chunk_text(text, size, overlap):
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    chunks =[]
    step = size-overlap
    for start in range(0, len(text), step):
                if start > 0 and start + overlap >= len(text):
                   break
                chunks.append(text[start:start+size])
    return chunks

def chunk_pages(pages,size=800,overlap=100):
     all_chunks = []
     for source, page,text in pages:
          text = " ".join(text.split())
          pieces = chunk_text(text,size,overlap)
          for chunk_number, piece in enumerate(pieces, start=1):
               all_chunks.append({
                     "id":f"{source.replace('.pdf','')}-p{page}-c{chunk_number}",
                     "text":piece,
                     "source":source,
                     "page":page,
               })
     return all_chunks

if __name__ == "__main__":
    files = ["nist_csf.pdf", "dpdp_act.pdf", "iso27001_summary.pdf"]
    all_chunks = []
    for name in files:
        pages = load_pdf("data/raw/" + name)
        chunks = chunk_pages(pages)
        print(name, len(chunks))
        all_chunks.extend(chunks)

    with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print("total", len(all_chunks))





