# Containerizing Your RAG Application — Practice Exercise

## The Full Containerized Stack

**Objective:** Build the complete three-service Docker Compose setup for your RAG application and verify end-to-end functionality.

**Time:** 45 minutes

**What you’ll do:**

1. Create the full project structure with `backend/`, `frontend/`, and root-level files
2. Write Dockerfiles for both backend (FastAPI) and frontend (Streamlit)
3. Write a `docker-compose.yml` with three services: `backend`, `frontend`, `ollama`
4. Configure environment variables, port mappings, volumes, and dependencies
5. Build and run: `docker-compose up --build`
6. Pull the Ollama model: `docker-compose exec ollama ollama pull llama3.2:1b`
7. Verify the complete flow:
    - Visit `http://localhost:8501` (Streamlit)
    - Click Re-index Documents
    - Ask a question
    - See the answer with source citations
    - Check the health endpoint at `http://localhost:8000/health`

**Deliverable:** A complete, containerized RAG application running with `docker-compose up`. All three services communicating correctly.

**Why this exercise?** This IS the module project, minus polish. Getting the three-service stack working end-to-end now means the project is about adding quality — better documents, better UI, better README — not debugging infrastructure.