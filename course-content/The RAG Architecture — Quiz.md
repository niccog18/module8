# The RAG Architecture — Quiz

**Module 8 — RAG Intro & Docker Deployment**

---

**Question 1:** What does RAG stand for, and what problem does it solve?

- A) Random Access Generation — it makes AI responses faster
- B) Retrieval-Augmented Generation — it grounds AI responses in actual source documents instead of relying on the model’s training data alone
- C) Recursive Algorithm Generation — it makes AI responses more creative
- D) Real-time API Gateway — it routes API requests to the correct service

> **Answer: B** — RAG combines retrieval (finding relevant documents from a knowledge base) with generation (using an LLM to produce an answer). The key benefit is grounding: instead of generating answers from memory (which can hallucinate), the model answers based on specific, verifiable source documents. This reduces hallucination, works with current data, and enables the model to work with private information.
> 

---

**Question 2:** In the RAG pipeline, what happens BETWEEN retrieving documents from ChromaDB and getting the LLM’s response?

- A) The documents are fine-tuned into the model
- B) The retrieved documents are combined with a system prompt and the user’s question into a single prompt that is sent to the LLM
- C) The documents are deleted from ChromaDB
- D) The documents are sent directly to the user

> **Answer: B** — The prompt assembly step is critical. The retrieved document chunks become the *context* in a structured prompt that tells the LLM: "Here are relevant documents. Answer the user’s question based on this context." The system prompt also includes instructions like "if the answer isn’t in the context, say you don’t know" and "cite your sources." This step is what connects retrieval to generation.
> 

---

**Question 3:** Why is RAG preferred over fine-tuning for most knowledge-base applications?

- A) RAG is always faster than fine-tuning
- B) RAG allows updating knowledge by changing documents (not retraining), supports citations to source materials, and keeps private data in your own database rather than in model weights
- C) Fine-tuning doesn’t work with modern LLMs
- D) RAG requires no computing resources

> **Answer: B** — RAG’s advantages are practical: update documents without retraining (fast iteration), provide citations showing where answers came from (verifiability), and keep sensitive data in your controlled database (privacy). Fine-tuning is better for changing the model’s style or teaching new skills, but for question-answering over documents, RAG is more flexible and maintainable.
>