import os
import json
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

with open("embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def embed_text(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(question, top_k=8):
    question_embedding = embed_text(question)
    scored_chunks = []
    for item in data:
        score = cosine_similarity(question_embedding, item["embedding"])
        scored_chunks.append((score, item["text"]))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [text for score, text in scored_chunks[:top_k]]

def answer_question(question):
    # Step 1: Retrieve relevant chunks
    top_chunks = search(question)

    # Step 2: Build a prompt that includes those chunks as context
    context = "\n\n---\n\n".join(top_chunks)
    prompt = f"""Answer the question using ONLY the context below. 
If the answer isn't in the context, say "I don't know based on the syllabus."

Context:
{context}

Question: {question}

Answer:"""

    # Step 3: Ask Gemini to generate the final answer
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# Test it
question ="What textbooks are recommended for Artificial Intelligence?"
answer = answer_question(question)
print("Question:", question)
print("\nAnswer:")
print(answer)