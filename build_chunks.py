import os
import json
import glob
from pypdf import PdfReader

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# Find every PDF inside the documents folder automatically
pdf_files = glob.glob("documents/*.pdf")
print(f"Found {len(pdf_files)} PDF files")

all_chunks = []  # will hold {"text": ..., "source": ...} for every chunk, across all PDFs

for pdf_path in pdf_files:
    department_name = os.path.basename(pdf_path).replace(".pdf", "")
    print(f"Processing: {department_name}")

    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()

    chunks = chunk_text(full_text)
    for chunk in chunks:
        all_chunks.append({
            "text": chunk,
            "source": department_name
        })
    print(f"  -> {len(chunks)} chunks created")

print(f"\nTotal chunks across all departments: {len(all_chunks)}")

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f)

print("Saved to chunks.json")