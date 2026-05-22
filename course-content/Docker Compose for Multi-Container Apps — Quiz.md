# Docker Compose for Multi-Container Apps — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** Inside a Docker Compose network, how does the backend container reach the Ollama container?

- A) Using `http://localhost:11434`
- B) Using the service name as a hostname: `http://ollama:11434`
- C) Using the container’s IP address (which changes every time)
- D) Docker Compose services can’t communicate with each other

> **Answer: B** — Docker Compose creates an internal network where service names act as DNS hostnames. `http://ollama:11434` resolves to the Ollama container’s internal IP. `localhost` inside a container refers to that container itself, NOT other services. This is the most common Docker Compose networking mistake.
> 

---

**Question 2:** What do Docker volumes do in a Compose setup?

- A) They make containers run faster
- B) They persist data across container stops and restarts — without volumes, data inside a container is lost when the container is removed
- C) They control network traffic volume
- D) They limit disk space usage

> **Answer: B** — Volumes mount persistent storage into containers. Your ChromaDB data and Ollama model files live in named volumes. When you `docker-compose down` and `docker-compose up` again, the volume data is still there. Without volumes, every restart would lose your ingested documents and require re-downloading LLM models.
> 

---

**Question 3:** What does `docker-compose up --build` do?

- A) Only builds images without running them
- B) Rebuilds all images from their Dockerfiles and then starts all services
- C) Starts services without rebuilding (uses cached images)
- D) Deletes all volumes and starts fresh

> **Answer: B** — The `--build` flag forces Docker Compose to rebuild images before starting. Without it, Compose uses cached images (which is faster but won’t reflect code changes). Use `--build` after changing your code or Dockerfile. Use plain `docker-compose up` when nothing has changed and you just want to start services.
>