# What is Docker and Why It Matters — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** What problem does Docker solve?

- A) Docker makes Python code run faster
- B) Docker packages an application with ALL its dependencies into a standardized container that runs identically on any machine, eliminating "works on my machine" issues
- C) Docker replaces the need for programming languages
- D) Docker is only useful for web applications

> **Answer: B** — Docker solves environment inconsistency. Your application, its Python version, all libraries, system dependencies, and configuration are packaged together. A container built on macOS runs identically on Linux or Windows. This is especially valuable for AI applications with complex dependency chains.
> 

---

**Question 2:** What is the relationship between a Dockerfile, an image, and a container?

- A) They are three names for the same thing
- B) A Dockerfile is the recipe, an image is the snapshot built from it, and a container is a running instance of the image
- C) A container creates a Dockerfile which becomes an image
- D) An image is a running container that has been saved

> **Answer: B** — The flow is: Dockerfile (recipe/instructions) → `docker build` → Image (static snapshot) → `docker run` → Container (running instance). You write the Dockerfile once, build it into an image, and can create many containers from that one image.
> 

---

**Question 3:** How does Docker differ from a Python virtual environment (`venv`)?

- A) Docker only isolates Python packages; venv isolates everything
- B) Docker isolates the entire environment (OS, system libraries, Python, packages, configuration); venv only isolates Python packages
- C) They are identical in functionality
- D) Venv is more powerful than Docker

> **Answer: B** — A venv isolates Python packages from your system Python. Docker isolates *everything*: the operating system, system-level libraries (like `libgomp` for NumPy), Python itself, all packages, config files, and environment variables. When your app needs a Linux-specific library and your teammate uses Windows, venv can’t help. Docker can.
>