# Module 8: RAG Intro & Docker Deployment — Starter Kit

## Quick Setup

### Option A: Clone with Git

```bash
git clone <repo-url>
cd module-08-rag-intro-and-docker-deployment
```

### Option B: Download ZIP (no Git required)

1. Go to this repo on GitHub
2. Click the green **Code** button
3. Click **Download ZIP**
4. Unzip the downloaded file and open the folder

---

### Shared steps (both options)

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install and start Ollama** (required for Week 1 exercises):

   ```bash
   # Install from https://ollama.com, then:
   ollama serve
   ollama pull llama3.2:1b
   ```

4. **Install Docker Desktop** (required for Week 2 exercises):
   Download from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

5. **Start working:** Open any exercise folder and edit the starter file.

---

### Running the exercises

| Exercise type        | Command                                                          |
| -------------------- | ---------------------------------------------------------------- |
| Python script        | `python starter.py`                                              |
| FastAPI backend      | `uvicorn my_rag_api:app --reload --port 8000`                    |
| Docker image         | `docker build -t my-image . && docker run -p 8000:8000 my-image` |
| Docker Compose stack | `docker-compose up --build`                                      |

---

## Week 1 — RAG Pipeline

| #   | Exercise                 | Folder                                      | Packages / Tech                        |
| --- | ------------------------ | ------------------------------------------- | -------------------------------------- |
| L1  | Prompt Builder           | `exercises/the-rag-architecture/`           | Pure Python                            |
| L2  | Ollama Explorer          | `exercises/running-local-llms-with-ollama/` | **requests**, Ollama                   |
| L3  | Build the RAG Pipeline   | `exercises/building-the-rag-pipeline/`      | **chromadb**, **requests**             |
| L4  | Reliability & Guardrails | `exercises/reliability-and-guardrails/`     | **chromadb**, **requests**             |
| L5  | RAG FastAPI              | `exercises/connecting-rag-to-fastapi/`      | **fastapi**, **uvicorn**, **chromadb** |

> **Prerequisites for Week 1:** Ollama must be installed and running (`ollama serve`) with
> `llama3.2:1b` pulled before attempting Lessons 2–5.

---

## Week 2 — Docker & Deployment

| #   | Exercise                  | Folder                                                | Packages / Tech                            |
| --- | ------------------------- | ----------------------------------------------------- | ------------------------------------------ |
| L7  | Dockerfile Creation       | `exercises/dockerfile-creation/`                      | Docker                                     |
| L8  | Docker Compose            | `exercises/docker-compose-for-multi-container-apps/`  | Docker Compose                             |
| L9  | Environment Management    | `exercises/environment-management-and-configuration/` | **python-dotenv**                          |
| L10 | Containerize the RAG App  | `exercises/containerizing-your-rag-application/`      | Docker Compose, **fastapi**, **streamlit** |
| L11 | CI/CD with GitHub Actions | `exercises/ci-cd-basics-with-github-actions/`         | GitHub Actions, **pytest**                 |

> **Prerequisites for Week 2:** Docker Desktop must be installed and running before
> attempting any of these exercises. Complete Lesson 6 ("What is Docker?") first.

---

## Module Project

The project is a **Containerized RAG Assistant** — a full three-service application
(FastAPI backend + Streamlit frontend + Ollama) that runs with a single `docker-compose up`.

### Starter

```bash
cd project/starter
cp .env.example .env

# Build and run the full stack
docker-compose up --build
```

The starter includes:

- `backend/main.py` — FastAPI skeleton with TODO endpoint stubs
- `backend/rag.py` — RAG pipeline functions to implement
- `backend/config.py` — Settings class skeleton (reads from env vars)
- `backend/tests/test_api.py` — 3 test stubs to complete
- `backend/docs/` — Sample document corpus (add your own files)
- `frontend/app.py` — Streamlit chat UI skeleton with TODO sections
- `docker-compose.yml` — Service stubs to complete
- `.env.example` — All required environment variables documented

### Running locally (before Dockerizing)

```bash
# Backend
cd project/starter/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd project/starter/frontend
pip install -r requirements.txt
streamlit run app.py
```

See the project brief in `course-content/Module Project Containerized RAG Assistant.md` for full requirements and grading rubric.

---

## Solutions

Solutions are in the `solutions/` folder. **Try each exercise yourself first!**
Compare your approach to the reference solution after you've made your attempt.
Differences are fine — there are many valid ways to solve these problems.

---

## Need Help?

- Re-read the lesson's Concept and Guided Example sections
- Post in the course discussion board
- Bring questions to office hours
