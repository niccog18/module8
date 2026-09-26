from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "RAG API running in Docker"


def test_stats():
    response = client.get("/stats")

    assert response.status_code == 200
    assert "document_count" in response.json()


def test_ask_empty_question():
    response = client.post("/ask", json={"question": ""})

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Please provide a question."
    assert data["sources"] == []
    assert data["confidence"] == "low"
    assert data["chunks_retrieved"] == 0