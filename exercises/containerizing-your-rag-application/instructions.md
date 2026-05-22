# Containerizing Your RAG Application

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 45 minutes

## Objective

Build the complete three-service Docker Compose stack for your RAG application and verify end-to-end functionality.

## Project Structure to Create

```
containerizing-your-rag-application/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py            ← FastAPI RAG API (from Lesson 5)
│   ├── config.py          ← Settings class (from Lesson 6)
│   └── docs/              ← Your text files
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py             ← Streamlit UI
├── docker-compose.yml
└── .env
```

## What You'll Build

**`docker-compose.yml`** — Three services:

| Service | Build | Ports | Key env vars |
|---------|-------|-------|--------------|
| `backend` | `./backend` | `8000:8000` | `OLLAMA_URL=http://ollama:11434` |
| `frontend` | `./frontend` | `8501:8501` | `BACKEND_URL=http://backend:8000` |
| `ollama` | `ollama/ollama` image | `11434:11434` | — |

**`backend/Dockerfile`** — Python 3.11-slim, installs requirements, runs uvicorn

**`frontend/Dockerfile`** — Python 3.11-slim, installs requirements, runs streamlit

**`frontend/app.py`** — Streamlit UI with:
- A text input for questions
- A "Re-index Documents" button that calls `POST /ingest`
- Answer display with source citations and confidence badge
- Health status indicator in the sidebar

## Reference Code

Starter files are provided with TODOs — fill in each section.

## Running

```bash
docker-compose up --build
docker-compose exec ollama ollama pull llama3.2:1b
```

Then:

1. Open `http://localhost:8501` (Streamlit)
2. Click **Re-index Documents**
3. Ask a question
4. Verify the answer appears with source citations
5. Check `http://localhost:8000/health`

## Deliverable

A complete containerized RAG application running with `docker-compose up`, with all three services communicating correctly.
