# The RAG Architecture — Practice Exercise

## RAG Pipeline Diagram & Prompt Assembly

**Objective:** Reinforce your understanding of the RAG architecture by diagramming it and building the prompt assembly step.

**Time:** 25 minutes

**What you’ll do:**

**Part 1: Architecture Diagram (10 min)**

Draw (on paper, in a drawing tool, or in markdown) a complete RAG pipeline diagram showing all 5 stages:

1. User question input
2. Query embedding
3. Vector database retrieval
4. Prompt assembly (system prompt + context + question)
5. LLM generation + response

Label each stage with: what happens, which technology from this course handles it, and what data flows between stages.

**Part 2: Prompt Builder (15 min)**

Create a file called `prompt_builder.py` that:

1. Takes a user question and a list of retrieved document chunks (simulated)
2. Assembles a complete RAG prompt with:
    - A system prompt instructing the model to answer from context only
    - The retrieved chunks formatted with source labels
    - The user’s question
    - Instructions to cite sources
3. Prints the assembled prompt and its token count estimate (characters / 4 as a rough approximation)
4. Tests with at least 2 different questions and different sets of "retrieved" chunks

**Deliverable:** An architecture diagram (photo, screenshot, or markdown) and a working `prompt_builder.py` that demonstrates the prompt assembly step.

**Why this exercise?** The prompt assembly step is where most RAG quality issues live. A poorly assembled prompt produces bad answers even with perfect retrieval. Building this function now means you have a reusable component for the full pipeline in Lesson 3.