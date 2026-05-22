# Reliability & Guardrails — Practice Exercise

## Guardrailed RAG Pipeline

**Objective:** Add reliability features to your RAG pipeline from Lesson 3, making it production-ready.

**Time:** 30 minutes

**What you’ll do:**

1. Start with your `my_rag.py` from Lesson 3 (or copy the Guided Example’s `rag_pipeline.py`)
2. Add these **4 guardrails:**

**Guardrail 1: Distance threshold filtering**

- Only send chunks with distance below a configurable threshold (start with 1.0)
- If no chunks pass the filter, return a "no relevant information" response

**Guardrail 2: Confidence levels**

- Return a confidence level with each response: "high" (best distance < 0.5), "medium" (< 1.0), "low" (>= 1.0)

**Guardrail 3: Strengthened system prompt**

- Add explicit guardrail instructions: never make up information, say "I don’t know" when unsure, always cite sources

**Guardrail 4: Structured response**

- Return responses as a dictionary with: `answer`, `sources`, `confidence`, `chunks_retrieved`
1. Test with **4 queries:** one in-scope, one partially in-scope, one out-of-scope, and one ambiguous
2. Print the structured response for each query

**Deliverable:** An enhanced RAG pipeline with confidence thresholds, structured responses, and tested against all four query types.

**Why this exercise?** These guardrails are required for the module project. Building them now means your Containerized RAG Assistant will be reliable from the start.