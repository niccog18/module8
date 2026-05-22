# Building the RAG Pipeline — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** In the RAG pipeline, what is the purpose of the system prompt that accompanies the retrieved context?

- A) To make the model respond faster
- B) To instruct the model on how to use the context — answer from it only, cite sources, and admit when information is insufficient
- C) To embed the query into a vector
- D) To compress the context for efficiency

> **Answer: B** — The system prompt is the instruction layer. Without it, the model might ignore the context and answer from training data (hallucinate), or fail to cite sources. A good RAG system prompt says: "Answer from the context only, cite your sources, and say you don’t know if the answer isn’t there." This is where prompt engineering (Module 7, Lesson 6) meets the RAG pipeline.
> 

---

**Question 2:** Why is streaming important for RAG applications?

- A) It makes the model smarter
- B) It reduces the total response time
- C) It shows tokens as they’re generated, so users see progress instead of waiting 5–30 seconds for the complete response
- D) It’s required by Ollama

> **Answer: C** — The total generation time is roughly the same whether you stream or not. But streaming shows the first token within 1–2 seconds, while non-streaming shows nothing until the entire response is complete. For a 200-word answer that takes 15 seconds to generate, streaming means the user starts reading immediately instead of staring at a blank screen.
> 

---

**Question 3:** If your RAG pipeline returns a poor answer, which two factors should you investigate first?

- A) The model’s training data and the internet speed
- B) The retrieval quality (did ChromaDB find the right documents?) and the prompt quality (did the system prompt properly instruct the model?)
- C) The color scheme of the Streamlit interface
- D) The Python version and the operating system

> **Answer: B** — RAG quality depends on two things: retrieval and prompt. If ChromaDB returned irrelevant chunks, the model has no useful context to work with (bad in, bad out). If ChromaDB returned the right chunks but the prompt didn’t properly instruct the model, the answer might ignore the context or fail to cite sources. Always debug retrieval first, then prompt.
>