# Containerizing Your RAG Application — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/full-rag-stack/`

Compare your solution to the reference. Key things to check:

- Does `docker-compose up --build` start all three services without errors?
- Can you reach Streamlit at `localhost:8501` and FastAPI at `localhost:8000/docs`?
- Does the Streamlit frontend successfully call the FastAPI backend (check the /health endpoint)?
- Does asking a question return an answer with source citations?
- Do volumes persist data across `docker-compose down` and `docker-compose up`?

Your specific UI, endpoints, and documents will differ. The critical check: one command starts everything, and the user can ask questions and get grounded answers.