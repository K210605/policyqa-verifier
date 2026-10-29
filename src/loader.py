import os 
from pypdf import PdfReader

def load_pdf(path):
    pages = []
    reader = PdfReader(path)
    source = os.path.basename(path)

    for page_number , page in enumerate(reader.pages,start=1):
        text = page.extract_text() or ""
        if not text.strip():
            continue
        pages.append((source, page_number, text))

    return pages 
if __name__ == "__main__":
        files = ["nist_csf.pdf", "dpdp_act.pdf", "iso27001_summary.pdf"]
        for name in files:
            path = "data/raw/" + name
            result = load_pdf(path)
            print(f"{name}: {len(result)} packets")