# Dockerfile Creation — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/dockerfile-creation/`

Compare your solution to the reference. Key things to check:

- Is `requirements.txt` copied and installed BEFORE your application code?
- Does `CMD` use `--host 0.0.0.0`?
- Does `.dockerignore` exclude `venv`, `__pycache__`, and `.env`?
- Can you access `/docs` in the browser when the container runs?
- Does rebuilding after a code-only change show `CACHED` for the pip install step?

Your specific requirements and app structure may differ. The important patterns are: slim base image, requirements-first ordering, and 0.0.0.0 binding.