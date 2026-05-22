# Environment Management & Configuration — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** Why should you use environment variables instead of hardcoded values for configuration like the Ollama URL?

- A) Environment variables are faster than strings
- B) The same Docker image can run in different environments (dev, staging, production) just by changing the environment variables, without rebuilding
- C) Python can’t read hardcoded strings
- D) Docker requires all configuration to be in environment variables

> **Answer: B** — Separating configuration from code means one image works everywhere. In development, `OLLAMA_URL=http://localhost:11434`. In Docker Compose, `OLLAMA_URL=http://ollama:11434`. In production, maybe `OLLAMA_URL=http://gpu-server:11434`. Same code, different configuration.
> 

---

**Question 2:** Why should `.env` files be added to `.gitignore`?

- A) They are too large for Git
- B) They often contain secrets (API keys, passwords) that should never be in version control where anyone with repo access can see them
- C) Git doesn’t support `.env` files
- D) They slow down Git operations

> **Answer: B** — `.env` files frequently contain sensitive information: API keys, database passwords, secret keys. Committing these to Git means anyone with access to the repository (including public repos) can see your secrets. Create a `.env.example` (without real values) that IS committed, showing developers which variables they need to set.
>