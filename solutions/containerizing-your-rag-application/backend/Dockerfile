# backend/Dockerfile  (Solution)
# =================================
# Build context: ./backend
#
# Key points:
#   - requirements.txt copied BEFORE source code for layer caching
#   - CMD binds to 0.0.0.0 so the port is accessible outside the container

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
