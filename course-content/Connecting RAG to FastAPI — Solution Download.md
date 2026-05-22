# Connecting RAG to FastAPI — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/rag-api/`

Compare your solution to the reference. Key things to check:

- Does `/health` correctly detect when Ollama is down?
- Does `/ask` return a structured response with answer, sources, and confidence?
- Does `/ingest` actually load documents and you can verify via `/stats`?
- Does the 503 error for Ollama work (try stopping Ollama and calling /ask)?
- Is CORS middleware configured for frontend access?

Your endpoint names, schema field names, and specific error messages may differ. The important thing is that all four endpoints work and errors are handled gracefully.