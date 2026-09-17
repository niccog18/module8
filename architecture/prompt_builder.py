from typing import List, Dict

SYSTEM_PROMPT = """You are a helpful question-answering assistant.
Answer the user's question using only the provided context.
Do not use outside knowledge or make up information.
If the context does not contain enough information to answer the question,
say that the information is not available in the provided context.
When using information from the context, cite the source using its source label.
"""


def build_rag_prompt(
    question: str,
    retrieved_chunks: List[Dict[str, str]]
) -> str:
    context_sections = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk.get("source", "Unknown source")
        text = chunk.get("text", "")

        context_sections.append(
            f"[Context {index}]\n"
            f"Source: {source}\n"
            f"{text}"
        )

    context = "\n\n".join(context_sections)

    prompt = f"""{SYSTEM_PROMPT}

Retrieved Context:
{context}

User Question:
{question}

Instructions:
- Answer using only the retrieved context.
- Cite the source label for information used in your answer.
- If the context does not contain the answer, state that clearly.
"""
    return prompt


def estimate_token_count(text: str) -> int:
    return len(text) // 4


def display_prompt(question: str, retrieved_chunks: List[Dict[str, str]]) -> None:
    prompt = build_rag_prompt(question, retrieved_chunks)
    token_estimate = estimate_token_count(prompt)

    print("=" * 70)
    print("ASSEMBLED RAG PROMPT")
    print("=" * 70)
    print(prompt)
    print("=" * 70)
    print(f"Character count: {len(prompt)}")
    print(f"Estimated token count: {token_estimate}")
    print()


def main() -> None:
    chunks_for_question_1 = [
        {
            "source": "fastapi.txt",
            "text": (
                "FastAPI is a modern Python web framework for building APIs. "
                "It uses Python type hints to provide automatic validation "
                "and documentation."
            ),
        },
        {
            "source": "rest-apis.txt",
            "text": (
                "REST APIs commonly use HTTP methods such as GET, POST, "
                "PUT, PATCH, and DELETE to perform operations on resources."
            ),
        },
    ]

    chunks_for_question_2 = [
        {
            "source": "streamlit.txt",
            "text": (
                "Streamlit is a Python framework for building interactive "
                "data and machine learning applications."
            ),
        },
        {
            "source": "python-fundamentals.txt",
            "text": (
                "Python functions allow code to be organized into reusable "
                "blocks that can accept parameters and return values."
            ),
        },
    ]

    question_1 = "What features does FastAPI provide for building APIs?"
    question_2 = "What is Streamlit used for?"

    print("\nTEST 1")
    display_prompt(question_1, chunks_for_question_1)

    print("\nTEST 2")
    display_prompt(question_2, chunks_for_question_2)


if __name__ == "__main__":
    main()