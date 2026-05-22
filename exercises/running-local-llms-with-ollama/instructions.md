# Running Local LLMs with Ollama — Explorer

**Module:** 8 — RAG Intro & Docker Deployment
**Estimated time:** 25 minutes

## Objective

Get comfortable with Ollama by exploring how system prompts, context grounding, and model parameters affect LLM responses.

## Prerequisites

Ollama installed and running with at least one model pulled:

```bash
ollama serve          # in one terminal
ollama pull llama3.2:1b
```

## What You'll Build

An `ollama_explorer.py` that runs 4 experiments:

1. **Same question, different system prompts** — Ask "What is an API?" with no system prompt, an "explain like I'm 5" prompt, and a technical architect prompt. Compare the responses.
2. **RAG-style context grounding** — Provide a short paragraph as context, ask one question answerable from it, and one that isn't. Observe whether the model correctly stays grounded.
3. **Response timing** — Ask questions of varying length (short/medium/long) and record how response time scales.
4. **Temperature (optional bonus)** — Compare `temperature: 0.1` vs `temperature: 1.0` on the same prompt.

## Reference Code

The starter file (`ollama_explorer.py`) provides a scaffold with TODOs — fill in each section.

## Running

```bash
python ollama_explorer.py
```

## Deliverable

A working script that runs all 4 experiments and prints comparisons. Include brief inline comments noting what you observed.
