"""
L1 — Running Local LLMs with Ollama: Explorer  (Solution)
===========================================================
Run with:
    python solution.py

Prerequisites: Ollama running (`ollama serve`) with a model pulled.

Key concepts:
    System prompts dramatically shape output:
        The same question — "What is an API?" — produces a children's story, a
        casual explanation, and a technical architecture overview depending solely
        on the system prompt. This is the cheapest tuning lever you have.

    RAG grounding works — when you enforce it:
        With a strict "answer ONLY from context" prompt, a well-behaved model
        will correctly refuse questions whose answers aren't in the context.
        Without that instruction, models hallucinate confidently.

    Response time scales with output length, not input length:
        Longer questions don't necessarily produce longer answers. What matters
        is how many tokens the model generates. A short "yes/no" question can
        produce a long answer if the model decides to elaborate.

    Temperature controls creativity vs. determinism:
        Low temperature (0.1) → nearly identical outputs on repeated calls.
        High temperature (1.0) → varied, sometimes surprising outputs.
        For RAG, keep temperature low (0.1–0.3) to stay grounded in the context.
"""

import requests
import time

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"  # Change to match your downloaded model


# ── Core helper ────────────────────────────────────────────────────────────

def generate(messages: list[dict], temperature: float = 0.7) -> tuple[str, float]:
    """Call Ollama /api/chat. Returns (response_text, elapsed_seconds)."""
    try:
        start = time.time()
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            },
        )
        elapsed = time.time() - start
        return response.json()["message"]["content"], elapsed
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running? (ollama serve)", 0.0


# ── Experiment 1: System prompt comparison ─────────────────────────────────

def experiment_1():
    """Same question, three different system prompts."""
    question = "What is an API?"

    prompts = [
        ("No system prompt",
         ""),
        ("ELI5",
         "Explain like I'm 5 years old. Use very simple words and a fun analogy."),
        ("Technical architect",
         "You are a senior software architect. Be technical and precise. "
         "Use correct terminology. Assume the reader is an experienced developer."),
    ]

    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Same question, different system prompts")
    print("=" * 60)

    for label, system_prompt in prompts:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": question})

        text, elapsed = generate(messages)
        print(f"\n[{label}] ({elapsed:.1f}s)")
        print(text)
        print()

    # Observation: The same factual question produces wildly different answers.
    # ELI5 uses analogies ("like a waiter in a restaurant").
    # Technical gives HTTP methods, REST constraints, status codes.
    # No system prompt falls somewhere in between.


# ── Experiment 2: RAG-style context grounding ──────────────────────────────

def experiment_2():
    """Provide context; test answerable vs. unanswerable question."""

    context = (
        "FastAPI is a modern Python web framework for building APIs. "
        "It uses Python type hints for automatic validation and generates "
        "interactive API documentation via Swagger UI at /docs. "
        "FastAPI is built on top of Starlette and Pydantic. "
        "It supports async/await natively and is one of the fastest Python frameworks."
    )

    answerable_question = "What documentation does FastAPI generate automatically?"
    unanswerable_question = "How do I deploy FastAPI to AWS Lambda?"

    system_prompt = (
        "Answer ONLY from the provided context. "
        "If the context does not contain the answer, say exactly: "
        "'I don't have enough information to answer that.'"
    )

    print("\n" + "=" * 60)
    print("EXPERIMENT 2: RAG-style context grounding")
    print("=" * 60)
    print(f"\nContext provided:\n{context}\n")

    for label, question in [
        ("Answerable", answerable_question),
        ("Unanswerable", unanswerable_question),
    ]:
        user_content = f"Context:\n{context}\n\nQuestion: {question}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_content},
        ]
        text, elapsed = generate(messages)
        print(f"\n[{label}] {question}")
        print(f"Answer ({elapsed:.1f}s): {text}")

    # Observation: The answerable question gets a correct, grounded response.
    # The unanswerable question should produce the refusal phrase — but some
    # models still try to answer from training data. This is why guardrails
    # (distance thresholds + stronger prompts) are needed in production.


# ── Experiment 3: Response timing ──────────────────────────────────────────

def experiment_3():
    """Ask questions of varying length, compare response times."""

    questions = [
        ("Short  (~5 words)",  "What is Python?"),
        ("Medium (~20 words)", "Can you explain the difference between synchronous and asynchronous programming in Python with a simple example?"),
        ("Long   (~50 words)", (
            "I am building a REST API with FastAPI that needs to handle "
            "user authentication, store data in a PostgreSQL database, and "
            "return JSON responses. The API will be deployed in a Docker "
            "container. What are the key architectural decisions I should "
            "make and what libraries would you recommend for each concern?"
        )),
    ]

    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Response timing")
    print("=" * 60)

    for label, question in questions:
        messages = [{"role": "user", "content": question}]
        _, elapsed = generate(messages)
        print(f"\n{label}: {elapsed:.2f}s")
        print(f"  Question length: {len(question)} chars")

    # Observation: Response time correlates more with OUTPUT length than input
    # length. A short question that triggers a long explanation takes longer
    # than a long question with a short factual answer.


# ── Experiment 4 (bonus): Temperature comparison ───────────────────────────

def experiment_4():
    """Same prompt, temperature 0.1 vs 1.0."""
    question = "Tell me a one-sentence fact about the ocean."

    print("\n" + "=" * 60)
    print("EXPERIMENT 4 (Bonus): Temperature comparison")
    print("=" * 60)

    for temp in [0.1, 1.0]:
        messages = [{"role": "user", "content": question}]
        text, elapsed = generate(messages, temperature=temp)
        print(f"\n[temperature={temp}] ({elapsed:.1f}s)")
        print(text)

    # Run this experiment 3 times and compare. At temp=0.1, you'll get nearly
    # identical sentences. At temp=1.0, each run produces a different fact.
    # For RAG: use low temperature (0.1–0.3) so the model stays grounded.


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()
