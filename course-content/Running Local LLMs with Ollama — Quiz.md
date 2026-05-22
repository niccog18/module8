# Running Local LLMs with Ollama — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** What is the main advantage of running an LLM locally with Ollama versus using a cloud API?

- A) Local models are always smarter than cloud models
- B) Local models are free to run, keep data on your machine, work offline, and give you full control of the stack
- C) Ollama models don’t require any RAM
- D) Local models are always faster

> **Answer: B** — Ollama lets you run models without API keys (free), without sending data to external servers (privacy), without internet (offline capable), and with full control over the model and infrastructure. Cloud APIs are often higher quality and faster, but they cost money per request and require sending your data to a third party.
> 

---

**Question 2:** How does your Python code communicate with Ollama?

- A) Through a special Python library that only works with Ollama
- B) Through a REST API on [localhost:11434](http://localhost:11434) — the same HTTP request/response pattern you’ve used since Module 4
- C) Through direct function calls to the model’s weights
- D) Through a WebSocket connection

> **Answer: B** — Ollama exposes a REST API on port 11434. You send POST requests with JSON bodies (containing the model name, messages, and options) and receive JSON responses. This is the same HTTP pattern you’ve used with FastAPI, Postman, and the `requests` library. The `/api/chat` endpoint even uses the same `{"role": ..., "content": ...}` message format as OpenAI.
> 

---

**Question 3:** For a RAG application running on a laptop during development, which model size is the best starting point?

- A) 70B+ parameters for the highest quality
- B) 1–8B parameters — fast enough for development, small enough to run on most laptops, and adequate for RAG where retrieved context does most of the work
- C) The largest model that fits in memory
- D) Model size doesn’t matter

> **Answer: B** — For RAG development, a 1–8B model is ideal. In RAG, the model’s job is to synthesize an answer from *provided* context — it doesn’t need to know everything, just follow instructions and write clearly. Smaller models handle this well. Larger models (70B+) require significant hardware and don’t improve RAG quality proportionally since the context does the heavy lifting.
>