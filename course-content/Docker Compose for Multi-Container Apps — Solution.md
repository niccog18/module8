# Docker Compose for Multi-Container Apps — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/compose-multi-service/`

Compare your solution to the reference. Key things to check:

- Does `OLLAMA_URL` use the service name (`http://ollama:11434`), not `localhost`?
- Are named volumes defined for both ChromaDB and Ollama data?
- Does `depends_on` specify the correct startup order?
- Does `/health` show `ollama: connected` when both services are running?
- Does data persist across `docker-compose down` and `docker-compose up`?

Your app code and specific port choices may differ. The critical pattern is: environment-variable-based URLs + named volumes + service networking.