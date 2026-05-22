# Reliability & Guardrails — Concept

**Module 8 — RAG Intro & Docker Deployment**

**Estimated time: 30 minutes**

---

### Learning Objectives

By the end of this lesson, you will be able to:

1. Identify the ways a RAG pipeline can fail and produce unreliable output
2. Implement confidence thresholds to filter low-quality retrieval results
3. Add hallucination mitigation techniques to your RAG system
4. Build basic guardrails that improve response reliability

---

`[VIDEO PLACEHOLDER: 7 min — "RAG Guardrails: show a RAG system giving a bad answer because retrieval was poor, then add confidence thresholds and prompt guardrails to fix it. Demonstrate the before/after."]`

You built a RAG pipeline in the last lesson. It works — most of the time. But "most of the time" isn’t good enough for a production application.

Imagine your RAG chatbot is answering customer questions about your product. A customer asks about a feature you don’t have documentation for. Without guardrails, the system retrieves marginally related documents, the LLM sees some context and generates a confident-sounding but incorrect answer, and the customer acts on wrong information.

This lesson is about making your RAG system say "I don’t know" when it should, and answer correctly when it can.

---

## Where RAG Can Fail

**Retrieval failures:**

- The relevant document doesn’t exist in the knowledge base
- The relevant document exists but wasn’t chunked in a way that captures the right information
- The retrieved chunks are loosely related but don’t actually answer the question

**Generation failures:**

- The model ignores the provided context and answers from training data
- The model combines information from multiple unrelated chunks in misleading ways
- The model hallucinates details not present in any retrieved document

---

## Guardrail 1: Confidence Thresholds

The simplest and most effective guardrail: don’t send low-relevance chunks to the LLM.

```python
def retrieve_with_threshold(collection, query, n_results=5, max_distance=1.0):
    """Only return chunks above a confidence threshold."""
    results = collection.query(query_texts=[query], n_results=n_results)

    filtered = []
    for i in range(len(results['documents'][0])):
        distance = results['distances'][0][i]
        if distance <= max_distance:  # Lower distance = more relevant
            filtered.append({
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": distance
            })

    return filtered
```

If no chunks pass the threshold, your system should say: "I don’t have relevant information to answer that question" instead of generating a response from irrelevant context.

---

## Guardrail 2: "No Context" Fallback

```python
def rag_query_safe(collection, question):
    chunks = retrieve_with_threshold(collection, question, max_distance=1.0)

    if not chunks:
        return {
            "answer": "I don't have enough relevant information in my "
                      "knowledge base to answer that question.",
            "sources": [],
            "confidence": "low"
        }

    # Proceed with normal RAG generation...
    messages = build_messages(question, chunks)
    answer = generate(messages)

    return {
        "answer": answer,
        "sources": [c["metadata"]["source"] for c in chunks],
        "confidence": "high" if chunks[0]["distance"] < 0.5 else "medium"
    }
```

Returning a structured response with confidence level and sources lets the frontend display the answer differently based on confidence.

---

## Guardrail 3: Prompt-Level Instructions

Strengthen the system prompt with explicit guardrails:

```python
SYSTEM_PROMPT = """You are a helpful AI assistant. Answer based ONLY on the 
provided context.

CRITICAL RULES:
1. If the context doesn't contain enough information, say: "I don't have 
   enough information to answer that."
2. NEVER make up information not present in the context.
3. If you're unsure, say you're unsure rather than guessing.
4. Always cite which source document your answer comes from.
5. If the context is only loosely related to the question, acknowledge this.
"""
```

Stronger, more explicit instructions improve reliability, especially with smaller models.

---

## Guardrail 4: Output Validation

Check the model’s response before showing it to the user:

```python
def validate_response(answer, retrieved_sources):
    """Basic checks on the generated response."""
    warnings = []

    # Check if the answer seems too confident for low-relevance retrieval
    if len(answer) > 500:
        warnings.append("Response unusually long — may contain hallucinated details")

    # Check if the answer mentions sources not in the retrieved set
    # (This is a rough heuristic — not foolproof)
    for word in ["according to", "source:", "from the"]:
        if word in answer.lower():
            # Verify the cited source exists in retrieved set
            pass  # Implementation depends on your source naming

    return warnings
```

---

## Putting It Together

A reliable RAG system has layers of defense:

1. **Retrieval threshold** — Don’t send bad context to the model
2. **No-context fallback** — Gracefully handle cases where nothing relevant is found
3. **Strong prompt** — Explicit instructions about when to say "I don’t know"
4. **Output validation** — Check the response before showing it to users
5. **Confidence indicators** — Show users how confident the system is

No single guardrail is enough. Defense in depth — the same principle from prompt injection awareness (Module 7) — applies to reliability too.