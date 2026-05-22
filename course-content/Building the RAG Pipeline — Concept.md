# Building the RAG Pipeline — Concept

**Module 8 — RAG Intro & Docker Deployment**

**Estimated time: 40 minutes**

---

### Learning Objectives

By the end of this lesson, you will be able to:

1. Build a complete RAG pipeline that ingests documents, retrieves relevant chunks, and generates grounded answers
2. Wire together ChromaDB retrieval with Ollama generation in a single workflow
3. Format retrieved context into effective RAG prompts with source citations
4. Implement streaming responses for a better user experience

---

`[VIDEO PLACEHOLDER: 10 min — "Building the RAG Pipeline: build the complete Ingest → Chunk → Embed → Store → Retrieve → Generate pipeline from scratch. Show a user asking a question and getting a grounded answer with citations."]`

You’ve built the individual pieces across two modules: embeddings and retrieval (Module 7), and local LLM inference (Lesson 2). Now you assemble them into a single, working pipeline.

Think of it like building a car. In previous lessons, you built the engine (embeddings), the fuel system (ChromaDB), and the transmission (Ollama). This lesson is where you bolt everything together, turn the key, and drive.

---

## The Pipeline in Code

A RAG pipeline has two phases:

**Ingestion (run once or when documents change):**

```
Load documents → Chunk text → Embed chunks → Store in ChromaDB
```

**Query (run per user question):**

```
Embed question → Search ChromaDB → Build prompt → Call Ollama → Return answer
```

You built the ingestion phase in Module 7. The query phase adds three new steps: prompt building, LLM calling, and response formatting.

---

## Prompt Template Design

The prompt template is the bridge between retrieval and generation. It needs to:

1. **Set the model’s role** (system prompt)
2. **Provide the retrieved context** with source labels
3. **Include the user’s question**
4. **Add guardrails** ("answer from context only", "cite sources", "say if you don’t know")

```python
RAG_SYSTEM_PROMPT = """You are a helpful AI assistant. Answer the user's question 
based ONLY on the context provided below. Follow these rules:

1. Only use information from the provided context
2. If the context doesn't contain the answer, say "I don't have enough 
   information to answer that based on the available documents."
3. Cite your sources by mentioning the document name
4. Keep your response concise and focused
"""

def build_rag_prompt(question, retrieved_chunks):
    """Assemble the RAG prompt from retrieved context and user question."""
    context_parts = []
    for chunk in retrieved_chunks:
        source = chunk["metadata"]["source"]
        text = chunk["text"]
        context_parts.append(f"[Source: {source}]\n{text}")

    context = "\n\n---\n\n".join(context_parts)

    return [
        {"role": "system", "content": RAG_SYSTEM_PROMPT + f"\nCONTEXT:\n{context}"},
        {"role": "user", "content": question}
    ]
```

---

## Streaming: Don’t Make Users Wait

LLMs generate text token-by-token. Without streaming, the user stares at a blank screen for 5–30 seconds until the entire response is ready. With streaming, tokens appear as they’re generated — the same experience you get in ChatGPT.

Ollama supports streaming by default. When `stream: True`, the API returns a series of JSON objects, each containing one token:

```python
import requests
import json

def stream_response(messages, model="llama3.2:1b"):
    """Stream a response from Ollama, yielding tokens."""
    response = requests.post("http://localhost:11434/api/chat", json={
        "model": model,
        "messages": messages,
        "stream": True
    }, stream=True)  # Both Ollama and requests need stream=True

    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            token = data.get("message", {}).get("content", "")
            if token:
                yield token  # Yield one token at a time
```

In Streamlit, `st.write_stream()` consumes this generator and displays each token as it arrives — exactly like the chat interface you built in Module 6.

---

## The Complete Flow

`[DIAGRAM PLACEHOLDER: Complete RAG pipeline flow showing: User Question → ChromaDB query() returns top-K chunks with metadata → build_rag_prompt() combines system prompt + context + question → stream_response() sends to Ollama → Tokens stream back to the user. Each step labeled with its function name and data type.]`

When everything is connected, a single user question triggers this chain:

1. ChromaDB finds the 3–5 most relevant document chunks
2. The prompt builder formats them with source labels and guardrails
3. Ollama generates an answer grounded in the retrieved context
4. Tokens stream back to the user in real-time
5. Source citations tell the user where the information came from

The entire round trip — from question to first visible token — should be under 2–3 seconds on a modern machine with a small model.