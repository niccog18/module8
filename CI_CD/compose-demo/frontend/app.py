import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="RAG Assistant", page_icon="🤖", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("🤖 RAG Assistant")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3).json()
        st.success("API: Connected")
        st.write(f"Ollama: {health.get('ollama', 'unknown')}")
        st.metric("Documents", health.get("documents", 0))
    except requests.RequestException:
        st.error("API not available")

    if st.button("🔄 Re-index Documents"):
        try:
            r = requests.post(f"{API_URL}/ingest")
            st.success(r.json().get("message", "Done"))
            st.rerun()
        except requests.RequestException:
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
                    st.caption(s)

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"), st.spinner("Thinking..."):
        try:
            r = requests.post(f"{API_URL}/ask", json={"question": prompt})
            data = r.json()
            st.write(data["answer"])

            sources = data.get("sources", [])
            if sources:
                with st.expander(f"Sources ({data.get('confidence', 'unknown')} confidence)"):
                    for s in sources:
                        st.caption(s)

            st.session_state["messages"].append({
                "role": "assistant",
                "content": data["answer"],
                "sources": sources
            })
        except requests.RequestException as e:
            st.error(f"Error: {e!s}")