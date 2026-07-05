# 🎓 KTU AI Syllabus Assistant

An AI-powered chatbot that helps students quickly find information from KTU S7 & S8 syllabus documents using Retrieval-Augmented Generation (RAG) and Google's Gemini API.

## 🚀 Features

- 📄 Searches KTU syllabus PDFs using semantic search
- 🤖 AI-powered question answering with Gemini 2.5 Flash
- 🔍 Embedding-based document retrieval
- 🧠 RAG (Retrieval-Augmented Generation) architecture
- 🧮 Built-in calculator tool for academic calculations
- 💻 Simple and interactive Streamlit web interface

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Gemini Embeddings
- NumPy
- JSON
- python-dotenv

## 📂 Project Structure

```
AI-KNOWLEDGE-PLATFORM/
│
├── app.py
├── agent.py
├── rag.py
├── search.py
├── build_chunks.py
├── build_embeddings.py
├── read_pdf.py
├── documents/
├── chunks.json
├── embeddings.json
└── .gitignore
```

## ⚙️ How It Works

1. Reads KTU syllabus PDFs.
2. Splits the content into text chunks.
3. Generates embeddings using Gemini Embedding API.
4. Stores embeddings in JSON files.
5. Retrieves the most relevant chunks for user queries.
6. Uses Gemini 2.5 Flash to generate accurate answers.


## 👩‍💻 Author

**Shreya S**

GitHub: https://github.com/shreyasuresh27