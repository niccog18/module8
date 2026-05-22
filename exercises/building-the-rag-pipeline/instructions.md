# Building the RAG Pipeline

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 40 minutes

## Objective

Build a complete, working RAG pipeline over your own document collection — this is the foundation for the module project.

## What You'll Build

A `my_rag.py` that implements the full pipeline:

- **Ingest:** Load `.txt` and `.md` files from a `docs/` folder, chunk by paragraph, and store in a persistent ChromaDB collection
- **Retrieve:** Query ChromaDB with a user question, return the top 3 chunks
- **Generate:** Build a RAG prompt (context + system instructions) and call Ollama

**Also required:**

- Source citation instructions in the system prompt
- Display which chunks were retrieved before showing the answer
- Graceful error message when Ollama isn't running
- An interactive loop (keep asking until the user types `quit`)

## Reference Code

The starter file (`my_rag.py`) provides a scaffold with TODOs — fill in each section.

## Setup

1. Create a `docs/` folder alongside `my_rag.py`
2. Add at least **6 text files** on topics you've learned (or any domain you like)
3. Make sure Ollama is running: `ollama serve`

## Running

```bash
python my_rag.py
```

## Testing

Try at least 3 questions:

1. One that should be answerable from your documents
2. One that's related but not directly in the documents
3. One that's completely outside the scope

## Deliverable

A working `my_rag.py` with a `docs/` folder, ChromaDB persistence, Ollama generation, and tested against all 3 query types.
