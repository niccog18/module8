# Connecting RAG to FastAPI — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 10 min — "RAG API: build a FastAPI server with /ask, /ingest, and /stats endpoints. Demo the endpoints in Swagger UI, then connect a Streamlit frontend. Show the complete flow from question to grounded answer."]`

Let’s wrap the RAG pipeline in a FastAPI application. Create `rag_api.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import chromadb
import requests
import json
import os

app = FastAPI(title="RAG API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Config ---
OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"
DB_PATH = "./rag_db"

# --- ChromaDB setup ---
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("documents")

# --- Schemas ---
class AskRequest(BaseModel):
    question: str
    n_results: int = 3
    max_distance: float = 1.2

class SourceChunk(BaseModel):
    text: str
    source: str
    distance: float

class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    confidence: str

# --- RAG Logic ---
SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Answer ONLY from the provided context. "
    "If the context doesn't contain the answer, say you don't have enough "
    "information. Cite source documents. Keep responses under 200 words."
)

def retrieve(question: str, n_results: int, max_distance: float):
    if collection.count() == 0:
        return []
    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, collection.count())
    )
    chunks = []
    for i in range(len(results['documents'][0])):
        dist = results['distances'][0][i]
        if dist <= max_distance:
            chunks.append(SourceChunk(
                text=results['documents'][0][i],
                source=results['metadatas'][0][i].get('source', 'unknown'),
                distance=round(dist, 4)
            ))
    return chunks

def get_confidence(chunks):
    if not chunks:
        return "none"
    best = chunks[0].distance
    if best < 0.5: return "high"
    if best < 1.0: return "medium"
    return "low"

def generate(messages):
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL, "messages": messages, "stream": False
        })
        return r.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "Ollama is not running")

# --- Endpoints ---
@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    chunks = retrieve(req.question, req.n_results, req.max_distance)
    confidence = get_confidence(chunks)

    if not chunks:
        return AskResponse(
            answer="I don't have relevant information to answer that.",
            sources=[], confidence="none"
        )

    context = "\n\n".join(
        f"[Source: {c.source}]\n{c.text}" for c in chunks
    )
    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{context}"},
        {"role": "user", "content": req.question}
    ]

    answer = generate(messages)
    return AskResponse(answer=answer, sources=chunks, confidence=confidence)

@app.post("/ingest")
def ingest_documents():
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        raise HTTPException(404, "docs/ directory not found")

    chunks, ids, metadatas = [], [], []
    for filename in sorted(os.listdir(docs_dir)):
        if not filename.endswith(('.txt', '.md')):
            continue
        with open(os.path.join(docs_dir, filename), 'r') as f:
            content = f.read()
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        for i, para in enumerate(paragraphs):
            chunks.append(para)
            ids.append(f"{filename}_{i}")
            metadatas.append({"source": filename, "chunk_index": str(i)})

    if chunks:
        collection.upsert(documents=chunks, ids=ids, metadatas=metadatas)

    return {"message": f"Ingested {len(chunks)} chunks from {docs_dir}/"}

@app.get("/stats")
def stats():
    return {
        "document_count": collection.count(),
        "ollama_model": MODEL,
        "db_path": DB_PATH
    }

@app.get("/health")
def health():
    ollama_ok = False
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        ollama_ok = r.status_code == 200
    except:
        pass
    return {
        "chromadb": "ok",
        "ollama": "ok" if ollama_ok else "unavailable",
        "documents": collection.count()
    }
```

Run it:

```bash
uvicorn rag_api:app --reload
```

Visit `http://localhost:8000/docs` to see the Swagger UI. Try:

1. `POST /ingest` to load documents
2. `GET /stats` to verify the count
3. `POST /ask` with `{"question": "How does authentication work?"}` to test RAG

---

## What You Should See

A fully functional REST API that accepts questions and returns grounded answers with source citations, confidence levels, and structured JSON responses. The Swagger UI lets you test every endpoint interactively.

This is the backend for your module project. In Week 2, you’ll containerize it with Docker and add a Streamlit frontend.

`[DIAGRAM PLACEHOLDER: Swagger UI screenshot showing the /ask endpoint with a sample request and response including answer, sources, and confidence level]`