# Environment Management & Configuration — Practice Exercise

## Configurable RAG Application

**Objective:** Refactor your RAG application to read all configuration from environment variables, with a centralized Settings class and proper `.env` management.

**Time:** 25 minutes

**What you’ll do:**

1. Create a `config.py` with a `Settings` class that reads from environment variables with sensible defaults
2. Include at least these settings: `OLLAMA_URL`, `MODEL_NAME`, `CHROMA_PATH`, `MAX_RESULTS`, `CONFIDENCE_THRESHOLD`, `DEBUG`
3. Create a `.env` file with Docker Compose values
4. Create a `.env.example` (without secrets) for documentation
5. Add `.env` to both `.gitignore` and `.dockerignore`
6. Update your `docker-compose.yml` to use `env_file: .env`
7. Verify: change `MODEL_NAME` in `.env`, restart, and confirm the change takes effect

**Deliverable:** A refactored app with centralized configuration, `.env` management, and Docker Compose integration.

**Why this exercise?** Proper configuration management is required for the module project and is a fundamental production skill.