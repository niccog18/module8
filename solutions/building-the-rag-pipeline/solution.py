"""
L3 — Building the RAG Pipeline  (Solution)
============================================
Run with:
    python solution.py

Prerequisites:
    pip install chromadb requests
    ollama serve  (in a separate terminal)
    ollama pull llama3.2:1b
    A docs/ folder with at least 6 .txt or .md files.

Key concepts:
    Ingest once, query many times:
        ChromaDB's PersistentClient saves to disk. On first run we load and
        chunk the docs; on subsequent runs we skip ingestion and reuse the
        existing collection. This is the "ingest-on-first-run" pattern.

    Chunking by paragraph:
        Splitting on "\n\n" keeps semantically related sentences together.
        Each chunk gets a unique ID (filename + index) and metadata (source).
        The metadata lets us show which file each retrieved chunk came from.

    ChromaDB embedding:
        By default ChromaDB uses a local sentence-transformer model to convert
        text → vectors automatically. You don't need to call an embedding API.

    Streaming vs. non-streaming:
        With stream=True we get tokens one at a time and can print them as
        they arrive — much better UX than waiting for the full response.

    Retrieval before generation:
        Printing the retrieved chunks before the answer makes the pipeline
        transparent: students can see exactly what context the LLM received.
"""

import chromadb
import requests
import json
import os
import time

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"


# ── Step 1: Ingestion ──────────────────────────────────────────────────────

def load_documents(directory: str) -> list[dict]:
    """Load all .txt and .md files, chunk by paragraph."""
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
    """Load, chunk, and upsert documents into ChromaDB. Returns chunk count."""
    chunks = load_documents(docs_directory)
    if not chunks:
        print("Warning: no documents found in docs/")
        return 0
    collection.upsert(
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[c["id"] for c in chunks],
    )
    return len(chunks)


# ── Step 2: Retrieval ──────────────────────────────────────────────────────

def retrieve(collection, query: str, n_results: int = 3) -> list[dict]:
    """Query ChromaDB, return top-n chunks as dicts."""
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text":     results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })
    return chunks


# ── Step 3: Prompt building ────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful AI assistant.
Answer the user's question based ONLY on the context provided below.

Rules:
- Only use information from the CONTEXT section.
- If the context doesn't contain the answer, say "I don't have enough information to answer that."
- Cite your sources by mentioning the document name in parentheses.
- Keep your response under 200 words.
"""


def build_messages(question: str, chunks: list[dict]) -> list[dict]:
    """Assemble the RAG messages list: system (with context) + user question."""
    context_parts = []
    for chunk in chunks:
        source = chunk["metadata"]["source"]
        context_parts.append(f"[Source: {source}]\n{chunk['text']}")
    context = "\n\n---\n\n".join(context_parts)
    system_with_context = f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"
    return [
        {"role": "system", "content": system_with_context},
        {"role": "user",   "content": question},
    ]


# ── Step 4: Generation ─────────────────────────────────────────────────────

def generate(messages: list[dict]) -> str:
    """Stream a response from Ollama, printing tokens as they arrive."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": messages, "stream": True},
            stream=True,
        )
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                token = data.get("message", {}).get("content", "")
                if token:
                    print(token, end="", flush=True)
                    full_response += token
        print()  # newline after stream ends
        return full_response
    except requests.exceptions.ConnectionError:
        msg = "ERROR: Cannot connect to Ollama. Is it running? (ollama serve)"
        print(msg)
        return msg


# ── Step 5: Full RAG query ─────────────────────────────────────────────────

def rag_query(collection, question: str) -> str:
    """Retrieve → build prompt → generate. Prints retrieved chunks first."""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    chunks = retrieve(collection, question)
    print(f"\nRetrieved {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}] dist={chunk['distance']:.4f}  {chunk['metadata']['source']}")

    messages = build_messages(question, chunks)

    print(f"\nAnswer:\n")
    start = time.time()
    answer = generate(messages)
    print(f"[Generated in {time.time() - start:.1f}s]")

    return answer


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    client = chromadb.PersistentClient(path="./rag_db")
    collection = client.get_or_create_collection("course_docs")

    if collection.count() == 0:
        count = ingest(collection, "docs")
        print(f"Ingested {count} document chunks.")
    else:
        print(f"Using existing collection: {collection.count()} chunks.")

    print("\nRAG Pipeline ready! Type your question or 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if question:
            rag_query(collection, question)
