# CI/CD Basics with GitHub Actions

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 25 minutes

## Objective

Add a GitHub Actions CI workflow to your RAG project that runs tests and verifies Docker builds on every push.

## What You'll Build

- **`.github/workflows/ci.yml`** — CI pipeline with three jobs
- **`backend/tests/test_api.py`** — 3 FastAPI tests that run in CI

## Workflow Requirements

Trigger on: pushes to `main` and pull requests to `main`

**Job 1 — `test`:** Set up Python 3.11, install dependencies, run pytest

**Job 2 — `docker`:** Build backend and frontend images, verify they exist

**Job 3 — `lint`:** Install ruff, check `backend/` and `frontend/`

## Test Requirements

Write at least 3 tests in `backend/tests/test_api.py`:

1. `test_root` — `GET /` returns 200
2. `test_health` — `GET /health` returns 200 with expected fields
3. `test_stats` — `GET /stats` returns 200 with a `document_count` field

## Reference Code

Starter files are provided with TODOs.

## Running Locally

```bash
cd backend
pip install pytest httpx
pytest tests/ -v
```

## Pushing to GitHub

```bash
git add .github/ backend/tests/
git commit -m "Add CI workflow and API tests"
git push origin main
```

Then check the **Actions** tab in your GitHub repository.

## Deliverable

A working CI pipeline visible in the GitHub Actions tab with green checkmarks on all three jobs.
