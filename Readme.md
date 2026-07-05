# 📘 KTU S7 CSE Syllabus Assistant

An AI-powered knowledge assistant that answers natural-language questions about the KTU (APJ Abdul Kalam Technological University) Semester 7 & 8 CSE syllabus — course outcomes, modules, textbooks, credits, and more — using Retrieval-Augmented Generation (RAG) and a tool-using AI agent.

**🔗 Live demo:** https://shreyasuresh27-ai-knowledge-platform-app-q6fnuk.streamlit.app/

---

## What it does

Ask it things like:
- "What are the course outcomes of Artificial Intelligence?"
- "What textbook is recommended for CST401?"
- "What is the course code for Compiler Lab?"

Instead of relying on general AI knowledge (which could be outdated or wrong), the assistant **retrieves the exact relevant section of the actual syllabus PDF** before answering — so responses are grounded in the real document, not guessed.

## How it works (architecture)

```
PDF Syllabus → Text Extraction → Chunking → Embeddings → Vector Search → AI Agent → Answer
```

1. **Ingestion** — The 440-page KTU CSE syllabus PDF is parsed and its text extracted using `pypdf`.
2. **Chunking** — Text is split into ~1000-character overlapping chunks (200-char overlap) so context isn't lost at chunk boundaries.
3. **Embeddings** — Each chunk is converted into a 3072-dimension vector using Google's `gemini-embedding-001` model, capturing semantic meaning rather than just keywords.
4. **Retrieval** — When a question is asked, it's embedded the same way, and compared against all stored chunk embeddings using **cosine similarity** to find the most relevant sections.
5. **Agent + Generation** — The top matching chunks are passed to `gemini-2.5-flash`, which is also equipped with tool-calling capability (e.g. a calculator tool), allowing it to decide whether a question needs syllabus lookup, computation, or both.
6. **Interface** — A Streamlit web app provides a chat interface, with conversation history and graceful handling of API rate limits.

## Why these design choices

- **Chunking size (1000 chars, 200 overlap):** balances context completeness against retrieval precision — large enough to preserve meaning, small enough for accurate matching.
- **Cosine similarity over keyword search:** allows the system to match on *meaning*, not exact words — e.g. a question about "learning techniques" correctly retrieves content phrased as "supervised and unsupervised learning."
- **Tool-calling agent architecture:** rather than a single fixed pipeline, the AI model itself decides which capability (retrieval vs. computation) a question needs — a foundational pattern in modern agentic AI systems.
- **Resumable, checkpointed ingestion:** for scaling to multiple departments, the embedding pipeline saves progress every 20 chunks and can resume after interruptions or API rate limits — a practical necessity when working within free-tier API quotas.

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python |
| LLM & Embeddings | Google Gemini API (`gemini-2.5-flash`, `gemini-embedding-001`) |
| Vector similarity | NumPy (cosine similarity) |
| PDF processing | pypdf |
| Web interface | Streamlit |
| Deployment | Streamlit Community Cloud |

## Known limitations

- Broad/aggregate questions (e.g. "list every subject in the syllabus") are harder to answer well, since the answer is scattered across many chunks rather than contained in the top few retrieved — a well-known limitation of basic RAG that would typically be addressed with hybrid search or metadata filtering.
- Currently scoped to the CSE department syllabus (S7 & S8); a multi-department version covering all KTU branches is in progress.
- Running on Google Gemini's free tier, which has daily request limits.

## Running it locally

```bash
git clone https://github.com/shreyasuresh27/ai-knowledge-platform.git
cd ai-knowledge-platform
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

Then run:
```bash
streamlit run app.py
```

## Author

Shreya Suresh — [LinkedIn](https://linkedin.com/in/shreyasuresh-81b202299) · [GitHub](https://github.com/shreyasuresh27) · [Portfolio](https://shreyasuresh27.lovable.app)
