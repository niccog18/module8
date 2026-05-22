# Reliability & Guardrails — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** What is a confidence threshold in a RAG system?

- A) A limit on how many tokens the LLM can generate
- B) A minimum similarity score that retrieved chunks must meet before being sent to the LLM — filtering out loosely related or irrelevant results
- C) A time limit for how long the system waits for Ollama
- D) A measure of the user’s trust in the system

> **Answer: B** — Confidence thresholds filter retrieval results by distance/similarity score. If no chunks meet the threshold, the system returns a "don’t know" response instead of sending irrelevant context to the LLM. This is the single most effective guardrail: preventing bad context from reaching the model prevents bad answers.
> 

---

**Question 2:** Why should a RAG system return structured responses with confidence levels and source citations?

- A) It makes the API response larger
- B) It lets the frontend display answers differently based on confidence (e.g., show a warning for low-confidence answers) and lets users verify sources
- C) ChromaDB requires it
- D) It speeds up the LLM generation

> **Answer: B** — Structured responses with confidence levels allow the UI to adapt: high-confidence answers displayed normally, medium-confidence with a note, low-confidence with a clear warning. Source citations let users verify the answer against the original documents. This transparency builds user trust and catches errors.
> 

---

**Question 3:** A user asks your RAG chatbot about a topic not in your knowledge base. Without guardrails, what is the most likely failure mode?

- A) The system crashes
- B) The system returns irrelevant chunks, the LLM generates a confident-sounding answer based on loosely related context (or hallucination), and the user trusts incorrect information
- C) The system returns an empty response
- D) The system asks the user to rephrase

> **Answer: B** — Without guardrails, ChromaDB always returns *something* (the least-dissimilar chunks), even if those chunks are barely relevant. The LLM then generates an answer from this weak context, often filling gaps with hallucination. The result is confident-sounding misinformation — the most dangerous failure mode.
>