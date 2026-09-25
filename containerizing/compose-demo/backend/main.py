from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from config import settings
from my_rag import (
    load_documents,
    chunk_documents,
    ingest_documents,
    rag_query,
)

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=settings.CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=settings.COLLECTION_NAME
)


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "ollama": "configured",
        "ollama_url": settings.OLLAMA_URL,
        "documents": collection.count(),
    }


@app.post("/ingest")
def ingest():
    documents = load_documents()

    if not documents:
        return {
            "message": "No documents were found.",
            "documents": 0,
            "chunks": 0,
        }

    chunks = chunk_documents(documents)

    ingest_documents(
        collection,
        chunks,
        model,
    )

    return {
        "message": "Documents indexed successfully.",
        "documents": len(documents),
        "chunks": collection.count(),
    }


@app.post("/ask")
def ask(request: AskRequest):
    question = request.question.strip()

    if not question:
        return {
            "answer": "Please provide a question.",
            "sources": [],
            "confidence": "low",
            "chunks_retrieved": 0,
        }

    return rag_query(
        question,
        collection,
        model,
    )


@app.get("/")
def root():
    return {
        "message": "RAG API running in Docker",
        "model": settings.MODEL_NAME,
    }