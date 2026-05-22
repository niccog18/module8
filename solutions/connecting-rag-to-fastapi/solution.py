"""
L5 — Connecting RAG to FastAPI  (Solution)
============================================
Run with:
    uvicorn solution:app --reload --port 8000

Then open http://localhost:8000/docs to test in Swagger UI.

Prerequisites:
    pip install fastapi uvicorn chromadb requests pydantic
    docs/ folder with text files
    ollama serve (or the /health endpoint will show disconnected)

Key concepts:
    FastAPI wraps the pipeline:
        The RAG logic (retrieve → prompt → generate) is identical to Lesson 3/4.
        FastAPI adds HTTP endpoints, input validation, error handling, and docs.

    Pydantic field_validator:
        Raises a 422 Unprocessable Entity before the endpoint runs if the
        question is empty. Better to catch bad input at the boundary than
        deep inside business logic.

    503 vs 422:
        422 = client error (bad input — their fault, fix the request)
        503 = server error (Ollama not running — our infrastructure, fix the env)

    /health endpoint:
        Production services need health checks for load balancers and Docker
        Compose dependency readiness probes. Check both ChromaDB and Ollama.

    CORS middleware:
        Required so a browser-based Streamlit frontend (different port) can call
        this API. Without it, the browser blocks the request with a CORS error.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import chromadb
import requests
import json
import os

app = FastAPI(title="RAG API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Config ─────────────────────────────────────────────────────────────────
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL      = os.environ.get("MODEL_NAME", "llama3.2:1b")
DB_PATH    = os.environ.get("CHROMA_PATH", "./rag_db")
DOCS_DIR   = "./docs"

# ── ChromaDB setup ─────────────────────────────────────────────────────────
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection    = chroma_client.get_or_create_collection("documents")


# ── Pydantic schemas ───────────────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str
    n_results: int = 3
    max_distance: float = 1.2

    @field_validator("question")
    @classmethod
    def question_not_empty(cls, v: str) -> str:
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
    """Load .txt/.md files, chunk by paragraph."""
    docs = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith((".txt", ".md")):
            with open(os.path.join(directory, filename), "r") as f:
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
    """Query ChromaDB, filter by max_distance."""
    if collection.count() == 0:
        return []
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        dist = results["distances"][0][i]
        if dist <= max_distance:
            chunks.append({
                "text":     results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": dist,
            })
    return chunks


def compute_confidence(chunks: list[dict]) -> str:
    """Return 'high' / 'medium' / 'low' based on best distance."""
    if not chunks:
        return "low"
    best = min(c["distance"] for c in chunks)
    if best < 0.5:
        return "high"
    if best < 1.0:
        return "medium"
    return "low"


def call_ollama(messages: list[dict]) -> str:
    """Call Ollama. Raises 503 if unreachable."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": messages, "stream": False},
        )
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Start it with: ollama serve",
        )


def check_ollama_health() -> bool:
    """Return True if Ollama is reachable."""
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    """Retrieve context and generate a grounded answer."""
    chunks = retrieve(req.question, req.n_results, req.max_distance)

    if not chunks:
        return AskResponse(
            answer="No relevant documents found. Try running /ingest first, or rephrase your question.",
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

    answer = call_ollama(messages)  # may raise 503

    return AskResponse(
        answer=answer,
        sources=[
            SourceChunk(
                text=c["text"],
                source=c["metadata"]["source"],
                distance=c["distance"],
            )
            for c in chunks
        ],
        confidence=compute_confidence(chunks),
    )


@app.post("/ingest", response_model=IngestResponse)
def ingest():
    """Load documents from docs/ into ChromaDB."""
    chunks = load_documents(DOCS_DIR)
    if not chunks:
        return IngestResponse(chunks_ingested=0, message="No documents found in docs/")
    collection.upsert(
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[c["id"] for c in chunks],
    )
    return IngestResponse(
        chunks_ingested=len(chunks),
        message=f"Successfully ingested {len(chunks)} chunks from {DOCS_DIR}",
    )


@app.get("/stats")
def stats():
    """Return document count and model info."""
    return {
        "document_count": collection.count(),
        "model": MODEL,
        "db_path": DB_PATH,
    }


@app.get("/health")
def health():
    """Check ChromaDB and Ollama liveness."""
    try:
        doc_count = collection.count()
        chroma_status = "ok"
    except Exception:
        doc_count = 0
        chroma_status = "error"

    ollama_ok = check_ollama_health()

    return {
        "status": "ok" if chroma_status == "ok" and ollama_ok else "degraded",
        "chromadb": chroma_status,
        "ollama": "connected" if ollama_ok else "disconnected",
        "document_count": doc_count,
    }
