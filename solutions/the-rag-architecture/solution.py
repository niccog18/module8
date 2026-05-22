"""
L2 — The RAG Architecture: Prompt Builder  (Solution)
=======================================================
Run with:
    python solution.py

Key concepts:
    RAG prompt structure:
        Every RAG prompt has 3 parts assembled in order:
        1. System instruction — tells the model how to behave
        2. Context — the retrieved document chunks, each labelled with its source
        3. User question — what the user actually wants to know

        This separation matters: the system prompt sets the rules, the context
        provides the facts, and the question focuses the response.

    format_chunks():
        Labelling each chunk with its source is critical — it's what lets the
        model cite its references. Without labels, the model can't say
        "according to doc1.txt...".

    token_estimate():
        GPT-4 averages ~4 characters per token. This rough estimate lets you
        check whether a prompt will fit within a model's context window before
        sending it. A 128k-token model can handle ~512k characters.

    Prompt assembly:
        The order is deliberate: system rules first (high-weight), then context
        (medium-weight), then the question (active frame). Putting instructions
        after the context reduces their influence on some models.
"""

# ── System prompt ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful AI assistant.
Answer the user's question based ONLY on the context provided below.

Rules:
- Only use information from the CONTEXT section.
- If the context doesn't contain the answer, say "I don't have enough information to answer that."
- Cite your sources by mentioning the document name in parentheses.
- Keep your response concise — under 200 words.
"""


# ── Helpers ────────────────────────────────────────────────────────────────

def format_chunks(chunks: list[dict]) -> str:
    """Format a list of chunk dicts into a labelled context string."""
    parts = []
    for chunk in chunks:
        parts.append(f"[Source: {chunk['source']}]\n{chunk['text']}")
    return "\n\n---\n\n".join(parts)


def token_estimate(text: str) -> int:
    """Rough token count: characters // 4 (GPT-4 average)."""
    return len(text) // 4


def build_prompt(question: str, chunks: list[dict]) -> str:
    """Assemble the full RAG prompt: system + context + question."""
    context_block = "CONTEXT:\n" + format_chunks(chunks)
    return f"{SYSTEM_PROMPT}\n{context_block}\n\nUSER QUESTION: {question}"


# ── Test runner ────────────────────────────────────────────────────────────

def run_test(question: str, chunks: list[dict]) -> None:
    """Assemble and print a prompt with token count estimate."""
    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)
    prompt = build_prompt(question, chunks)
    print(prompt)
    print("-" * 70)
    print(f"Estimated tokens: ~{token_estimate(prompt)}")


# ── Test cases ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Test case 1: question answerable from context
    run_test(
        question="What is ChromaDB used for?",
        chunks=[
            {
                "text": (
                    "ChromaDB is an open-source vector database designed for "
                    "storing and querying embeddings. It is commonly used in RAG "
                    "pipelines to store document chunks as vectors and retrieve the "
                    "most semantically similar ones given a user query."
                ),
                "source": "chromadb-overview.txt",
                "distance": 0.21,
            },
            {
                "text": (
                    "ChromaDB supports both in-memory and persistent storage modes. "
                    "The PersistentClient saves the database to disk so data survives "
                    "restarts. Collections group related documents, similar to tables "
                    "in a relational database."
                ),
                "source": "chromadb-overview.txt",
                "distance": 0.35,
            },
        ],
    )

    # Test case 2: question NOT answerable from context — model should refuse
    run_test(
        question="What is the capital of France?",
        chunks=[
            {
                "text": (
                    "FastAPI is a modern Python web framework for building APIs. "
                    "It uses Python type hints to generate automatic validation, "
                    "serialisation, and interactive documentation via Swagger UI."
                ),
                "source": "fastapi-intro.md",
                "distance": 1.45,
            },
        ],
    )
