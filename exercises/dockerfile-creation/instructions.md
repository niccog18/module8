# Dockerfile Creation

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 30 minutes

## Objective

Write a Dockerfile for your RAG FastAPI backend, build the image, and verify it runs correctly in a container.

## What You'll Build

- **`Dockerfile`** — Multi-step build for the FastAPI RAG backend
- **`.dockerignore`** — Exclude files that shouldn't be in the image

## Dockerfile Requirements

- Base image: `python:3.11-slim`
- Install system dependencies if needed (`build-essential`)
- Copy `requirements.txt` first (to benefit from layer caching)
- Install Python packages with `--no-cache-dir`
- Copy application code and `docs/` folder
- Expose port `8000`
- Run uvicorn bound to `0.0.0.0`

## .dockerignore Requirements

Exclude: `__pycache__`, `*.pyc`, `venv/`, `.git/`, `.env`, `chroma_data/`, `rag_db/`

## Reference Code

The starter `Dockerfile` and `.dockerignore` provide scaffolding with TODOs.

## Running

```bash
docker build -t my-rag-api .
docker run -p 8000:8000 my-rag-api
```

Then visit `http://localhost:8000/docs` to test.

## Caching Verification

Change a comment in your Python code, rebuild, and confirm that the `pip install` layer is cached (it should say `CACHED`).

## Deliverable

A working `Dockerfile` that builds your RAG API into an image accessible at `localhost:8000`.
