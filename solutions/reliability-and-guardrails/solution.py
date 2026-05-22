"""
L4 — Reliability & Guardrails: Enhanced RAG Pipeline  (Solution)
==================================================================
Run with:
    python solution.py

Prerequisites:
    pip install chromadb requests
    ollama serve + a model pulled
    docs/ folder (reuse from Lesson 3)

Key concepts:
    Guardrail 1 — Distance threshold filtering:
        ChromaDB L2 distance: 0.0 = identical, ~1.5 = quite different.
        Filtering removes noise before it reaches the LLM. A chunk with
        distance 1.4 is barely relevant — passing it only confuses the model.
        Start at 1.0 and tighten if the model hallucinates.

    Guardrail 2 — Confidence levels:
        Confidence is derived from the BEST (lowest) distance among kept chunks.
        "high" (<0.5): very close semantic match — answer is likely accurate.
        "medium" (<1.0): moderate match — answer should be checked.
        "low" (>=1.0): weak match — treat the answer with scepticism.

    Guardrail 3 — Strengthened system prompt:
        Explicit "never make up" instructions meaningfully reduce hallucination
        on smaller models. Larger models may ignore weak instructions.

    Guardrail 4 — Structured response:
        Returning a dict instead of a plain string makes the pipeline composable.
        The FastAPI layer (Lesson 5) can directly serialise this dict to JSON
        and the Streamlit frontend (Lesson 10) can render each field separately.
"""

import chromadb
import requests
import json
import os

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"
DISTANCE_THRESHOLD = 1.0


# ── Guardrail 3: Strengthened system prompt ────────────────────────────────
SYSTEM_PROMPT = """You are a reliable AI assistant grounded in provided documents.
Answer the user's question based ONLY on the context below.

Critical rules — follow these without exception:
- NEVER make up information. If it is not in the context, say so.
- If the context does not contain the answer, say: "I don't know based on the available documents."
- Always cite the source document name in parentheses after each claim.
- Keep your response under 200 words.
- Do not speculate or infer beyond what is explicitly stated.
"""


# ── Core pipeline ──────────────────────────────────────────────────────────

def load_documents(directory: str) -> list[dict]:
    """Load .txt/.md files from directory, chunk by paragraph."""
    docs = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith((".txt", ".md")):
            with open(os.path.join(directory, filename), "r") as f:
                content = f.read()
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            for i, para in enumerate(paragraphs):
                docs.append({
                    "text": para,
                    "id": f"{filename}_{i}",
                    "metadata": {"source": filename, "chunk_index": str(i)},
                })
    return docs


def ingest(collection, docs_directory: str) -> int:
    """Upsert all document chunks into ChromaDB."""
    chunks = load_documents(docs_directory)
    if not chunks:
        print("Warning: no documents found.")
        return 0
    collection.upsert(
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[c["id"] for c in chunks],
    )
    return len(chunks)


def retrieve(collection, query: str, n_results: int = 3) -> list[dict]:
    """Query ChromaDB, return list of {"text", "metadata", "distance"}."""
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
    ]


def generate(messages: list[dict]) -> str:
    """Call Ollama (non-streaming). Return response text."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": messages, "stream": False},
        )
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running? (ollama serve)"


# ── Guardrail 1 + 2 ────────────────────────────────────────────────────────

def filter_chunks(chunks: list[dict], threshold: float = DISTANCE_THRESHOLD) -> list[dict]:
    """Guardrail 1 — discard chunks that are too distant to be relevant."""
    return [c for c in chunks if c["distance"] < threshold]


def compute_confidence(chunks: list[dict]) -> str:
    """Guardrail 2 — confidence label based on best (lowest) distance."""
    best = min(c["distance"] for c in chunks)
    if best < 0.5:
        return "high"
    if best < 1.0:
        return "medium"
    return "low"


# ── Guardrail 4: Structured RAG query ─────────────────────────────────────

def rag_query(collection, question: str) -> dict:
    """Full guardrailed pipeline. Returns a structured result dict."""
    raw_chunks = retrieve(collection, question)
    kept_chunks = filter_chunks(raw_chunks)

    if not kept_chunks:
        return {
            "answer": "I couldn't find relevant information in the documents to answer that question.",
            "sources": [],
            "confidence": "low",
            "chunks_retrieved": 0,
        }

    confidence = compute_confidence(kept_chunks)

    # Build prompt
    context_parts = [
        f"[Source: {c['metadata']['source']}]\n{c['text']}"
        for c in kept_chunks
    ]
    context = "\n\n---\n\n".join(context_parts)
    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"},
        {"role": "user",   "content": question},
    ]

    answer = generate(messages)
    sources = list({c["metadata"]["source"] for c in kept_chunks})

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "chunks_retrieved": len(kept_chunks),
    }


# ── Main: test with 4 query types ─────────────────────────────────────────

if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./rag_db")
    collection = client.get_or_create_collection("course_docs")

    if collection.count() == 0:
        count = ingest(collection, "docs")
        print(f"Ingested {count} chunks.")
    else:
        print(f"Using existing collection: {collection.count()} chunks.")

    # Replace these with questions appropriate to your docs/ content
    test_questions = [
        ("in-scope",     "What is ChromaDB and how does it store documents?"),
        ("partial",      "How does ChromaDB compare to PostgreSQL for storing data?"),
        ("out-of-scope", "What is the tallest mountain in the world?"),
        ("ambiguous",    "Can I use Python to work with databases?"),
    ]

    for label, question in test_questions:
        print(f"\n{'='*60}")
        print(f"[{label.upper()}] {question}")
        result = rag_query(collection, question)
        print(f"Confidence   : {result['confidence']}")
        print(f"Chunks used  : {result['chunks_retrieved']}")
        print(f"Sources      : {result['sources']}")
        print(f"Answer       :\n{result['answer']}")
