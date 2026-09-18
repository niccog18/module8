import json
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"


def generate(prompt, system_prompt=None, context=None, temperature=None):
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    if context:
        messages.append({
            "role": "system",
            "content": (
                "Use the following context to answer the user's question. "
                "Only use information supported by the context. "
                "If the answer cannot be determined from the context, "
                "say that the information is not provided in the context.\n\n"
                f"Context:\n{context}"
            )
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    if temperature is not None:
        payload["options"] = {
            "temperature": temperature
        }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    start_time = time.perf_counter()

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    elapsed = time.perf_counter() - start_time

    response_text = result["message"]["content"]

    return response_text, elapsed


def print_result(label, response, elapsed):
    print(f"\n{label}")
    print("-" * 70)
    print(response)
    print(f"\nResponse time: {elapsed:.2f} seconds")


def experiment_1():
    print("\n" + "=" * 70)
    print("EXPERIMENT 1: SAME QUESTION, DIFFERENT SYSTEM PROMPTS")
    print("=" * 70)

    question = "What is an API?"

    response_1, time_1 = generate(question)

    response_2, time_2 = generate(
        question,
        system_prompt="Explain like I'm 5 years old."
    )

    response_3, time_3 = generate(
        question,
        system_prompt=(
            "You are a senior software architect. "
            "Be technical and precise."
        )
    )

    print_result("1A - No System Prompt", response_1, time_1)
    print_result("1B - Explain Like I'm 5", response_2, time_2)
    print_result("1C - Senior Software Architect", response_3, time_3)

    print("\nObservation:")
    print(
        "The system prompt changes the style, vocabulary, level of detail, "
        "and intended audience of the response even though the question "
        "remains the same."
    )


def experiment_2():
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: RAG-STYLE CONTEXT GROUNDING")
    print("=" * 70)

    context = (
        "FastAPI is a Python web framework designed for building APIs. "
        "It is based on standard Python type hints and uses Pydantic for "
        "data validation. FastAPI can automatically generate OpenAPI "
        "documentation and is commonly used for building modern REST APIs."
    )

    question_1 = "What Python framework is described in the context?"
    question_2 = "Who originally created FastAPI?"

    response_1, time_1 = generate(
        question_1,
        context=context
    )

    response_2, time_2 = generate(
        question_2,
        context=context
    )

    print("\nContext:")
    print(context)

    print_result(
        "2A - Question Answerable From Context",
        response_1,
        time_1
    )

    print_result(
        "2B - Question NOT Answerable From Context",
        response_2,
        time_2
    )

    print("\nObservation:")
    print(
        "The first question can be answered directly from the supplied context. The second question cannot be answered from the context, but the model still provided an unsupported answer, demonstrating that prompt-based context grounding does not always prevent hallucinations."
    )


def experiment_3():
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: RESPONSE TIMING")
    print("=" * 70)

    prompts = [
        (
            "Short",
            "What is Python used for?"
        ),
        (
            "Medium",
            "What are the key benefits of using Python for web development "
            "and building modern API driven software applications efficiently today?"
        ),
        (
            "Long",
            "Explain how Python can be used to build a modern web application "
            "with FastAPI, validate incoming data using Pydantic models, interact "
            "with a relational database, process core business logic, and return "
            "structured JSON responses to a client while also supporting automatic "
            "interactive API documentation for developers and end users alike."
        )
    ]

    results = []

    for label, prompt in prompts:
        response, elapsed = generate(prompt)

        word_count = len(prompt.split())

        print_result(
            f"{label} Prompt ({word_count} words)",
            response,
            elapsed
        )

        results.append((label, word_count, elapsed))

    print("\nTiming Comparison:")
    print("-" * 70)

    for label, word_count, elapsed in results:
        print(
            f"{label:<10} | Prompt words: {word_count:<3} | "
            f"Time: {elapsed:.2f}s"
        )

    print("\nObservation:")
    print(
        "Response time can vary based on prompt length, generated response "
        "length, model workload, and local hardware. The longer prompt may "
        "take more time to process, but response length and other factors "
        "also affect the total response time."
    )


def experiment_4():
    print("\n" + "=" * 70)
    print("EXPERIMENT 4: TEMPERATURE")
    print("=" * 70)

    prompt = (
        "Describe a futuristic city in three sentences."
    )

    response_low, time_low = generate(
        prompt,
        temperature=0.1
    )

    response_high, time_high = generate(
        prompt,
        temperature=1.0
    )

    print_result(
        "4A - Temperature 0.1",
        response_low,
        time_low
    )

    print_result(
        "4B - Temperature 1.0",
        response_high,
        time_high
    )

    print("\nObservation:")
    print(
        "Lower temperature generally produces more predictable and "
        "consistent responses, while higher temperature allows more "
        "variation and creativity."
    )


def main():
    print("=" * 70)
    print("OLLAMA EXPLORER")
    print("=" * 70)
    print(f"Model: {MODEL}")
    print(f"Endpoint: {OLLAMA_URL}")

    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()

    print("\n" + "=" * 70)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()