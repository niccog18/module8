import requests
import time

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"  # Use whatever model you pulled

def check_ollama():
    """Verify Ollama is running."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags")
        models = [m["name"] for m in r.json().get("models", [])]
        print(f"Ollama is running. Available models: {models}")
        return True
    except requests.exceptions.ConnectionError:
        print("ERROR: Ollama is not running. Start it with: ollama serve")
        return False

def generate(prompt, system="You are a helpful assistant."):
    """Send a prompt to Ollama and return the response."""
    start = time.time()

    response = requests.post(f"{OLLAMA_URL}/api/chat", json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "stream": False  # Wait for the complete response
    })

    elapsed = time.time() - start
    data = response.json()
    text = data["message"]["content"]

    print(f"[Generated in {elapsed:.1f}s]")
    return text

# --- Run the demo ---
if not check_ollama():
    exit(1)

print("\n" + "=" * 60)
print("TEST 1: Basic question")
print("=" * 60)
response = generate("What is a REST API? Explain in 2-3 sentences.")
print(response)

print("\n" + "=" * 60)
print("TEST 2: With system prompt (RAG-style)")
print("=" * 60)

context = (
    "FastAPI is a modern Python web framework. It uses Pydantic for validation "
    "and generates automatic API documentation at /docs."
)

rag_system = (
    "Answer the user's question based ONLY on the following context. "
    "If the context doesn't contain the answer, say 'I don't have enough "
    "information to answer that.'\\n\\n"
    f"CONTEXT:\\n{context}"
)

response = generate(
    "What framework should I use to build a Python API?",
    system=rag_system
)
print(response)

print("\n" + "=" * 60)
print("TEST 3: Question outside the context (should admit ignorance)")
print("=" * 60)
response = generate(
    "How do I deploy to Kubernetes?",
    system=rag_system
)
print(response)