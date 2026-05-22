# Dockerfile Creation — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 10 min — "Build a Dockerfile: create a Dockerfile for the RAG FastAPI backend from Lesson 5. Show the build process, layer caching, and running the containerized API."]`

Let’s build a proper Dockerfile for the RAG API from Lesson 5. Create this project structure:

```
rag-docker-demo/
├── main.py            # Your RAG FastAPI app (from Lesson 5)
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── docs/              # Your document collection
    ├── fastapi_basics.txt
    └── streamlit_guide.txt
```

**`requirements.txt`:**

```
fastapi==0.109.0
uvicorn==0.27.0
chromadb==0.4.22
sentence-transformers==2.3.1
requests==2.31.0
pydantic==2.6.0
```

**`.dockerignore`:**

```
__pycache__
*.pyc
.git
.env
venv
chroma_data
.DS_Store
```

**`Dockerfile`:**

```docker
# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy and install Python dependencies first (caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and documents
COPY main.py .
COPY docs/ docs/

# Document the port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Build the Image

```bash
cd rag-docker-demo
docker build -t rag-api .
```

Watch the output — each instruction is a step. The first build downloads and installs everything. Subsequent builds (if you only change `main.py`) will reuse the cached layers for pip install.

---

## Run the Container

```bash
docker run -p 8000:8000 rag-api
```

Visit `http://localhost:8000/docs` — your RAG API is running inside a container.

Test the endpoints:

1. `POST /ingest` to load documents
2. `GET /stats` to verify
3. `POST /ask` with a question

---

## Verify Layer Caching

Change something in `main.py` (add a comment) and rebuild:

```bash
docker build -t rag-api .
```

Notice how the first few steps say `CACHED` — Docker skipped them because nothing changed. Only the `COPY main.py .` step and beyond re-run. This is the power of ordering your Dockerfile correctly.

`[DIAGRAM PLACEHOLDER: Build output showing CACHED steps for the first layers and only the code copy step rebuilding]`