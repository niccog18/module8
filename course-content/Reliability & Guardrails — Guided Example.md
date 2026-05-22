# Reliability & Guardrails — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 8 min — "Guardrails Demo: show a RAG system without guardrails answering poorly, then add threshold filtering, no-context fallback, and confidence levels. Before/after comparison."]`

Let’s add guardrails to a RAG pipeline and see the before/after difference. Create `guardrails_demo.py`:

```python
import chromadb

# --- Setup: Mini knowledge base ---
client = chromadb.Client()
collection = client.get_or_create_collection("demo")

documents = [
    "FastAPI uses Pydantic models for automatic request validation.",
    "JWT tokens provide stateless authentication for REST APIs.",
    "ChromaDB stores document embeddings for similarity search.",
    "Streamlit session state persists data across re-runs.",
]
collection.add(
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))],
    metadatas=[{"source": f"module{i+3}.md"} for i in range(len(documents))]
)

# --- Without guardrails ---
def naive_retrieve(query, n_results=3):
    results = collection.query(query_texts=[query], n_results=n_results)
    return [
        {"text": results['documents'][0][i],
         "distance": results['distances'][0][i],
         "source": results['metadatas'][0][i]['source']}
        for i in range(len(results['documents'][0]))
    ]

# --- With guardrails ---
def safe_retrieve(query, n_results=3, max_distance=1.0):
    results = collection.query(query_texts=[query], n_results=n_results)
    filtered = []
    for i in range(len(results['documents'][0])):
        dist = results['distances'][0][i]
        if dist <= max_distance:
            filtered.append({
                "text": results['documents'][0][i],
                "distance": dist,
                "source": results['metadatas'][0][i]['source']
            })
    return filtered

def get_confidence(chunks):
    if not chunks:
        return "none", "🔴"
    best = chunks[0]["distance"]
    if best < 0.5:
        return "high", "🟢"
    elif best < 1.0:
        return "medium", "🟡"
    else:
        return "low", "🔴"

def answer_with_guardrails(query):
    chunks = safe_retrieve(query, max_distance=1.2)
    confidence, icon = get_confidence(chunks)

    print(f"\n  Confidence: {icon} {confidence}")
    print(f"  Chunks retrieved: {len(chunks)}")

    if not chunks:
        print("  Answer: I don't have relevant information to answer that.")
        return

    for c in chunks:
        print(f"    [{c['distance']:.3f}] {c['source']}: {c['text'][:60]}...")

    if confidence == "low":
        print("  Answer: I found some loosely related information, but "
              "I'm not confident it answers your question:")
    print(f"  Answer: [Would generate from {len(chunks)} chunks using Ollama]")

# --- Compare ---
queries = [
    "How does FastAPI validate data?",          # In scope — should answer well
    "How do I deploy to Kubernetes?",           # Out of scope — should refuse
    "What is a vector database?",               # Partially in scope
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Query: '{query}'")

    print(f"\n  --- Without guardrails ---")
    naive = naive_retrieve(query)
    for c in naive:
        print(f"    [{c['distance']:.3f}] {c['source']}: {c['text'][:60]}...")
    print(f"  [Would send ALL {len(naive)} chunks to LLM regardless of relevance]")

    print(f"\n  --- With guardrails ---")
    answer_with_guardrails(query)
```

Run it:

```bash
python guardrails_demo.py
```

---

## What You Should See

For the in-scope query (FastAPI validation): both approaches find relevant chunks, but guardrails add confidence indicators.

For the out-of-scope query (Kubernetes): the naive approach still returns chunks (the most loosely related ones), which could lead to hallucination. Guardrails filter them out and return a "don’t know" response.

For the partially-in-scope query (vector database): guardrails show medium confidence, signaling to the user that the answer may be incomplete.

`[DIAGRAM PLACEHOLDER: Side-by-side comparison showing naive retrieval sending irrelevant chunks to the LLM vs. guardrailed retrieval filtering them out and returning "I don’t know"]`