# What is Docker and Why It Matters — Concept

**Module 8 — RAG Intro & Docker Deployment**

**Estimated time: 35 minutes**

---

### Learning Objectives

By the end of this lesson, you will be able to:

1. Explain what Docker is and the problem it solves ("works on my machine")
2. Distinguish between images, containers, and registries
3. Describe the relationship between a Dockerfile, an image, and a running container
4. Explain why Docker is essential for deploying AI applications

---

`[VIDEO PLACEHOLDER: 6 min — "What is Docker? Analogy: shipping containers. 'Your code works on your machine. Docker makes it work on every machine.' Show the problem Docker solves with a real before/after example."]`

Imagine you build an amazing RAG application on your laptop. It uses Python 3.11, ChromaDB, sentence-transformers, Ollama, FastAPI, and Streamlit. Your instructor asks you to demo it. You send them the code. They try to run it and get:

```
ModuleNotFoundError: No module named 'chromadb'
ERROR: Could not find a version that satisfies the requirement sentence-transformers
OSError: libgomp.so.1: cannot open shared object file
```

They’re on a different operating system. They have a different Python version. They’re missing system libraries. They have conflicting package versions. Your code is correct — the environment is wrong.

This is the "**it works on my machine**" problem. It’s been plaguing software development for decades. Docker solves it.

---

## Docker: The Shipping Container Analogy

Before standardized shipping containers, goods were loaded onto ships in bags, barrels, crates, and loose piles. Every port had different equipment, different workers, different methods. Transferring cargo between ships, trains, and trucks was chaotic and error-prone.

Then someone invented the standardized shipping container: a metal box with uniform dimensions. Now everything fits inside the same box, every crane lifts the same box, every truck carries the same box. It doesn’t matter what’s inside — the container is the standard.

Docker does the same thing for software. Your application goes inside a **container** with everything it needs: the operating system, Python, all libraries, all configurations. The container runs identically on your laptop, your teammate’s laptop, a CI server, or a cloud deployment. The machine running the container doesn’t need Python installed, doesn’t need ChromaDB installed, doesn’t need anything except Docker.

---

## Key Concepts

**Dockerfile:** A text file with step-by-step instructions for building an image. Think of it as a recipe.

**Image:** A snapshot built from a Dockerfile. It contains your code, dependencies, and configuration, frozen at a point in time. Think of it as a class definition.

**Container:** A running instance of an image. It has its own processes, network, and filesystem. Think of it as an object (instance of a class). You can run multiple containers from the same image.

**Registry:** A storage service for images (like GitHub for code). Docker Hub is the default public registry. You push images to a registry and pull them to any machine.

`[DIAGRAM PLACEHOLDER: Flow diagram showing: Dockerfile (recipe) → docker build → Image (snapshot) → docker run → Container (running instance). With a note: "One image can create many containers"]`

---

## The Docker Workflow

```bash
# 1. Write a Dockerfile (the recipe)
# 2. Build an image from it
docker build -t my-rag-app .

# 3. Run a container from the image
docker run -p 8000:8000 my-rag-app

# 4. Share the image (optional)
docker push my-rag-app
```

That’s it. Anyone with Docker can `docker pull` your image and `docker run` it. No Python installation, no dependency management, no environment configuration. It just works.

---

## Why Docker Matters for AI Applications

AI applications have the most complex dependency chains in software. Your RAG app needs: a specific Python version, NumPy, PyTorch (for sentence-transformers), ChromaDB (with its C++ dependencies), FastAPI + Uvicorn, Streamlit, and system libraries like `libgomp` for parallel processing.

Installing all of this correctly on three different operating systems is a nightmare. Docker makes it a single `docker build` command.

Docker also enables:

- **Reproducibility:** The exact same environment for development, testing, and production
- **Isolation:** Your app’s dependencies can’t conflict with other apps on the same machine
- **Scalability:** Run multiple instances of your app easily
- **CI/CD:** Automated testing and deployment in consistent environments

---

## Docker vs. Virtual Environments

You might wonder: "I already use `venv` for Python. How is Docker different?"

Virtual environments isolate Python packages. Docker isolates **everything**: the operating system, system libraries, Python itself, configuration files, and your application code. A venv can’t help when someone is on Windows and your app needs a Linux-specific library. Docker can.