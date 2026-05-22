# Dockerfile Creation — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** Why should you copy `requirements.txt` and run `pip install` BEFORE copying your application code in a Dockerfile?

- A) It’s required by Docker
- B) It leverages layer caching: since requirements change rarely, Docker can skip the pip install step on rebuilds when only your code changes
- C) It makes the image smaller
- D) It installs packages faster

> **Answer: B** — Docker caches each layer. If `requirements.txt` hasn’t changed, the `RUN pip install` layer is reused from cache. If you `COPY . .` first, any code change invalidates the cache for every subsequent layer, forcing a full reinstall of all packages on every build. Proper ordering can save minutes per build.
> 

---

**Question 2:** Why must your FastAPI app bind to `0.0.0.0` instead of `127.0.0.1` when running in Docker?

- A) `0.0.0.0` is faster
- B) `127.0.0.1` only accepts connections from inside the container; `0.0.0.0` accepts connections from outside (including your host machine via port mapping)
- C) Docker doesn’t support `127.0.0.1`
- D) `0.0.0.0` uses a different protocol

> **Answer: B** — `127.0.0.1` ([localhost](http://localhost)) means "only accept connections from this machine." Inside a container, that means only from within the container itself. Since your browser and Streamlit frontend are on the host machine (outside the container), they can’t reach it. `0.0.0.0` means "accept connections from any network interface," including the Docker network that connects to your host.
> 

---

**Question 3:** What does the `.dockerignore` file do?

- A) Tells Docker which containers to ignore
- B) Lists files and directories that should NOT be copied into the image during `COPY`, keeping the image smaller and excluding sensitive files
- C) Prevents Docker from running certain commands
- D) Ignores errors during the build

> **Answer: B** — Like `.gitignore` for Git, `.dockerignore` tells Docker which files to exclude from the build context. This prevents copying `venv/` (hundreds of MB), `__pycache__/`, `.env` (API keys), and `chroma_data/` (database files) into the image. This makes builds faster and images smaller.
>