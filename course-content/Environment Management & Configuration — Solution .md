# Environment Management & Configuration — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/env-configuration/`

Compare your solution to the reference. Key things to check:

- Does `config.py` use `os.environ.get()` with defaults for every setting?
- Is `.env` excluded from Git and Docker (`.gitignore` and `.dockerignore`)?
- Does `.env.example` exist with placeholder values?
- Does changing a value in `.env` and restarting actually affect the app behavior?
- Are settings used throughout the app via the centralized Settings class (not hardcoded)?