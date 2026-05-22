# Docker Compose for Multi-Container Apps — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 10 min — "Docker Compose in Action: create a docker-compose.yml with FastAPI backend and Ollama. Start with docker-compose up, show both services communicating, demonstrate volume persistence."]`

Let’s build a two-service Docker Compose setup: FastAPI backend + Ollama. Create this structure:

```
compose-demo/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── docs/
│       └── sample.txt
└── .env
```

**`backend/main.py`** (simplified RAG API):

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import chromadb
import requests

app = FastAPI(title="RAG API")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Read config from environment variables (set in docker-compose.yml)
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("MODEL_NAME", "llama3.2:1b")

client = chromadb.PersistentClient(path="/app/chroma_data")
collection = client.get_or_create_collection("documents")

@app.get("/health")
def health():
    ollama_ok = False
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        ollama_ok = r.status_code == 200
    except:
        pass
    return {
        "status": "healthy",
        "ollama": "connected" if ollama_ok else "unavailable",
        "ollama_url": OLLAMA_URL,
        "documents": collection.count()
    }

@app.get("/")
def root():
    return {"message": "RAG API running in Docker", "model": MODEL}
```

**`backend/requirements.txt`:**

```
fastapi==0.109.0
uvicorn==0.27.0
chromadb==0.4.22
requests==2.31.0
```

**`backend/Dockerfile`:**

```docker
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`docker-compose.yml`:**

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_URL=http://ollama:11434
      - MODEL_NAME=llama3.2:1b
    depends_on:
      - ollama
    volumes:
      - chroma_data:/app/chroma_data

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  chroma_data:
  ollama_data:
```

---

## Start It Up

```bash
cd compose-demo
docker-compose up --build
```

You’ll see logs from both services. Wait for both to be ready, then:

1. Visit `http://localhost:8000` — should show the root message
2. Visit `http://localhost:8000/health` — should show `"ollama": "connected"`

The backend container is reaching Ollama at `http://ollama:11434` using the Docker Compose network. They’re communicating through service names.

---

## Verify Volume Persistence

1. Stop everything: `docker-compose down`
2. Start again: `docker-compose up`
3. Check `/health` — document count should be preserved (ChromaDB data survived the restart)

To remove volumes (reset everything): `docker-compose down -v`

`[DIAGRAM PLACEHOLDER: Terminal showing docker-compose up with interleaved logs from both backend and ollama services, plus browser showing the /health endpoint response]`