# Building the RAG Pipeline — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/rag-pipeline/`

Compare your solution to the reference. Key things to check:

- Does ingestion use persistent ChromaDB (data survives restarts)?
- Does the system prompt instruct the model to answer from context only and cite sources?
- Are retrieved chunks displayed with distance scores before the answer?
- Does the out-of-scope question produce a "don’t know" response (or at least a weaker response)?
- Is there graceful error handling for when Ollama isn’t running?

Your documents, questions, and specific answers will differ. The pipeline structure (ingest → retrieve → build prompt → generate) should match.