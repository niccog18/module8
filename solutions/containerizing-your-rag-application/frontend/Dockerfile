# frontend/Dockerfile  (Solution)
# =================================
# Build context: ./frontend
#
# Key points:
#   - --server.address=0.0.0.0 is REQUIRED to reach Streamlit from outside
#     the container (same reason as uvicorn --host 0.0.0.0)
#   - --server.fileWatcherType=none disables the file watcher (not needed
#     in production and can cause issues in some container environments)

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
  "--server.port=8501", \
  "--server.address=0.0.0.0", \
  "--server.fileWatcherType=none"]
