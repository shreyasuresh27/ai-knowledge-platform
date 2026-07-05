import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

text = "Machine learning algorithms learn patterns from data."

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text
)

embedding = result.embeddings[0].values

print(f"Type of result: {type(embedding)}")
print(f"How many numbers in this embedding: {len(embedding)}")
print(f"First 10 numbers: {embedding[:10]}")