# CI/CD Basics with GitHub Actions — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 8 min — "GitHub Actions Setup: create a workflow file, push to GitHub, watch the CI pipeline run. Show the green checkmark on success and how to debug a failing build."]`

Let’s create a CI workflow for your RAG project. Create the workflow directory and file:

```bash
mkdir -p .github/workflows
```

Create `.github/workflows/ci.yml`:

```yaml
name: RAG Application CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # Job 1: Run Python tests
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend  # Run commands from backend dir

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest httpx  # Test dependencies

      - name: Run tests
        run: pytest tests/ -v --tb=short
        env:
          OLLAMA_URL: http://localhost:11434  # Won't actually connect in CI
          CHROMA_PATH: ./test_chroma

  # Job 2: Verify Docker builds
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build backend image
        run: docker build -t rag-backend ./backend

      - name: Build frontend image
        run: docker build -t rag-frontend ./frontend

      - name: Verify images exist
        run: |
          docker images rag-backend
          docker images rag-frontend

  # Job 3: Lint (code quality)
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Check code formatting
        run: |
          pip install ruff
          ruff check backend/ frontend/
```

---

## Push and Watch

```bash
git add .github/
git commit -m "Add CI workflow"
git push origin main
```

Go to your GitHub repository and click the **Actions** tab. You’ll see your workflow running. Each job (test, docker, lint) runs in parallel on separate VMs.

Green checkmarks mean everything passed. A red X means something failed — click into the failed job to see the error logs.

---

## Writing a Simple Test for CI

Create `backend/tests/test_api.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data or "chromadb" in data

def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "document_count" in data
```

These tests verify your API endpoints respond correctly. The CI pipeline runs them on every push.

---

## What You Should See on GitHub

After pushing, the Actions tab shows three parallel jobs. Each shows step-by-step logs. On success, your commit gets a green checkmark visible in the commit history and on any PR.

`[DIAGRAM PLACEHOLDER: GitHub Actions interface showing three jobs (test, docker, lint) with green checkmarks, plus the commit view showing the CI status badge]`