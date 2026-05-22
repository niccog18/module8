# Module Project: Containerized RAG Assistant

**Module 8 — RAG Intro & Docker Deployment**

---

## Project Overview

Build and containerize a **minimal RAG-powered chatbot** that runs entirely with `docker-compose up`. The chatbot ingests documents, stores them in ChromaDB, retrieves relevant chunks for user questions, generates grounded answers via Ollama, and presents everything through a Streamlit interface.

**Time:** 10–15 hours

**Presentation:** 5 minutes (live demo of `docker-compose up` + question answering)

---

## Project Structure

```
containerized-rag/
├── docker-compose.yml
├── .env
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml             # Optional but impressive
├── backend/
│   ├── Dockerfile
│   ├── main.py              # FastAPI with /ask, /ingest, /stats, /health
│   ├── rag.py               # RAG pipeline (retrieve + generate)
│   ├── config.py            # Environment-based settings
│   ├── requirements.txt
│   ├── docs/                # Document corpus
│   └── tests/
│       └── test_api.py
├── frontend/
│   ├── Dockerfile
│   ├── app.py               # Streamlit chat interface
│   └── requirements.txt
└── README.md
```

---

## Requirements & Rubric

### 1. Document Ingestion (15 points)

- Load documents from a corpus (Python docs, course notes, textbook excerpts, or your own collection)
- Chunk documents with a clear strategy
- Store in ChromaDB with metadata (source file, chunk index)
- Ingestible via API endpoint (`POST /ingest`)

### 2. RAG Pipeline (25 points)

- Retrieve relevant chunks from ChromaDB for a given question
- Build a RAG prompt with system instructions, retrieved context, and the question
- Generate an answer using Ollama (local LLM)
- Return structured responses with answer, sources, and confidence level
- Include at least one guardrail (confidence threshold, no-context fallback, or output validation)

### 3. Streamlit Interface (15 points)

- Chat interface with `st.chat_message()` and `st.chat_input()`
- Chat history persists in session state
- Source citations displayed (in expandable sections)
- Sidebar with health status, document count, and re-index button

### 4. Docker Containerization (25 points)

- `docker-compose.yml` with three services: backend, frontend, ollama
- Both backend and frontend have proper Dockerfiles
- Named volumes for ChromaDB data and Ollama models
- Environment variables for all configuration (no hardcoded URLs)
- The entire application runs with `docker-compose up`

### 5. Documentation & Quality (20 points)

- README with: setup instructions, architecture description (with diagram), usage guide, what model to pull
- Working `requirements.txt` for both services
- `.env.example` showing required configuration
- At least 3 passing tests
- Clean code with functions, docstrings, and modular files

---

## Grading Rubric

| Category | Points | Criteria |
| --- | --- | --- |
| Document Ingestion | 15 | Corpus loaded, chunked, stored in ChromaDB with metadata |
| RAG Pipeline | 25 | Retrieval + generation, structured responses, at least one guardrail |
| Streamlit Interface | 15 | Chat UI, history, source citations, sidebar controls |
| Docker Containerization | 25 | 3 services, Dockerfiles, volumes, env vars, `docker-compose up` works |
| Documentation & Quality | 20 | README, tests, .env.example, clean code |
| **Total** | **100** |  |

---

## Document Corpus Options

**Option A (Recommended):** The provided starter corpus — excerpts from Python documentation, FastAPI docs, and Streamlit docs.

**Option B:** Your own course notes from Modules 1–7. Export them as text files.

**Option C:** Any domain you’re interested in: cooking recipes, fitness guides, travel information, or technical documentation from an open-source project.

Use at least 5 documents with a combined 10+ pages of content.

---

## 5-Minute Presentation

1. **`docker-compose up`** (1 min) — Run it live. Show all three services starting.
2. **Ask the chatbot a question** (1 min) — Show the answer with source citations. Ask a follow-up.
3. **Show your `docker-compose.yml`** (1 min) — Walk through the services. Explain what each one does.
4. **One guardrail/reliability decision** (1 min) — What did you add to make the system more reliable? Show it working.
5. **What you’d improve** (1 min) — With more time, what would you add or change?

---

## Starter Code

**GitHub:** `module-08-rag-docker/project/starter/`

The starter includes: complete project folder structure, `docker-compose.yml` template with service stubs, Dockerfile templates for both services, `config.py` with environment variable patterns, `.env.example`, sample document corpus, `requirements.txt` files per service, and a README template.

You build the RAG logic, Streamlit interface, and API endpoints. The starter saves you infrastructure setup time.

---

## Recommended Build Order

1. **Get the backend working locally** (without Docker) — `uvicorn main:app --reload`
2. **Get the frontend working locally** — `streamlit run app.py`
3. **Dockerize the backend** — Dockerfile + build + test
4. **Dockerize the frontend** — Dockerfile + build + test
5. **Write docker-compose.yml** — Connect all three services
6. **Test the full stack** — `docker-compose up --build`
7. **Write the README** — Setup instructions, architecture, usage
8. **Polish** — Guardrails, error handling, tests, CI workflow