# Dockerfile Creation — Practice Exercise

## Dockerize Your RAG API

**Objective:** Write a Dockerfile for your RAG FastAPI backend from Week 1, build the image, and verify it runs correctly in a container.

**Time:** 30 minutes

**What you’ll do:**

1. Create a `Dockerfile` for your RAG API (from Lesson 5) that:
    - Uses `python:3.11-slim` as the base image
    - Installs system dependencies if needed (`build-essential`)
    - Copies `requirements.txt` first (layer caching)
    - Installs Python packages with `--no-cache-dir`
    - Copies your application code and `docs/` folder
    - Exposes port 8000
    - Runs uvicorn bound to `0.0.0.0`
2. Create a `.dockerignore` file excluding: `__pycache__`, `venv`, `.git`, `.env`, `chroma_data`
3. Build the image: `docker build -t my-rag-api .`
4. Run the container: `docker run -p 8000:8000 my-rag-api`
5. Test in your browser: visit `http://localhost:8000/docs` and call the `/ingest` and `/ask` endpoints
6. Verify caching: change a comment in your Python code, rebuild, and confirm that pip install is cached

**Deliverable:** A working Dockerfile that builds your RAG API into a Docker image. The API should be accessible at `localhost:8000` when the container runs.

**Why this exercise?** This Dockerfile becomes part of your module project. Getting it working now means the Docker Compose step (next lesson) builds on a solid foundation.