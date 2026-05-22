# Containerizing Your RAG Application — Guided Example

**Module 8 — RAG Intro & Docker Deployment**

`[VIDEO PLACEHOLDER: 12 min — "The Complete Containerized RAG App: build and run the full three-service stack. Show Streamlit calling FastAPI calling Ollama, all in Docker. Demo the one-command startup."]`

Let’s build the complete containerized RAG application. This guided example provides the full `docker-compose.yml` and both Dockerfiles.

---

## The Complete `docker-compose.yml`

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - ollama
    volumes:
      - chroma_data:/app/chroma_data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://backend:8000
    depends_on:
      - backend

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  chroma_data:
  ollama_data:
```

---

## Frontend `app.py` (Streamlit)

```python
import streamlit as st
import requests
import os

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="RAG Assistant", page_icon="🤖", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("🤖 RAG Assistant")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3).json()
        st.success(f"API: Connected")
        st.write(f"Ollama: {health.get('ollama', 'unknown')}")
        st.metric("Documents", health.get('documents', 0))
    except:
        st.error("API not available")

    if st.button("🔄 Re-index Documents"):
        try:
            r = requests.post(f"{API_URL}/ingest")
            st.success(r.json().get("message", "Done"))
            st.rerun()
        except:
            st.error("Ingestion failed")

# --- Chat Interface ---
st.title("Ask Your Documents")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.caption(f"{s['source']} (distance: {s['distance']:.3f})")

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = requests.post(f"{API_URL}/ask", json={"question": prompt})
                data = r.json()
                st.write(data["answer"])

                sources = data.get("sources", [])
                if sources:
                    with st.expander(f"Sources ({data.get('confidence', 'unknown')} confidence)"):
                        for s in sources:
                            st.caption(f"{s['source']} (dist: {s['distance']:.3f})")
                            st.write(s['text'][:200] + "...")

                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": sources
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")
```

---

## Running the Full Stack

```bash
# Build and start everything
docker-compose up --build

# In another terminal, pull the Ollama model (first time only)
docker-compose exec ollama ollama pull llama3.2:1b
```

Visit `http://localhost:8501` — your Streamlit RAG chatbot, running entirely in Docker.

1. Click "Re-index Documents" to load your docs
2. Ask a question — see the answer with source citations
3. Check the sidebar for health status and document count

This is your module project’s foundation. The next steps are polishing the UI, adding more documents, and writing a README.

`[DIAGRAM PLACEHOLDER: Screenshot of the running RAG chatbot in Streamlit showing a question, answer with citations, and sidebar with health status]`