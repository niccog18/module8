"""
Backend: FastAPI RAG API  (Solution)
======================================
This is the Lesson 5 solution wired to the Lesson 6 Settings class.
Config now comes from environment variables — no hardcoded values.

Run locally:
    uvicorn main:app --reload --port 8000

Inside Docker Compose:
    Started automatically; reads OLLAMA_URL, CHROMA_PATH, MODEL_NAME from env.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from config import settings
import chromadb
import requests
import os

app = FastAPI(title="RAG API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ChromaDB ───────────────────────────────────────────────────────────────
chroma_client = chromadb.PersistentClient(path=settings.chroma_path)
collection    = chroma_client.get_or_create_collection("documents")

DOCS_DIR = "./docs"

# ── Schemas ────────────────────────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str
    n_results: int = 3
    max_distance: float = 1.2

    @field_validator("question")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("question must not be empty")
        return v


class SourceChunk(BaseModel):
    text: str
    source: str
    distance: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    confidence: str


class IngestResponse(BaseModel):
    chunks_ingested: int
    message: str


# ── RAG helpers ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Answer ONLY from the provided context. "
    "If the context doesn't contain the answer, say you don't have enough "
    "information. Cite source documents by name. Keep responses under 200 words."
)


def load_documents(directory: str) -> list[dict]:
    docs = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith((".txt", ".md")):
            with open(os.path.join(directory, filename)) as f:
                content = f.read()
            for i, para in enumerate(p.strip() for p in content.split("\n\n")):
                if para:
                    docs.append({
                        "text": para,
                        "id": f"{filename}_{i}",
                        "metadata": {"source": filename, "chunk_index": str(i)},
                    })
    return docs


def retrieve(query: str, n_results: int = 3, max_distance: float = 1.2) -> list[dict]:
    if collection.count() == 0:
        return []
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
    )
    return [
        {
            "text":     results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        }
        for i in range(len(results["documents"][0]))
        if results["distances"][0][i] <= max_distance
    ]


def compute_confidence(chunks: list[dict]) -> str:
    if not chunks:
        return "low"
    best = min(c["distance"] for c in chunks)
    return "high" if best < 0.5 else "medium" if best < 1.0 else "low"


def call_ollama(messages: list[dict]) -> str:
    try:
        r = requests.post(
            f"{settings.ollama_url}/api/chat",
            json={"model": settings.model_name, "messages": messages, "stream": False},
        )
        return r.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama is not running")


def check_ollama_health() -> bool:
    try:
        requests.get(f"{settings.ollama_url}/api/tags", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "RAG API is running", "docs": "/docs"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    chunks = retrieve(req.question, req.n_results, req.max_distance)
    if not chunks:
        return AskResponse(
            answer="No relevant documents found. Try running /ingest first.",
            sources=[],
            confidence="low",
        )
    context = "\n\n---\n\n".join(
        f"[Source: {c['metadata']['source']}]\n{c['text']}" for c in chunks
    )
    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{context}"},
        {"role": "user",   "content": req.question},
    ]
    answer = call_ollama(messages)
    return AskResponse(
        answer=answer,
        sources=[SourceChunk(text=c["text"], source=c["metadata"]["source"], distance=c["distance"]) for c in chunks],
        confidence=compute_confidence(chunks),
    )


@app.post("/ingest", response_model=IngestResponse)
def ingest():
    chunks = load_documents(DOCS_DIR)
    if not chunks:
        return IngestResponse(chunks_ingested=0, message="No documents found in docs/")
    collection.upsert(
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[c["id"] for c in chunks],
    )
    return IngestResponse(chunks_ingested=len(chunks), message=f"Ingested {len(chunks)} chunks")


@app.get("/stats")
def stats():
    return {"document_count": collection.count(), "model": settings.model_name, "db_path": settings.chroma_path}


@app.get("/health")
def health():
    try:
        doc_count = collection.count()
        chroma_ok = True
    except Exception:
        doc_count = 0
        chroma_ok = False
    ollama_ok = check_ollama_health()
    return {
        "status": "ok" if chroma_ok and ollama_ok else "degraded",
        "chromadb": "ok" if chroma_ok else "error",
        "ollama": "connected" if ollama_ok else "disconnected",
        "document_count": doc_count,
    }
