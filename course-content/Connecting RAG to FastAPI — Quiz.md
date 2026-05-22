# Connecting RAG to FastAPI — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** Why wrap a RAG pipeline in a FastAPI application instead of running it as a standalone script?

- A) FastAPI makes the model smarter
- B) An API allows multiple clients (Streamlit, mobile apps, other services) to access the RAG pipeline over HTTP, enables authentication, and is necessary for containerization
- C) Scripts can’t access ChromaDB
- D) FastAPI is required by Ollama

> **Answer: B** — A standalone script only runs locally for one user. An API makes the RAG pipeline accessible to any HTTP client: Streamlit frontends, mobile apps, other microservices, or automated tools. It also enables authentication (so you control access), proper error handling with status codes, and clean containerization in Docker.
> 

---

**Question 2:** What Pydantic model would you use for the `/ask` endpoint response?

- A) Just return a plain string
- B) A structured model with `answer` (str), `sources` (list of source objects), and `confidence` (str) fields
- C) Return the raw Ollama API response
- D) Return only the ChromaDB query results

> **Answer: B** — A structured response model gives clients everything they need: the answer text, which sources were used (for verification), and a confidence level (for UI adaptation). Returning a plain string (A) loses the metadata. Returning raw Ollama or ChromaDB responses (C, D) exposes internal implementation details to the client.
>