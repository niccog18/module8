"""
Backend: Settings  (Solution)
===============================
Reads all config from environment variables. Docker Compose injects these
via the `environment:` block in docker-compose.yml.
"""

import os


class Settings:
    def __init__(self):
        self.ollama_url           = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        self.model_name           = os.environ.get("MODEL_NAME", "llama3.2:1b")
        self.chroma_path          = os.environ.get("CHROMA_PATH", "./rag_db")
        self.max_results          = int(os.environ.get("MAX_RESULTS", "3"))
        self.confidence_threshold = float(os.environ.get("CONFIDENCE_THRESHOLD", "1.0"))
        self.debug                = os.environ.get("DEBUG", "false").lower() == "true"

    def __repr__(self) -> str:
        return (
            f"Settings(ollama_url={self.ollama_url!r}, model={self.model_name!r}, "
            f"chroma_path={self.chroma_path!r}, max_results={self.max_results}, "
            f"threshold={self.confidence_threshold}, debug={self.debug})"
        )


settings = Settings()
