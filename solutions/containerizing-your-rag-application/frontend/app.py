"""
Frontend: Streamlit RAG UI  (Solution)
========================================
Run locally:
    BACKEND_URL=http://localhost:8000 streamlit run app.py

Inside Docker Compose: started automatically; reads BACKEND_URL from env.

Key concepts:
    BACKEND_URL from environment:
        Inside Docker Compose, services communicate via service names.
        The frontend reaches the backend at http://backend:8000, not localhost.
        Reading from os.environ means the same code works locally and in Docker.

    Sidebar health check:
        Calling /health on every page load gives instant feedback about whether
        the stack is healthy. Students learn to add operational visibility early.

    Confidence colour coding:
        Visual cues (green/orange/red) make confidence levels immediately
        obvious without requiring the user to read a number or label carefully.

    Error handling:
        requests.exceptions.ConnectionError means the backend container isn't
        reachable. Showing a helpful message (rather than a Python traceback)
        is essential for a production-quality UI.
"""

import streamlit as st
import requests
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

CONFIDENCE_COLOURS = {"high": "green", "medium": "orange", "low": "red"}

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="RAG Assistant", page_icon="🔍", layout="centered")

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Controls")

    # Health check
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=3).json()
        chroma  = health.get("chromadb", "unknown")
        ollama  = health.get("ollama",   "unknown")
        doc_cnt = health.get("document_count", 0)
        st.success(f"Backend: connected")
        st.caption(f"ChromaDB: {chroma} | Ollama: {ollama} | Docs: {doc_cnt}")
    except requests.exceptions.ConnectionError:
        st.error("Backend: unreachable")
        st.caption(f"Expected at {BACKEND_URL}")

    st.divider()

    # Re-index button
    if st.button("Re-index Documents", use_container_width=True):
        try:
            resp = requests.post(f"{BACKEND_URL}/ingest", timeout=30).json()
            st.success(f"Ingested {resp.get('chunks_ingested', 0)} chunks")
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach backend")

# ── Main area ──────────────────────────────────────────────────────────────
st.title("RAG Assistant")
st.caption("Ask questions grounded in your documents.")

question = st.text_input("Your question", placeholder="What is ChromaDB?")

if st.button("Ask", type="primary") and question.strip():
    try:
        with st.spinner("Thinking…"):
            resp = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": question},
                timeout=60,
            )
            if resp.status_code == 422:
                st.warning("Please enter a valid question.")
            elif resp.status_code == 503:
                st.error("Ollama is not running. Start it with: ollama serve")
            else:
                data = resp.json()
                answer     = data.get("answer", "No answer returned.")
                confidence = data.get("confidence", "low")
                sources    = data.get("sources", [])

                colour = CONFIDENCE_COLOURS.get(confidence, "gray")
                st.markdown(f":{colour}[Confidence: **{confidence}**]")
                st.markdown(answer)

                if sources:
                    with st.expander(f"Sources ({len(sources)})"):
                        for src in sources:
                            st.markdown(f"**{src['source']}** (dist: {src['distance']:.3f})")
                            st.caption(src["text"][:300] + ("…" if len(src["text"]) > 300 else ""))

    except requests.exceptions.ConnectionError:
        st.error(f"Cannot reach the backend at {BACKEND_URL}. Is it running?")
