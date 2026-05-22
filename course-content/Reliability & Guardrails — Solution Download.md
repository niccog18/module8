# Reliability & Guardrails — Solution Download

**GitHub:** `module-08-rag-docker/solutions/exercises/guardrailed-rag/`

Compare your solution to the reference. Key things to check:

- Does the threshold filter actually prevent low-relevance chunks from reaching the LLM?
- Does the out-of-scope query return a "don’t know" response (not a hallucinated answer)?
- Are confidence levels computed correctly based on distance scores?
- Does the structured response include all four fields (answer, sources, confidence, chunks_retrieved)?

Your specific threshold values and prompt wording will differ. The important thing is that the system behaves differently for in-scope vs. out-of-scope queries.