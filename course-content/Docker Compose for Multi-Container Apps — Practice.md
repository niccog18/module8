# Docker Compose for Multi-Container Apps — Practice Exercise

## Multi-Service RAG Stack

**Objective:** Build a Docker Compose setup with FastAPI backend and Ollama, verifying that they communicate correctly.

**Time:** 35 minutes

**What you’ll do:**

1. Create a project directory with the structure from the Guided Example
2. Write a `docker-compose.yml` with two services:
    - `backend` — Your RAG FastAPI app (built from a Dockerfile)
    - `ollama` — The Ollama service (using the `ollama/ollama` image)
3. Configure:
    - Port mappings for both services
    - Environment variables so the backend knows how to reach Ollama (`OLLAMA_URL`)
    - Named volumes for ChromaDB data and Ollama models
    - `depends_on` so backend starts after Ollama
4. Run `docker-compose up --build` and verify:
    - The backend’s `/health` endpoint shows `ollama: connected`
    - The backend’s root endpoint responds correctly
5. Test persistence:
    - Stop with `docker-compose down`
    - Restart with `docker-compose up`
    - Verify data survived (document count preserved)

**Deliverable:** A working Docker Compose setup where FastAPI and Ollama run as connected containers.

**Why this exercise?** This is the core of the module project. Adding a Streamlit frontend service (Lesson 10) will complete the full stack.