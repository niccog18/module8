# Running Local LLMs with Ollama — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/ollama-explorer/`

Compare your solution to the reference. Key things to check:

- Does your generate function measure and report response time?
- Do different system prompts produce visibly different responses for the same question?
- Does the RAG-grounded experiment show the model staying within context (or attempting to)?
- Did you handle the case where Ollama isn’t running with a clear error message?

Your specific questions, observations, and timing results will differ. The key insight: system prompts dramatically change model behavior, and smaller models may not reliably refuse out-of-context questions (which is why guardrails exist).