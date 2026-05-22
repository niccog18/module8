# Knowledge Check: RAG & Containerization Concepts

**Module 8 — RAG Intro & Docker Deployment**

**Mid-Module Assessment — Covers Week 1 (RAG Pipeline) plus preview of Docker concepts**

---

**Question 1:** What is RAG (Retrieval-Augmented Generation), and how does it improve over using an LLM alone?

- A) RAG retrains the LLM on new data
- B) RAG retrieves relevant documents from a knowledge base and provides them as context to the LLM, grounding its responses in actual source material instead of relying on training data alone
- C) RAG replaces the LLM with a search engine
- D) RAG only works with cloud-hosted models

> **Answer: B** — RAG combines retrieval (finding relevant documents) with generation (LLM producing an answer). By providing actual source material as context, RAG reduces hallucination, works with current information, and enables the model to answer about private data it was never trained on.
> 

---

**Question 2:** Put these RAG pipeline stages in the correct order:

- A) Generate answer → Retrieve documents → Embed query → Build prompt
- B) Embed query → Retrieve from vector DB → Build prompt with context → Send to LLM → Generate answer
- C) Build prompt → Generate answer → Embed query → Retrieve documents
- D) Retrieve documents → Generate answer → Build prompt → Embed query

> **Answer: B** — The pipeline flows: embed the question, search the vector database for similar chunks, assemble a prompt with system instructions + retrieved context + question, send to the LLM, and receive the generated answer. Each stage feeds into the next.
> 

---

**Question 3:** What does Ollama do in the RAG stack?

- A) It stores document embeddings
- B) It provides the Streamlit interface
- C) It runs open-source language models locally for text generation, replacing the need for cloud API calls
- D) It creates document chunks

> **Answer: C** — Ollama downloads and runs open-source LLMs (like Llama, Mistral, Phi) on your local machine. It exposes a REST API on port 11434 that your FastAPI backend calls to generate answers. This means no API keys, no per-request costs, and no data leaving your machine.
> 

---

**Question 4:** Why are confidence thresholds an important guardrail in RAG systems?

- A) They make the LLM generate longer answers
- B) They filter out low-relevance retrieval results before they reach the LLM, preventing the model from generating answers based on irrelevant context
- C) They limit how many users can query the system
- D) They improve ChromaDB’s search speed

> **Answer: B** — Without thresholds, ChromaDB always returns *something* even for out-of-scope questions. These loosely related chunks can mislead the LLM into generating confident but incorrect answers. Thresholds ensure only genuinely relevant context reaches the model, and when nothing passes the threshold, the system returns "I don’t know" instead of hallucinating.
> 

---

**Question 5 (Docker preview):** What is a Dockerfile?

- A) A running instance of an application
- B) A text file containing step-by-step instructions for building a Docker image — specifying the base OS, dependencies, files to include, and the command to start the application
- C) A database for storing Docker containers
- D) A configuration file for Ollama

> **Answer: B** — A Dockerfile is a recipe. It starts with a base image (like `python:3.11-slim`), adds your code and dependencies, and defines how to start the application. When you run `docker build`, Docker follows these instructions to create an image. An image is a snapshot; a container is a running instance of that image.
> 

---

**Question 6 (Docker preview):** Why does containerization matter especially for AI applications?

- A) Containers make AI models more intelligent
- B) AI apps have complex dependencies (Python versions, ML libraries, database drivers, model files) that are hard to install consistently — containers package everything together so the app runs identically on any machine
- C) Containers are required for Python applications
- D) Containers replace the need for version control

> **Answer: B** — AI applications are notoriously difficult to set up: specific Python versions, GPU drivers, ML framework versions, system libraries, model files, and database configurations. Docker packages ALL of these into a single container that runs identically on a developer’s laptop, a CI server, or a cloud deployment. "Works on my machine" becomes "works everywhere."
> 

---

**Question 7 (Docker preview):** What is the difference between a Docker image and a Docker container?

- A) Images are for production; containers are for development
- B) An image is a static snapshot (template) built from a Dockerfile; a container is a running instance of that image
- C) Containers are larger than images
- D) There is no difference

> **Answer: B** — Think of an image as a class definition and a container as an object (instance). The image is the template: your code, dependencies, and configuration frozen in a snapshot. A container is a running copy of that image, with its own processes and state. You can run multiple containers from the same image.
> 

---

**Question 8 (Docker preview):** What does Docker Compose do that a single Dockerfile cannot?

- A) Builds faster images
- B) Defines and runs multi-container applications — coordinating multiple services (FastAPI, Streamlit, ChromaDB, Ollama) that work together as one system
- C) Replaces the need for Docker
- D) Only works on Linux

> **Answer: B** — A Dockerfile builds one service. Docker Compose coordinates multiple services into a single application. For your RAG project, you need FastAPI, Streamlit, ChromaDB, and Ollama all running together and communicating. Docker Compose defines all services in one `docker-compose.yml` file and starts everything with `docker-compose up`.
>