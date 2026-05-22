# Running Local LLMs with Ollama — Practice Exercise

## Ollama Explorer

**Objective:** Get comfortable with Ollama by exploring model capabilities, testing different system prompts, and measuring response characteristics.

**Time:** 25 minutes

**Prerequisites:** Ollama installed and running with at least one model pulled.

**What you’ll do:**

1. Create a file called `ollama_explorer.py`
2. Write a `generate()` helper function that calls Ollama’s `/api/chat` endpoint, measures response time, and returns the response text
3. Run these **4 experiments:**

**Experiment 1: Same question, different system prompts**

- Ask "What is an API?" with three different system prompts: (a) no system prompt, (b) "Explain like I’m 5 years old," (c) "You are a senior software architect. Be technical and precise."
- Compare how the responses differ

**Experiment 2: RAG-style context grounding**

- Provide a short paragraph of context about a topic you choose
- Ask a question that CAN be answered from the context
- Ask a question that CANNOT be answered from the context
- Does the model correctly refuse the second question?

**Experiment 3: Response timing**

- Ask questions of varying length (short: 5 words, medium: 20 words, long: 50 words)
- Record and compare response times

**Experiment 4: Temperature (optional)**

- Add `"temperature": 0.1` to one request and `"temperature": 1.0` to another with the same prompt
- Compare how deterministic vs creative the responses are

**Deliverable:** A working script with 4 experiments and printed comparisons. Include brief comments noting what you observed.

**Why this exercise?** Understanding how system prompts, context, and model parameters affect responses is essential for building reliable RAG applications. These are the tuning knobs you’ll use in Lessons 3–5.