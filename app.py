import os
import json
import numpy as np
import streamlit as st
from google import genai
from google.genai import types

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Load embeddings once
@st.cache_resource
def load_data():
    with open("embeddings.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

def embed_text(text):
    result = client.models.embed_content(model="gemini-embedding-001", contents=text)
    return result.embeddings[0].values

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

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

def calculate(expression: str) -> str:
    """Evaluates a basic math expression, like '25 * 4', and returns the result."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

tools = [search_syllabus, calculate]

# ---- Streamlit UI starts here ----
st.set_page_config(page_title="KTU Syllabus Assistant", page_icon="📘")
st.title("📘 KTU S7,S8 CSE Syllabus Assistant")
st.caption("Ask me anything about your S7 or S8 syllabus — course outcomes, modules, textbooks, and more.")

# Keep chat history across interactions
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(tools=tools)
    )
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box at the bottom
user_input = st.chat_input("Ask a question about your syllabus...")

if user_input:
    # Show user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                answer_text = response.text
            except Exception as e:
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    answer_text = "⚠️ Daily free quota reached for the AI model. Please try again after some time, or tomorrow."
                else:
                    answer_text = f"⚠️ Something went wrong: {e}"
            st.write(answer_text)

    st.session_state.messages.append({"role": "assistant", "content": answer_text})