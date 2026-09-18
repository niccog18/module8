import json
import urllib.error
import urllib.request
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

from my_rag import (
    DOCS_DIR,
    CHROMA_PATH,
    COLLECTION_NAME,
    OLLAMA_URL,
    MODEL,
    TOP_K,
    DISTANCE_THRESHOLD,
    load_documents,
    chunk_documents,
    create_collection,
    ingest_documents,
    rag_query,
)


app = FastAPI(
    title="RAG API",
    description="FastAPI backend for a local ChromaDB and Ollama RAG pipeline.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask the RAG system.",
    )


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: str
    chunks_retrieved: int


class IngestResponse(BaseModel):
    message: str
    documents_loaded: int
    chunks_created: int
    chunks_in_database: int


class StatsResponse(BaseModel):
    document_count: int
    chunk_count: int
    model: str
    embedding_model: str
    collection_name: str
    chroma_path: str
    top_k: int
    distance_threshold: float


class HealthResponse(BaseModel):
    status: str
    chromadb: str
    ollama: str
    model: str


print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Connecting to ChromaDB...")
collection = create_collection()

print(f"RAG API initialized. Existing chunks: {collection.count()}")


def ollama_base_url() -> str:
    """Derive the Ollama base URL (scheme + host + port) from OLLAMA_URL."""
    parsed = urlparse(OLLAMA_URL)
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}"
    return "http://localhost:11434"


def model_matches(installed_name: str) -> bool:
    """Match 'llama3.2' against 'llama3.2:latest' as well as exact names."""
    if installed_name == MODEL:
        return True
    return ":" not in MODEL and installed_name == f"{MODEL}:latest"


def check_ollama() -> bool:
    """Return True when Ollama is reachable and the configured model exists."""
    try:
        request = urllib.request.Request(
            f"{ollama_base_url()}/api/tags",
            method="GET",
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        return any(
            model_matches(model.get("name", ""))
            for model in data.get("models", [])
        )

    except (OSError, json.JSONDecodeError):
        return False


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check whether ChromaDB and Ollama are accessible."""

    chromadb_status = "healthy"

    try:
        collection.count()
    except Exception:
        chromadb_status = "unavailable"

    ollama_status = "healthy" if check_ollama() else "unavailable"

    if chromadb_status == "healthy" and ollama_status == "healthy":
        overall_status = "healthy"
    else:
        overall_status = "degraded"

    return HealthResponse(
        status=overall_status,
        chromadb=chromadb_status,
        ollama=ollama_status,
        model=MODEL,
    )


@app.get("/stats", response_model=StatsResponse)
def get_stats():
    """Return RAG database and model information."""

    try:
        chunk_count = collection.count()

        metadatas = collection.get(include=["metadatas"]).get("metadatas", [])

        sources = {
            metadata.get("source")
            for metadata in metadatas
            if metadata and metadata.get("source")
        }

        return StatsResponse(
            document_count=len(sources),
            chunk_count=chunk_count,
            model=MODEL,
            embedding_model="all-MiniLM-L6-v2",
            collection_name=COLLECTION_NAME,
            chroma_path=CHROMA_PATH,
            top_k=TOP_K,
            distance_threshold=DISTANCE_THRESHOLD,
        )

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"ChromaDB is unavailable: {error}",
        )


@app.post("/ingest", response_model=IngestResponse)
def ingest():
    """Load documents from docs/ and add them to ChromaDB."""

    documents = load_documents()

    if not documents:
        raise HTTPException(
            status_code=404,
            detail=f"No .txt documents were found in '{DOCS_DIR}'.",
        )

    chunks = chunk_documents(documents)

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="Documents were found, but no usable chunks were created.",
        )

    before_count = collection.count()

    ingest_documents(collection, chunks, embedding_model)

    after_count = collection.count()

    if before_count > 0:
        message = (
            "Existing ChromaDB collection was used. "
            "No duplicate documents were added."
        )
    else:
        message = "Documents successfully ingested into ChromaDB."

    return IngestResponse(
        message=message,
        documents_loaded=len(documents),
        chunks_created=len(chunks),
        chunks_in_database=after_count,
    )


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """Ask a question and return a grounded RAG response."""

    if not request.question.strip():
        raise HTTPException(
            status_code=422,
            detail="Question must not be empty or whitespace only.",
        )

    if collection.count() == 0:
        return AskResponse(
            answer=(
                "No documents have been ingested yet. "
                "Please call POST /ingest before asking a question."
            ),
            sources=[],
            confidence="low",
            chunks_retrieved=0,
        )

    if not check_ollama():
        raise HTTPException(
            status_code=503,
            detail=(
                f"Ollama is unavailable or model '{MODEL}' "
                "is not installed. Please start Ollama and "
                "make sure the model is available."
            ),
        )

    try:
        response = rag_query(
            request.question,
            collection,
            embedding_model,
        )

        # generate_answer() returns Ollama failures as "Error: ..." strings
        # instead of raising, so surface them as a proper 503.
        if response["answer"].startswith("Error:"):
            raise HTTPException(
                status_code=503,
                detail=response["answer"],
            )

        return AskResponse(
            answer=response["answer"],
            sources=response["sources"],
            confidence=response["confidence"],
            chunks_retrieved=response["chunks_retrieved"],
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"RAG query failed: {error}",
        )