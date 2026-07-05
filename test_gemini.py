import os
from dotenv import load_dotenv
from google import genai

# Load the secret key from our .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Create a connection to Gemini using our key
client = genai.Client(api_key=api_key)

# Send a question and get a response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="In one sentence, explain what RAG means in AI."
)

# Print the answer
print(response.text)