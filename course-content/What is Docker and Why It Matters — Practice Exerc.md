# What is Docker and Why It Matters — Practice Exercise

## Docker First Steps

**Objective:** Get comfortable with Docker commands by running, inspecting, and managing containers.

**Time:** 25 minutes

**Prerequisites:** Docker installed and running.

**What you’ll do:**

1. Run the `hello-world` container and verify Docker is working
2. Run a Python container interactively (`docker run -it python:3.11-slim bash`) and:
    - Check the Python version
    - Try installing a package (`pip install requests`)
    - Exit the container
3. Run the FastAPI example from the Guided Example:
    - Create the `app.py` and `Dockerfile`
    - Build the image with `docker build -t my-first-api .`
    - Run the container with `docker run -p 8000:8000 my-first-api`
    - Visit `http://localhost:8000` in your browser to verify
4. Practice management commands:
    - `docker ps` to see running containers
    - `docker ps -a` to see all containers (including stopped)
    - `docker images` to see downloaded images
    - `docker stop <id>` to stop a running container
    - `docker rm <id>` to remove a stopped container
5. Write down the answers to these questions:
    - What happens when you `docker run` the same image twice?
    - What happens to files created inside a container when it stops?
    - How is the `-p` flag used to map ports?

**Deliverable:** A running Docker container serving a FastAPI app, plus written answers to the three questions.

**Why this exercise?** Docker fluency is essential for the module project. Getting comfortable with basic commands now means you can focus on Dockerfiles and Compose in the next lessons.