# Containerizing Your RAG Application — Concept

**Module 8 — RAG Intro & Docker Deployment**

**Estimated time: 35 minutes**

---

### Learning Objectives

By the end of this lesson, you will be able to:

1. Design a Docker Compose setup for a complete RAG application (FastAPI + Streamlit + Ollama)
2. Write Dockerfiles for both the FastAPI backend and Streamlit frontend
3. Configure networking, volumes, and environment variables for the full stack
4. Start the entire application with `docker-compose up` and verify all services communicate

---

`[VIDEO PLACEHOLDER: 10 min — "Containerizing the Full RAG Stack: write docker-compose.yml with backend, frontend, and Ollama. Start everything with one command. Show the Streamlit UI talking to FastAPI talking to Ollama."]`

This is the lesson where everything comes together. You’ve built each piece individually: a RAG API (Lesson 5), Docker images (Lesson 7), Docker Compose configurations (Lesson 8), and proper environment management (Lesson 9). Now you assemble the complete, containerized RAG application.

The goal: anyone can clone your repo, run `docker-compose up`, and have a working AI-powered chatbot — no Python installation, no Ollama setup, no ChromaDB configuration. One command.

---

## The Full Stack Architecture

```
┌───────────────────────────────────────────────┐
│                Docker Compose Network                │
│                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┓  │
│  │  Streamlit  │  │   FastAPI   │  │   Ollama    ┃  │
│  │  (frontend) │─▶│  (backend)  │─▶│   (LLM)    ┃  │
│  │  :8501      │  │  :8000      │  │  :11434    ┃  │
│  └─────────────┘  └──────┬──────┘  └────────────┛  │
│                      │                                │
│                ┌──────┴──────┐                       │
│                │  ChromaDB   │ (volume)                │
│                └─────────────┘                       │
└───────────────────────────────────────────────┘
```

`[DIAGRAM PLACEHOLDER: Polished version of the architecture diagram showing all three containers with ports, the Docker network, and volume connections]`

Three services, one network, two volumes. The Streamlit frontend calls the FastAPI backend at `http://backend:8000`. The FastAPI backend calls Ollama at `http://ollama:11434`. ChromaDB data persists in a named volume.

---

## Project Structure

```
rag-app/
├── docker-compose.yml
├── .env
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── rag.py
│   ├── config.py
│   ├── requirements.txt
│   └── docs/
├── frontend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── README.md
```

Separate Dockerfiles for backend and frontend. Shared `.env` file at the root. The `docs/` folder lives inside backend (or could be a shared volume).

---

## The Streamlit Dockerfile

Streamlit needs its own Dockerfile because it runs as a separate service:

```docker
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

Key difference from FastAPI: the CMD runs `streamlit run` instead of `uvicorn`, and it binds to port 8501.

---

## Model Initialization in Ollama

Ollama containers start without any models. You need to pull a model after the container starts. Options:

**Option 1: Manual pull after startup**

```bash
docker-compose exec ollama ollama pull llama3.2:1b
```

**Option 2: Init script in docker-compose.yml**

```yaml
ollama:
  image: ollama/ollama
  volumes:
    - ollama_data:/root/.ollama
```

Once pulled, the model is stored in the volume and persists across restarts. You only need to pull once.

---

## One Command to Start Everything

```bash
git clone <your-repo>
cd rag-app
cp .env.example .env  # Copy and configure
docker-compose up --build
```

That’s it. The entire RAG application — frontend, backend, LLM — starts with one command. This is the module project’s key deliverable.