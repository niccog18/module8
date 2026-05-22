# Module 8 Overview

**Module 8 — RAG Intro & Docker Deployment**

**Duration:** 2 Weeks | **Hours:** 40 | **Prerequisites:** Modules 1–7

---

## Module Philosophy

Week 1 brings the full RAG pipeline together. Students connect their Module 7 retrieval skills with local LLM generation via Ollama, building a complete question-answering system over their own documents. Week 2 puts the entire stack in Docker containers so it runs with a single command on any machine.

Students leave with a working, containerized AI application — the most impressive portfolio piece of the course and the direct preparation for the Capstone.

---

## Week Structure

### Week 1 — RAG Pipeline

1. **The RAG Architecture** — End-to-end overview, pipeline stages, why RAG beats LLM-alone
2. **Running Local LLMs with Ollama** — Installation, model pulling, REST API, local vs cloud
3. **Building the RAG Pipeline** — Complete ingest → retrieve → generate workflow with streaming
4. **Reliability & Guardrails** — Confidence thresholds, no-context fallback, prompt guardrails
5. **Connecting RAG to FastAPI** — API endpoints, Pydantic schemas, streaming responses

### Knowledge Check: RAG & Containerization Concepts (8 questions)

Covers RAG pipeline, Ollama, guardrails, plus Docker preview questions.

### Week 2 — Docker & Deployment

1. **What is Docker and Why It Matters** — Images, containers, registries, the shipping container analogy
2. **Dockerfile Creation** — Instructions, layer caching, .dockerignore, best practices
3. **Docker Compose for Multi-Container Apps** — Service networking, volumes, depends_on
4. **Environment Management & Configuration** — .env files, Settings class, dev vs production
5. **Containerizing Your RAG Application** — Full 3-service stack, one-command startup
6. **CI/CD Basics with GitHub Actions** — Automated testing, Docker build verification

### Module Project: Containerized RAG Assistant (100 points, 5-minute presentation)

---

## Assessment Summary

| Assessment | Type | Placement | Weight |
| --- | --- | --- | --- |
| RAG & Containerization Concepts | Knowledge Check (8 questions) | End of Week 1 | Mid-module checkpoint |
| Containerized RAG Assistant | Module Project (5-min presentation) | End of Week 2 | Final module assessment |

---

## Dependencies

**Backend:**

```
fastapi
uvicorn
chromadb
sentence-transformers
requests
pydantic
pytest
httpx
```

**Frontend:**

```
streamlit
requests
```

**Infrastructure:**

```
Docker Desktop (or Docker Engine)
docker-compose
Ollama (via Docker image: ollama/ollama)
```

---

## Video Placeholders Summary

| Lesson | Placement | Length | Theme |
| --- | --- | --- | --- |
| The RAG Architecture | Concept | 7 min | End-to-end RAG animation, pipeline stages |
| The RAG Architecture | Guided Example | 8 min | Trace a question through each pipeline stage |
| Running Local LLMs | Concept | 7 min | Install Ollama, pull model, chat locally |
| Running Local LLMs | Guided Example | 8 min | Call Ollama from Python, test RAG-style prompts |
| Building the RAG Pipeline | Concept | 10 min | Complete pipeline from ingest to generate |
| Building the RAG Pipeline | Guided Example | 12 min | Build rag_[pipeline.py](http://pipeline.py) with interactive query loop |
| Reliability & Guardrails | Concept | 7 min | Before/after guardrails demo |
| Reliability & Guardrails | Guided Example | 8 min | Threshold filtering, confidence levels, fallbacks |
| Connecting RAG to FastAPI | Concept | 8 min | Wrap RAG in API endpoints, Swagger UI demo |
| Connecting RAG to FastAPI | Guided Example | 10 min | Full RAG API with /ask, /ingest, /health |
| What is Docker | Concept | 6 min | Shipping container analogy, images vs containers |
| What is Docker | Guided Example | 8 min | Install, hello-world, run Python in container |
| Dockerfile Creation | Concept | 8 min | Instructions, layer caching, best practices |
| Dockerfile Creation | Guided Example | 10 min | Dockerfile for RAG backend, build optimization |
| Docker Compose | Concept | 10 min | Multi-service setup, networking, volumes |
| Docker Compose | Guided Example | 10 min | FastAPI + Ollama two-service stack |
| Environment Management | Concept | 6 min | .env files, Settings class, dev vs prod |
| Environment Management | Guided Example | 7 min | Configurable app with environment variables |
| Containerizing RAG | Concept | 10 min | Full 3-service architecture, one-command startup |
| Containerizing RAG | Guided Example | 12 min | Complete docker-compose with Streamlit + FastAPI + Ollama |
| CI/CD Basics | Concept | 6 min | GitHub Actions workflow, automated testing |
| CI/CD Basics | Guided Example | 8 min | Create and push CI workflow, verify in GitHub Actions |