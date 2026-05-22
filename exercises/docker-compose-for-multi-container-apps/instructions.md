# Docker Compose for Multi-Container Apps

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 35 minutes

## Objective

Build a Docker Compose setup with your FastAPI RAG backend and Ollama running as connected containers.

## What You'll Build

- **`docker-compose.yml`** — Two services: `backend` + `ollama`
- **`Dockerfile`** — Backend image (reuse from Lesson 7 if complete)

## docker-compose.yml Requirements

| Service | Image | Details |
|---------|-------|---------|
| `backend` | Built from `./Dockerfile` | Port `8000:8000`, depends on `ollama`, reads `OLLAMA_URL` from env |
| `ollama` | `ollama/ollama` | Port `11434:11434`, named volume for model storage |

**Also configure:**

- `OLLAMA_URL=http://ollama:11434` environment variable on `backend` (use the service name, not localhost)
- Named volume `ollama_models` for persisting downloaded models
- Named volume `chroma_data` for persisting the vector database
- `depends_on: ollama` so the backend waits for Ollama to start

## Reference Code

The starter `docker-compose.yml` and `Dockerfile` provide scaffolding with TODOs.

## Running

```bash
docker-compose up --build
# In a second terminal, pull the model:
docker-compose exec ollama ollama pull llama3.2:1b
```

Verify:
- `http://localhost:8000/health` shows `"ollama": "connected"`
- `http://localhost:8000/docs` loads Swagger UI

## Persistence Test

```bash
docker-compose down
docker-compose up
# Check that document count is preserved
```

## Deliverable

A working Docker Compose setup where FastAPI and Ollama run as connected containers, with verified persistence across restarts.
