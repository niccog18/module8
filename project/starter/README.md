# Module 8 Project — Containerized RAG Assistant (Starter)

## Overview

Build and containerize a RAG-powered chatbot that runs entirely with `docker-compose up`.
The chatbot ingests documents, stores embeddings in ChromaDB, retrieves relevant chunks,
generates grounded answers via Ollama, and presents everything through a Streamlit chat UI.

## Project Structure

```
containerized-rag/
├── docker-compose.yml          ← Wire up backend, frontend, and Ollama
├── .env.example                ← Copy to .env and fill in values
├── backend/
│   ├── Dockerfile
│   ├── main.py                 ← FastAPI: /ask, /ingest, /stats, /health
│   ├── rag.py                  ← RAG pipeline: retrieve + generate
│   ├── config.py               ← Environment-based settings
│   ├── requirements.txt
│   ├── docs/                   ← Sample document corpus (add your own files here)
│   └── tests/
│       └── test_api.py
├── frontend/
│   ├── Dockerfile
│   ├── app.py                  ← Streamlit chat UI
│   └── requirements.txt
└── README.md                   ← You write this at the end
```

## Quick Start

### Step 1 — Build locally first (easier to debug)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Step 2 — Dockerize

```bash
# Copy and fill in your .env
cp .env.example .env

# Build and run everything
docker-compose up --build
```

### Step 3 — Pull the model (only needed once)

```bash
ollama pull llama3.2:1b
```

## Files

| File                        | Purpose                                               |
| --------------------------- | ----------------------------------------------------- |
| `docker-compose.yml`        | Defines backend, frontend, and Ollama services        |
| `.env.example`              | Template for required environment variables           |
| `backend/main.py`           | FastAPI app — your primary backend work file          |
| `backend/rag.py`            | RAG logic: chunking, retrieval, generation            |
| `backend/config.py`         | Reads all config from environment variables           |
| `backend/tests/test_api.py` | API smoke tests (at least 3 required)                 |
| `backend/docs/`             | Document corpus — add `.txt` or `.md` files here      |
| `frontend/app.py`           | Streamlit chat interface — your primary frontend file |

## Requirements

See the project brief in the course platform for full rubric.
Key sections to implement:

1. **Document Ingestion** — Load, chunk, and store documents in ChromaDB via `POST /ingest`
2. **RAG Pipeline** — Retrieve chunks, build prompt, generate answer with Ollama
3. **Streamlit Interface** — `st.chat_message()`, chat history in session state, source citations
4. **Docker Containerization** — 3 services, volumes for data persistence, env vars for all config
5. **Documentation & Quality** — README, `.env.example`, 3+ passing tests, clean code

## Build Order (Recommended)

1. Get the backend working locally — run `uvicorn main:app --reload`
2. Get the frontend working locally — run `streamlit run app.py`
3. Dockerize the backend — write `backend/Dockerfile`, build and test
4. Dockerize the frontend — write `frontend/Dockerfile`, build and test
5. Write `docker-compose.yml` — connect all three services
6. Test the full stack — `docker-compose up --build`
7. Write the `README.md` — setup, architecture diagram, usage guide

## Tips

- Implement `rag.py` functions one at a time and test each in isolation before wiring to FastAPI.
- The `docs/` folder already has sample documents. Add your own files for a better demo.
- Use the `/health` endpoint to verify all services are reachable before asking questions.
- All configuration (URLs, model names, paths) must come from environment variables — no hardcoded values.
- Named Docker volumes keep your ChromaDB data and Ollama models between restarts.
