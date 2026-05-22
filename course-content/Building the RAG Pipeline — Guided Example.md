# Building the RAG Pipeline — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 12 min — "Complete RAG Pipeline: build rag_pipeline.py from scratch. Load documents, create ChromaDB collection, implement the query function with Ollama, and demonstrate it answering questions with citations."]`

Let’s build the complete RAG pipeline in a single file. Create `rag_pipeline.py`:

```python
import chromadb
import requests
import json
import os
import time

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"  # Adjust based on your downloaded model

# --- Step 1: Ingestion ---

def load_documents(directory):
    """Load all .txt and .md files from a directory."""
    docs = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(('.txt', '.md')):
            with open(os.path.join(directory, filename), 'r') as f:
                content = f.read()
            # Split by paragraphs for chunking
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            for i, para in enumerate(paragraphs):
                docs.append({
                    "text": para,
                    "id": f"{filename}_{i}",
                    "metadata": {"source": filename, "chunk_index": str(i)}
                })
    return docs

def ingest(collection, docs_directory):
    """Load, chunk, and store documents in ChromaDB."""
    chunks = load_documents(docs_directory)
    if not chunks:
        print("No documents found!")
        return 0

    collection.upsert(
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[c["id"] for c in chunks]
    )
    return len(chunks)

# --- Step 2: Retrieval ---

def retrieve(collection, query, n_results=3):
    """Search ChromaDB for relevant document chunks."""
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    chunks = []
    for i in range(len(results['documents'][0])):
        chunks.append({
            "text": results['documents'][0][i],
            "metadata": results['metadatas'][0][i],
            "distance": results['distances'][0][i]
        })
    return chunks

# --- Step 3: Prompt Building ---

SYSTEM_PROMPT = """You are a helpful AI assistant for students learning AI engineering.
Answer the user's question based ONLY on the context provided below.

Rules:
- Only use information from the CONTEXT section
- If the context doesn't contain the answer, say "I don't have enough information
  to answer that based on the available documents."
- Cite your sources by mentioning the document name in parentheses
- Keep your response under 200 words
"""

def build_messages(question, retrieved_chunks):
    """Build the RAG prompt with retrieved context."""
    context_parts = []
    for chunk in retrieved_chunks:
        source = chunk['metadata']['source']
        context_parts.append(f"[Source: {source}]\n{chunk['text']}")

    context = "\n\n---\n\n".join(context_parts)
    system_with_context = f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"

    return [
        {"role": "system", "content": system_with_context},
        {"role": "user", "content": question}
    ]

# --- Step 4: Generation ---

def generate(messages, stream=False):
    """Call Ollama to generate a response."""
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL,
            "messages": messages,
            "stream": stream
        }, stream=stream)

        if stream:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        print(token, end="", flush=True)  # Print as they arrive
                        full_response += token
            print()  # Newline after streaming
            return full_response
        else:
            return response.json()["message"]["content"]

    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running? (ollama serve)"

# --- Step 5: The RAG Function ---

def rag_query(collection, question, n_results=3, stream=True):
    """Complete RAG pipeline: retrieve + build prompt + generate."""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    # Retrieve
    chunks = retrieve(collection, question, n_results)
    print(f"\nRetrieved {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}] (dist: {chunk['distance']:.4f}) {chunk['metadata']['source']}")

    # Build prompt
    messages = build_messages(question, chunks)

    # Generate
    print(f"\nAnswer (streaming):\n")
    start = time.time()
    answer = generate(messages, stream=stream)
    elapsed = time.time() - start
    print(f"\n[Generated in {elapsed:.1f}s]")

    return answer

# --- Main ---
if __name__ == "__main__":
    # Create ChromaDB collection
    client = chromadb.PersistentClient(path="./rag_db")
    collection = client.get_or_create_collection("course_docs")

    # Ingest documents (only if collection is empty)
    if collection.count() == 0:
        count = ingest(collection, "docs")
        print(f"Ingested {count} document chunks.")
    else:
        print(f"Using existing collection: {collection.count()} chunks")

    # Interactive query loop
    print("\nRAG Pipeline Ready! Ask questions about your documents.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ('quit', 'exit', 'q'):
            break
        if question:
            rag_query(collection, question)
```

---

## Running It

1. Make sure you have a `docs/` folder with text files (reuse from Module 7 or create new ones)
2. Make sure Ollama is running (`ollama serve`)
3. Run the pipeline:

```bash
python rag_pipeline.py
```

Type questions and watch the full RAG chain in action: retrieval results are shown first, then the LLM streams a grounded answer.

---

## What You Should See

For each question:

- Which chunks were retrieved (with distance scores and sources)
- The streaming answer appearing token-by-token
- Source citations in the answer
- Response timing

Try questions that ARE in your documents and questions that AREN’T. The model should attempt to answer the first type from context and indicate insufficient information for the second.

`[DIAGRAM PLACEHOLDER: Terminal screenshot showing a question, retrieved chunks with scores, and a streaming answer with source citations]`