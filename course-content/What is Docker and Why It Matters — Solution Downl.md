# What is Docker and Why It Matters — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/docker-first-steps/`

Compare your answers to the reference:

- **Running twice:** Each `docker run` creates a NEW container from the same image. They’re independent instances.
- **Files in stopped containers:** Files created inside a container exist in that container’s filesystem. If the container is removed, the files are gone. To persist data, use Docker volumes (covered in Lesson 9).
- **Port mapping (-p):** `-p 8000:8000` maps port 8000 on your host machine to port 8000 inside the container. `-p 3000:8000` would map host port 3000 to container port 8000.

The Dockerfile and [app.py](http://app.py) should match the Guided Example.