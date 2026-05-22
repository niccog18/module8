# Environment Management & Configuration — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 7 min — "Environment Configuration: show the same image running with different settings by changing .env values. Demonstrate switching between models, toggling debug mode, and managing API keys safely."]`

Let’s build a properly configured RAG app that reads all settings from environment variables.

Create `config.py` in your backend directory:

```python
import os

class Settings:
    """Application settings loaded from environment variables."""

    # Ollama configuration
    OLLAMA_URL: str = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    MODEL_NAME: str = os.environ.get("MODEL_NAME", "llama3.2:1b")

    # ChromaDB configuration
    CHROMA_PATH: str = os.environ.get("CHROMA_PATH", "./chroma_data")
    COLLECTION_NAME: str = os.environ.get("COLLECTION_NAME", "documents")

    # RAG configuration
    MAX_RESULTS: int = int(os.environ.get("MAX_RESULTS", "3"))
    CONFIDENCE_THRESHOLD: float = float(os.environ.get("CONFIDENCE_THRESHOLD", "1.2"))

    # Application settings
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"
    DOCS_DIRECTORY: str = os.environ.get("DOCS_DIRECTORY", "./docs")

    # Optional cloud API key (for OpenAI fallback)
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")

settings = Settings()

# Print configuration on startup (useful for debugging)
if settings.DEBUG:
    print("=== Configuration ===")
    print(f"  Ollama URL: {settings.OLLAMA_URL}")
    print(f"  Model: {settings.MODEL_NAME}")
    print(f"  ChromaDB: {settings.CHROMA_PATH}")
    print(f"  Max Results: {settings.MAX_RESULTS}")
    print(f"  Threshold: {settings.CONFIDENCE_THRESHOLD}")
    print(f"  Debug: {settings.DEBUG}")
    print(f"  OpenAI key: {'set' if settings.OPENAI_API_KEY else 'not set'}")
```

Use it in your app:

```python
from config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
collection = client.get_or_create_collection(settings.COLLECTION_NAME)
```

**`.env`:**

```bash
OLLAMA_URL=http://ollama:11434
MODEL_NAME=llama3.2:1b
CHROMA_PATH=/app/chroma_data
MAX_RESULTS=5
CONFIDENCE_THRESHOLD=1.0
DEBUG=true
DOCS_DIRECTORY=/app/docs
```

**`docker-compose.yml` update:**

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - ollama
    volumes:
      - chroma_data:/app/chroma_data
```

Now you can change any setting by editing `.env` and restarting — no image rebuild needed.

`[DIAGRAM PLACEHOLDER: Diagram showing the .env file feeding environment variables into docker-compose.yml, which passes them to the container, where config.py reads them with os.environ.get()]`