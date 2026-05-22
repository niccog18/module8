# Containerizing Your RAG Application — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** In the complete RAG Docker Compose setup, how does the Streamlit frontend communicate with the FastAPI backend?

- A) Through `http://localhost:8000` — both are on the same machine
- B) Through `http://backend:8000` — using the Docker Compose service name as the hostname
- C) Through a shared database
- D) Through file system access

> **Answer: B** — Inside the Docker Compose network, services use their service names as hostnames. The Streamlit container reaches the FastAPI container at `http://backend:8000`. `localhost` inside the Streamlit container refers to the Streamlit container itself, not the host machine or other containers.
> 

---

**Question 2:** After `docker-compose up`, you need to pull an Ollama model. What command pulls the model inside the running Ollama container?

- A) `ollama pull llama3.2:1b`
- B) `docker-compose exec ollama ollama pull llama3.2:1b`
- C) `docker pull ollama/llama3.2:1b`
- D) The model downloads automatically

> **Answer: B** — `docker-compose exec` runs a command inside a running container. `docker-compose exec ollama` targets the Ollama service, then `ollama pull llama3.2:1b` runs inside that container. The model files are saved to the Ollama volume, persisting across restarts.
> 

---

**Question 3:** Why does the Streamlit Dockerfile use `--server.address 0.0.0.0` in the CMD?

- A) It’s the default Streamlit setting
- B) It makes the Streamlit app accessible from outside the container, just like FastAPI needs `--host 0.0.0.0`
- C) It runs Streamlit faster
- D) It’s required by Docker

> **Answer: B** — By default, Streamlit listens on `localhost` (127.0.0.1), which is only accessible from inside the container. Setting `--server.address 0.0.0.0` makes it accessible from the Docker host (your browser). This is the same principle as FastAPI needing `--host 0.0.0.0`.
>