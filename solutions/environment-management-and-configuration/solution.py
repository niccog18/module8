"""
L6 — Environment Management & Configuration  (Solution)
=========================================================
Run with:
    python solution.py        # prints current settings

Key concepts:
    Why centralise config?
        Without a Settings class, environment variable reads are scattered across
        every file. When you need to rename OLLAMA_URL to OLLAMA_HOST you'd have
        to find and change every os.environ.get() call. A single Settings class
        means one change, everywhere updated.

    Module-level singleton:
        `settings = Settings()` runs once at import time. All other modules do
        `from config import settings` and get the same object. No repeated env
        reads, no inconsistency.

    .env vs .env.example:
        .env          → real values, never committed (add to .gitignore)
        .env.example  → documented template with placeholder values, committed
        Docker Compose reads .env automatically with `env_file: .env`.

    Type coercion is intentional:
        os.environ returns strings. Failing to cast means you'd compare
        "3" == 3 (False) or try to pass "false" to a boolean branch.

    Fail loudly for secrets:
        For a real API key you'd write:
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise ValueError("OPENAI_API_KEY must be set")
        Never silently default a secret to an empty string.
"""

import os


class Settings:
    """
    Central configuration. All values read from environment variables.
    Import with: from config import settings
    """

    def __init__(self):
        self.ollama_url          = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        self.model_name          = os.environ.get("MODEL_NAME", "llama3.2:1b")
        self.chroma_path         = os.environ.get("CHROMA_PATH", "./rag_db")
        self.max_results         = int(os.environ.get("MAX_RESULTS", "3"))
        self.confidence_threshold = float(os.environ.get("CONFIDENCE_THRESHOLD", "1.0"))
        self.debug               = os.environ.get("DEBUG", "false").lower() == "true"

    def __repr__(self) -> str:
        return (
            f"Settings(\n"
            f"  ollama_url           = {self.ollama_url!r}\n"
            f"  model_name           = {self.model_name!r}\n"
            f"  chroma_path          = {self.chroma_path!r}\n"
            f"  max_results          = {self.max_results}\n"
            f"  confidence_threshold = {self.confidence_threshold}\n"
            f"  debug                = {self.debug}\n"
            f")"
        )


# Module-level singleton — import this everywhere
settings = Settings()


if __name__ == "__main__":
    print(settings)
    print()
    print("Usage in other modules:")
    print("  from config import settings")
    print(f"  # settings.ollama_url → {settings.ollama_url!r}")
    print(f"  # settings.model_name → {settings.model_name!r}")
