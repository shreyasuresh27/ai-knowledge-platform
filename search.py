import os
import json
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Step 1: Load our saved chunks + embeddings
with open("embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} chunks from storage")

# Step 2: Turn a question into an embedding
def embed_text(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

# Step 3: Cosine similarity function
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Step 4: Ask a question, find top matching chunks
question = "What are the course outcomes of Artificial Intelligence?"
question_embedding = embed_text(question)

# Compare question against every stored chunk
scored_chunks = []
for item in data:
    score = cosine_similarity(question_embedding, item["embedding"])
    scored_chunks.append((score, item["text"]))

# Sort by score, highest first
scored_chunks.sort(key=lambda x: x[0], reverse=True)

# Show top 3 matches
print(f"\nTop 3 matches for: '{question}'\n")
for score, text in scored_chunks[:3]:
    print(f"Score: {score:.4f}")
    print(text[:300])
    print("---")