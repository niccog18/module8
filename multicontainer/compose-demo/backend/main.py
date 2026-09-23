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