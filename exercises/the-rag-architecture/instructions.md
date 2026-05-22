# The RAG Architecture — Prompt Builder

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 25 minutes

## Objective

Reinforce your understanding of the RAG architecture by building the prompt assembly step that sits at the heart of every RAG pipeline.

## What You'll Build

A `prompt_builder.py` that:

1. Accepts a user question and a list of retrieved document chunks (simulated)
2. Assembles a complete RAG prompt with a system instruction, formatted context chunks with source labels, and the user's question
3. Prints the assembled prompt and a token count estimate (characters ÷ 4)
4. Tests with at least 2 different questions and different sets of simulated chunks

## Reference Code

The starter file (`prompt_builder.py`) provides a scaffold with TODOs — fill in each section, then compare with the solution.

## Running

```bash
python prompt_builder.py
```

## Deliverable

A working `prompt_builder.py` that assembles and prints a well-structured RAG prompt for each test case, with token count estimates.
