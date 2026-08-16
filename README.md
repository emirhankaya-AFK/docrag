# DocRAG - Developer Documentation Tech Assistant Agent

[English](README.md) | [Türkçe](README_TR.md)

DocRAG is a complete, developer-focused documentation assistant and code synthesizer. It parses framework and library API documentations across HTML, Markdown, and PDF layouts, conducts semantic code searches, answers complex setup questions, resolves compilation and runtime errors using predefined trace mappings, and generates ready-to-run code snippets.

---

## Tech Stack
- **Backend API**: FastAPI + Uvicorn
- **RAG & Vector Storage**: ChromaDB + Gemini Embeddings (`models/embedding-001`)
- **LLM**: Gemini API (`gemini-2.0-flash`)
- **Doc Parsers**: BeautifulSoup (`bs4`), Markdown parser, PyMuPDF (`fitz`), and Pygments code highlighter
- **Version Tracking**: Semantic Versioning comparisons (`semver`)
- **Frontend Dashboard**: Streamlit

---

## Directory Structure
```
docrag/
├── backend/
│   ├── main.py              # FastAPI server entrypoint
│   ├── db.py                # SQLite database helper
│   ├── routes/              # FastAPI router endpoints
│   ├── agents/              # Custom LLM agents (Parsing, Search, QA, Examples, Error, Practices)
│   ├── services/            # Doc parsing, code extraction, version management, error databases, and RAG services
│   ├── models/              # Pydantic schemas
│   └── config/              # Prompts, frameworks catalog, error mappings
├── frontend/
│   ├── app.py               # Streamlit application
│   ├── pages/               # Sidebar subpages
│   └── components/          # Code viewer highlighter, doc browsers, stacktrace explainers
├── tests/
│   ├── generate_test_docs.py # Mock markdown documentation generator
│   ├── test_search.py       # Markdown parsing & vector search tests
│   ├── test_qa.py           # Documentation Q&A tests
│   └── test_examples.py     # Versioning & code generation tests
├── requirements.txt
└── README.md
```

---

## Installation & Setup

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Gemini Credentials**:
   Get an API key from Google AI Studio and set the environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
   *Note: If no API key is set, the application will run in mock mode with pre-baked responses for offline testing.*

---

## Running the Application

### 1. Launch FastAPI Backend
```bash
python -m backend.main
```
The backend API server will run at `http://127.0.0.1:8003`. You can view the OpenAPI documentation at `http://127.0.0.1:8003/docs`.

### 2. Launch Streamlit Frontend
```bash
streamlit run frontend/app.py
```
The Streamlit app will launch at `http://localhost:8503`.

---

## Running Automated Tests
Run the test suite using `pytest`:
```bash
pytest tests/
```
