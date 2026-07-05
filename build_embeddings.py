import os
import json
import time
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Step 1: Read PDF
reader = PdfReader("documents/COMPUTER SCIENCE AND ENGINEERING S7 & S8.pdf")
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Step 2: Chunk it
def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(full_text)
print(f"Total chunks to embed: {len(chunks)}")

# Step 3: Embed each chunk, one at a time, and store the results
data = []  # will hold {"text": ..., "embedding": [...]} for each chunk

for i, chunk in enumerate(chunks):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )
    embedding = result.embeddings[0].values
    data.append({
        "text": chunk,
        "embedding": embedding
    })
    print(f"Embedded chunk {i+1}/{len(chunks)}")
    time.sleep(0.5)  # small pause so we don't overwhelm the free tier limits

# Step 4: Save everything to a file so we never have to redo this
with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

print("Done! Saved to embeddings.json")