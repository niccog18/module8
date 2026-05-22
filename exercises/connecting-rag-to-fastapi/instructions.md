# Connecting RAG to FastAPI

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 35 minutes

## Objective

Wrap your RAG pipeline in a FastAPI application with production-ready features: health checks, configurable parameters, CORS, and proper error handling.

## What You'll Build

A `my_rag_api.py` with 4 endpoints:

| Method | Path      | Purpose                                                                 |
| ------ | --------- | ----------------------------------------------------------------------- |
| `POST` | `/ask`    | Accept a question, return a grounded answer with sources and confidence |
| `POST` | `/ingest` | Load documents from `docs/` into ChromaDB                               |
| `GET`  | `/stats`  | Return document count and model info                                    |
| `GET`  | `/health` | Check if ChromaDB is accessible and Ollama is reachable                 |

**Also required:**

- Pydantic schemas for all request/response models
- CORS middleware for frontend connectivity
- Error handling: Ollama down → 503, empty docs → clear message, empty question → 422 via Pydantic

## Reference Code

The starter file (`my_rag_api.py`) provides a scaffold with TODOs — fill in each section.

## Running

```bash
uvicorn my_rag_api:app --reload --port 8000
```

Then open `http://localhost:8000/docs` to test all endpoints in Swagger UI.

## Deliverable

All 4 endpoints working and tested via Swagger UI, with proper error handling for the 3 listed error cases.
