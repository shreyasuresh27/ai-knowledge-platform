from pypdf import PdfReader

# Step 1: Read the PDF (same as before)
reader = PdfReader("documents/COMPUTER SCIENCE AND ENGINEERING S7 & S8.pdf")
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Step 2: Break the text into overlapping chunks
def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # move forward, but overlap a bit
    return chunks

chunks = chunk_text(full_text)

# Step 3: Show results
print(f"Total chunks created: {len(chunks)}")
print("---- First chunk ----")
print(chunks[0])
print("\n---- Second chunk (notice the overlap at the start) ----")
print(chunks[1])