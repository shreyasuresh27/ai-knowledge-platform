import os
import json
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

with open("embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def embed_text(text):
    result = client.models.embed_content(model="gemini-embedding-001", contents=text)
    return result.embeddings[0].values

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---- TOOL 1: Search the syllabus ----
def search_syllabus(question: str) -> str:
    """Searches the KTU CSE S7 syllabus PDF for relevant content and returns matching text chunks."""
    question_embedding = embed_text(question)
    scored_chunks = []
    for item in data:
        score = cosine_similarity(question_embedding, item["embedding"])
        scored_chunks.append((score, item["text"]))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [text for score, text in scored_chunks[:3]]
    return "\n\n".join(top_chunks)

# ---- TOOL 2: Calculator ----
def calculate(expression: str) -> str:
    """Evaluates a basic math expression, like '25 * 4' or '180 * 0.25', and returns the result."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Tell Gemini these tools exist, using their function signatures + docstrings
tools = [search_syllabus, calculate]

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(tools=tools)
)

# Test it
question = "If a subject has 3 credits and each credit equals 15 hours, how many total hours is that?"
response = chat.send_message(question)
print("Question:", question)
print("Answer:", response.text)