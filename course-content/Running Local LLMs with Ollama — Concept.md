# Running Local LLMs with Ollama — Concept

**Module 8 — RAG Intro & Docker Deployment**

**Estimated time: 35 minutes**

---

### Learning Objectives

By the end of this lesson, you will be able to:

1. Explain what Ollama is and why running LLMs locally matters for development and privacy
2. Install Ollama and download a language model
3. Interact with a local LLM from the command line and from Python
4. Compare local LLMs with cloud API options and choose the right one for your use case

---

`[VIDEO PLACEHOLDER: 7 min — "Running Local LLMs with Ollama: install Ollama, pull a model, run it, chat with it from the terminal. 'You now have an AI model running entirely on your machine.'"]`

Up to this point, every time you’ve interacted with an AI model, it’s been through someone else’s server — OpenAI’s, Anthropic’s, or Google’s. You send your text over the internet, their server processes it, and sends back a response.

That works great for many use cases. But it comes with tradeoffs: you need an API key (which costs money per request), your data leaves your machine (privacy concern for sensitive documents), you need an internet connection, and you’re subject to the provider’s rate limits and policies.

What if you could run the AI model right on your own computer? No internet required. No API keys. No data leaving your machine. No per-request costs.

That’s what **Ollama** does.

---

## What Is Ollama?

Ollama is a tool that makes it easy to download and run open-source language models locally on your machine. Think of it as the "Docker for LLMs" — you pull a model (like pulling a Docker image), and it runs locally.

Models available through Ollama include:

- **Llama 3** (Meta) — General-purpose, good quality, multiple sizes
- **Mistral** — Efficient and fast, strong for its size
- **Phi** (Microsoft) — Very small, designed for edge/local use
- **Gemma** (Google) — Open model from Google
- Many more open-source models

The model runs entirely on your hardware. For smaller models (7B parameters), a modern laptop with 8GB+ RAM handles it fine. Larger models (13B+) benefit from more RAM or a GPU.

---

## Installation

**macOS:**

```bash
brew install ollama
```

Or download from [ollama.com](http://ollama.com)

**Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**

Download the installer from [ollama.com](http://ollama.com)

After installation, start the Ollama server:

```bash
ollama serve
```

This starts a local server on `http://localhost:11434` that accepts HTTP requests — the same interface pattern as your FastAPI apps.

`[VERIFY: Installation commands may change. Students should check ollama.com for the latest instructions.]`

---

## Pulling and Running a Model

Download a model (this happens once; the model is cached locally):

```bash
ollama pull llama3.2:1b    # Small and fast (1.3GB download)
```

Chat with it from the terminal:

```bash
ollama run llama3.2:1b
```

You’ll get an interactive prompt. Type a question, get an answer. Type `/bye` to exit. The model is running entirely on your machine — unplug your internet and it still works.

---

## Ollama’s REST API

Ollama exposes a REST API on `localhost:11434` — the same HTTP protocol you’ve been working with since Module 4. This is how your Python code will interact with it:

```python
import requests

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2:1b",
    "prompt": "What is FastAPI?",
    "stream": False  # Get the complete response at once
})

data = response.json()
print(data["response"])
```

For chat-style interactions (with message history):

```python
response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2:1b",
    "messages": [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "How do I create a FastAPI endpoint?"}
    ],
    "stream": False
})

data = response.json()
print(data["message"]["content"])
```

Notice the message format: `{"role": "...", "content": "..."}`. This is the same format used by OpenAI’s API and the chat history pattern from your Streamlit chat interface (Module 6, Lesson 12). The industry has standardized on this format.

---

## Local vs. Cloud: When to Use Which

**Use local (Ollama) when:**

- Developing and testing (no API costs while iterating)
- Working with sensitive/private data
- Offline or in restricted network environments
- Running in Docker containers (you control the whole stack)

**Use cloud APIs (OpenAI, Anthropic) when:**

- You need the highest quality responses (GPT-4, Claude are still ahead)
- You don’t have enough local hardware for larger models
- You need to scale to many concurrent users
- Response time matters and you have a fast internet connection

For this course and your capstone project, Ollama is the right choice: it’s free, private, containerizable, and teaches you how the full stack works without external dependencies.

---

## Model Sizes: Choosing the Right One

Language models come in different sizes, measured in **parameters** (billions):

- **1–3B** (e.g., `llama3.2:1b`, `phi3:mini`): Fast, runs on any laptop. Good enough for basic RAG with well-retrieved context. ~1–2GB download.
- **7–8B** (e.g., `llama3.1:8b`, `mistral`): Solid quality, needs 8GB+ RAM. The sweet spot for local development. ~4–5GB download.
- **13B+** (e.g., `llama3.1:70b`): High quality, needs 16GB+ RAM or GPU. Overkill for development.

For this module, we’ll use `llama3.2:1b` or `llama3.1:8b` depending on your hardware. The smaller model is fine for learning — the RAG architecture is what matters, not the model’s raw intelligence.