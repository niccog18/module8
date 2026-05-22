"""
Tests: FastAPI RAG API  (Solution)
=====================================
Run with:
    pytest tests/ -v

or, from the project root:
    pytest backend/tests/ -v

Key concepts:
    TestClient:
        FastAPI's TestClient (built on httpx) spins up the application in-process
        so tests are fast and don't require a running server.

    Override dependencies:
        In a larger test suite you'd use app.dependency_overrides to replace
        real DB/LLM clients with mocks. For these integration-style smoke tests
        we just verify the shape of the responses.

    Minimal assertions:
        Smoke tests check HTTP status codes and top-level response keys.
        They catch the most common regressions (broken routes, schema changes)
        without requiring a live Ollama instance or ChromaDB data.
"""

from fastapi.testclient import TestClient
import sys
import os

# Allow imports from parent directory when running pytest from ./backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: E402

client = TestClient(app)


def test_root():
    """GET / should return 200 with a message field."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_health():
    """GET /health should return 200 with status, chromadb, and ollama keys."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status"   in data
    assert "chromadb" in data
    assert "ollama"   in data


def test_stats():
    """GET /stats should return 200 with document_count and model keys."""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "document_count" in data
    assert "model"          in data
