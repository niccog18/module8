# What is Docker and Why It Matters — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 8 min — "Docker First Steps: install Docker, run hello-world, pull and run a Python image, explore docker ps and docker images. Build intuition for images and containers."]`

Let’s install Docker and run your first containers.

---

## Step 1: Install Docker

**macOS:** Download Docker Desktop from [docker.com](http://docker.com)

**Windows:** Download Docker Desktop. WSL 2 backend is recommended.

**Linux:**

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER  # Run Docker without sudo
```

`[VERIFY: Docker installation methods may change. Students should check docker.com for latest instructions.]`

Verify the installation:

```bash
docker --version
# Should print something like: Docker version 24.x.x

docker run hello-world
# Should print: Hello from Docker!
```

---

## Step 2: Run a Python Container

Let’s run Python inside a container:

```bash
# Pull the official Python image and start an interactive shell
docker run -it python:3.11-slim python
```

You’re now inside a Python REPL running in a container. The container has its own filesystem, its own Python installation, and its own process space. Try:

```python
import sys
print(sys.version)  # 3.11.x, regardless of what's on your host
print("Hello from inside a container!")
exit()
```

When you exit, the container stops. Your host system’s Python is completely unaffected.

---

## Step 3: Explore Docker Commands

```bash
# List running containers
docker ps

# List ALL containers (including stopped ones)
docker ps -a

# List downloaded images
docker images

# Remove a stopped container
docker rm <container_id>

# Remove an image
docker rmi <image_name>
```

---

## Step 4: Run a FastAPI App in Docker (Preview)

Let’s see what a containerized FastAPI app looks like. Create a simple `app.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Docker!", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

And a `Dockerfile`:

```docker
FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY app.py .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t my-fastapi .
docker run -p 8000:8000 my-fastapi
```

Visit `http://localhost:8000` — you’ll see `{"message": "Hello from Docker!"}`. Your FastAPI app is running inside a container, accessible from your browser. The `-p 8000:8000` flag maps port 8000 inside the container to port 8000 on your machine.

Stop it with `Ctrl+C` or `docker stop <container_id>`.

In the next lesson, you’ll learn how to write proper Dockerfiles for more complex applications.

`[DIAGRAM PLACEHOLDER: Terminal screenshot showing docker build, docker run, and the browser showing the FastAPI response from inside the container]`