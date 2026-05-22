# Building the RAG Pipeline — Practice Exercise

## Your RAG Pipeline

**Objective:** Build a working RAG pipeline over your own document collection, establishing the foundation for the module project.

**Time:** 40 minutes

**What you’ll do:**

1. Create a `docs/` folder with at least **6 text files** about topics you’ve learned (or any domain you’re interested in)
2. Build a `my_rag.py` that implements the complete pipeline:
    - **Ingest:** Load documents, chunk by paragraphs, store in persistent ChromaDB
    - **Retrieve:** Query ChromaDB with a user question, return top 3 chunks
    - **Generate:** Build a RAG prompt with retrieved context + system instructions, call Ollama, return the response
3. Include these features:
    - Source citation instructions in the system prompt
    - Display which chunks were retrieved before showing the answer
    - Handle the case where Ollama isn’t running (graceful error message)
    - An interactive loop (keep asking until the user types "quit")
4. Test with at least **3 questions:**
    - One that should be answerable from your documents
    - One that’s related but not directly in the documents
    - One that’s completely outside the scope

**Deliverable:** A working `my_rag.py` with documents, ChromaDB storage, Ollama generation, and test results showing all 3 query types.

**Why this exercise?** This is 80% of the module project. Getting a working RAG pipeline now means the project is mostly about adding Streamlit + FastAPI + Docker on top.