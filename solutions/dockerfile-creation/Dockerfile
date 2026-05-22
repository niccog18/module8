# Dockerfile for RAG FastAPI Backend  (Solution)
# ================================================
# Build:  docker build -t my-rag-api .
# Run:    docker run -p 8000:8000 my-rag-api
# Test:   open http://localhost:8000/docs
#
# Key concepts:
#   python:3.11-slim — minimal Debian image with Python, no extras.
#     ~200 MB vs ~1 GB for the full python:3.11 image. Always use slim
#     for production unless you need compilers or GUI libraries.
#
#   Layer caching — the most important Dockerfile performance trick:
#     Docker caches each instruction as a layer. If nothing above a layer
#     changed, Docker reuses the cached layer and skips re-running it.
#     Copying requirements.txt BEFORE application code means pip install
#     is cached as long as requirements.txt hasn't changed. This saves
#     minutes on every rebuild during development.
#
#   --host 0.0.0.0 — REQUIRED for containers:
#     By default uvicorn binds to 127.0.0.1 (localhost inside the container).
#     Nothing outside the container can reach it. 0.0.0.0 binds to all
#     network interfaces, making the port accessible via -p 8000:8000.
#
#   .dockerignore — keeps the build context small:
#     Docker sends all files in the build context to the daemon before
#     building. Excluding venv/, .git/, and rag_db/ avoids sending hundreds
#     of MB of irrelevant files. See .dockerignore alongside this file.

FROM python:3.11-slim

WORKDIR /app

# ── Layer 1: system deps (uncomment if chromadb needs build-essential) ────
# RUN apt-get update && apt-get install -y build-essential \
#     && rm -rf /var/lib/apt/lists/*

# ── Layer 2: Python dependencies (cached unless requirements.txt changes) ─
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Layer 3: Application code ─────────────────────────────────────────────
# Copied AFTER pip install so a code change doesn't invalidate the pip cache
COPY my_rag_api.py .
COPY docs/ docs/

# ── Runtime ───────────────────────────────────────────────────────────────
EXPOSE 8000

CMD ["uvicorn", "my_rag_api:app", "--host", "0.0.0.0", "--port", "8000"]
