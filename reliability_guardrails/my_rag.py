import os
import json
import re
import urllib.request
import urllib.error

import chromadb
from sentence_transformers import SentenceTransformer

DOCS_DIR = "docs"
CHROMA_PATH = "rag_db"
COLLECTION_NAME = "rag_documents"

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

TOP_K = 3
DISTANCE_THRESHOLD = 1.0

SYSTEM_PROMPT = """You are a retrieval-augmented generation assistant.

Your job is to answer the user's question using ONLY the retrieved
context provided to you.

IMPORTANT GUARDRAILS:

1. Never make up information.
2. Never guess or use outside knowledge.
3. Only answer using information contained in the retrieved context.
4. You must answer ALL parts of the user's question using the retrieved
   context.
5. If ANY part of the user's question cannot be answered from the
   retrieved context, explicitly say:
   "I don't know" for that part.
6. Do not omit an unanswered part of the question.
7. Do not fill in missing information using your general knowledge.
8. Every factual claim must be supported by the retrieved context.
9. Always cite the supporting source document using its exact
   filename in square brackets.
10. Use citations such as [fastapi.txt] or [streamlit.txt].
11. Never invent source filenames.
12. If the retrieved context cannot answer the question at all, say:
    "I don't know. The provided documents do not contain enough
    information to answer this question."
13. Do not discuss information that is not present in the retrieved
    context.
14. Keep answers concise and directly address every part of the
    user's question.
"""


def load_documents():
    documents = []

    if not os.path.exists(DOCS_DIR):
        print(f"Error: '{DOCS_DIR}' folder was not found.")
        return documents

    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DOCS_DIR, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()

            documents.append({
                "filename": filename,
                "text": text
            })

        except OSError as error:
            print(f"Could not read {filename}: {error}")

    return documents


def chunk_documents(documents):
    chunks = []

    for document in documents:
        paragraphs = document["text"].split("\n\n")

        for paragraph in paragraphs:
            paragraph = paragraph.strip()

            if not paragraph:
                continue

            chunks.append({
                "text": paragraph,
                "source": document["filename"]
            })

    return chunks


def create_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def ingest_documents(collection, chunks, model):
    if collection.count() > 0:
        print(f"Using existing collection: {collection.count()} chunks")
        return

    if not chunks:
        print("No document chunks were found.")
        return

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts).tolist()

    ids = [f"chunk_{index}" for index in range(len(chunks))]

    metadatas = [
        {"source": chunk["source"]}
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Ingested {len(chunks)} chunks into ChromaDB.")


def retrieve(question, collection, model):
    question_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=TOP_K
    )

    retrieved_documents = results.get("documents", [[]])[0]
    retrieved_metadatas = results.get("metadatas", [[]])[0]
    retrieved_distances = results.get("distances", [[]])[0]

    chunks = []

    for index, document in enumerate(retrieved_documents):
        metadata = retrieved_metadatas[index]
        distance = retrieved_distances[index]

        chunks.append({
            "text": document,
            "source": metadata.get("source", "unknown"),
            "distance": distance
        })

    return chunks


def filter_by_distance(chunks):
    """Return only chunks whose distance is below the threshold."""

    return [
        chunk
        for chunk in chunks
        if chunk["distance"] < DISTANCE_THRESHOLD
    ]


def get_confidence(chunks):
    """Determine confidence from the best filtered chunk distance."""

    if not chunks:
        return "low"

    best_distance = min(
        chunk["distance"]
        for chunk in chunks
    )

    if best_distance < 0.5:
        return "high"

    if best_distance < 1.0:
        return "medium"

    return "low"


def build_context(chunks):
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"Source: {chunk['source']}\n"
            f"Context:\n{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def display_retrieved_chunks(chunks):
    print("\n" + "=" * 60)
    print(f"Retrieved {len(chunks)} relevant chunks:")
    print("=" * 60)

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n[{index}] Source: {chunk['source']}")
        print(f"Distance: {chunk['distance']:.4f}")
        print("-" * 60)
        print(chunk["text"])


def context_contains_requested_detail(question, chunks):
    """
    Detect whether common requested details appear in the retrieved
    context.

    This provides a lightweight Python-side reliability check so the
    small local model is less likely to invent missing dates, years,
    or numeric information.
    """

    context = " ".join(
        chunk["text"]
        for chunk in chunks
    ).lower()

    question = question.lower()

    detail_patterns = {
        "year": [
            r"\byear\b",
            r"\breleased\b",
            r"\brelease date\b",
            r"\bwhen was\b",
            r"\bwhen did\b"
        ],
        "date": [
            r"\bdate\b",
            r"\bday\b",
            r"\bmonth\b",
            r"\bwhen\b"
        ],
        "number": [
            r"\bhow many\b",
            r"\bhow much\b",
            r"\bnumber of\b",
            r"\bcount\b",
            r"\b\d+\b"
        ]
    }

    requested_detail = None

    for detail_type, patterns in detail_patterns.items():
        if any(re.search(pattern, question) for pattern in patterns):
            requested_detail = detail_type
            break

    if requested_detail is None:
        return True

    if requested_detail == "year":
        has_year_word = bool(re.search(r"\byear\b", context))
        has_four_digit_year = bool(
            re.search(r"\b(?:19|20)\d{2}\b", context)
        )

        return has_year_word or has_four_digit_year

    if requested_detail == "date":
        has_date_word = bool(
            re.search(
                r"\b(?:date|day|month)\b",
                context
            )
        )

        has_date_pattern = bool(
            re.search(
                r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
                context
            )
        )

        return has_date_word or has_date_pattern

    if requested_detail == "number":
        return bool(
            re.search(
                r"\b\d+(?:\.\d+)?\b",
                context
            )
        )

    return True


def build_missing_detail_instruction(question, chunks):
    """
    Create an explicit instruction when the question requests a
    detail that is not present in the retrieved context.
    """

    if context_contains_requested_detail(question, chunks):
        return ""

    question_lower = question.lower()

    if any(
        phrase in question_lower
        for phrase in [
            "what year",
            "which year",
            "when was",
            "when did",
            "release year",
            "released"
        ]
    ):
        return """
IMPORTANT: The retrieved context does NOT contain a year or release
date.

You may answer other parts of the question that are directly supported
by the context.

For the missing year or release date, you MUST explicitly say:
"I don't know what year it was first released because that information
is not provided in the documents."

Do not provide a year from your general knowledge.
Do not mention possible years.
Do not speculate about the missing year.
"""

    if any(
        phrase in question_lower
        for phrase in [
            "how many",
            "how much",
            "number of",
            "count"
        ]
    ):
        return """
IMPORTANT: The retrieved context does NOT contain enough information
to determine the requested number.

You may answer other parts of the question that are directly supported
by the context.

For the missing number, explicitly say:
"I don't know because that information is not provided in the
documents."

Do not guess or calculate a number using outside knowledge.
"""

    return ""


def extract_supported_answer(chunks, question):
    """
    Create a concise fallback answer directly from the retrieved
    context when a requested detail is missing.
    """

    if not chunks:
        return (
            "I don't know. The provided documents do not contain "
            "enough information to answer this question."
        )

    first_chunk = chunks[0]

    sentences = re.split(
        r"(?<=[.!?])\s+",
        first_chunk["text"].strip()
    )

    supported_sentence = sentences[0].strip()

    if not supported_sentence:
        supported_sentence = first_chunk["text"].strip()

    question_lower = question.lower()

    if any(
        phrase in question_lower
        for phrase in [
            "what year",
            "which year",
            "when was",
            "when did",
            "release year",
            "released"
        ]
    ):
        return (
            f"{supported_sentence} [{first_chunk['source']}]\n\n"
            "I don't know what year it was first released because "
            "that information is not provided in the documents."
        )

    if any(
        phrase in question_lower
        for phrase in [
            "how many",
            "how much",
            "number of",
            "count"
        ]
    ):
        return (
            f"{supported_sentence} [{first_chunk['source']}]\n\n"
            "I don't know because that information is not provided "
            "in the documents."
        )

    return f"{supported_sentence} [{first_chunk['source']}]"


STOPWORDS = {
    "what", "when", "where", "which", "does", "did", "with", "from",
    "have", "were", "this", "that", "about", "there", "their", "into",
    "would", "could", "should", "some", "many", "much", "your", "you",
    "the", "and", "for", "are", "was", "how", "why", "who", "can",
    "will", "its", "it's", "please", "tell", "explain", "describe"
}


def answer_incorrectly_refuses(question, answer, chunks):
    """Detect when the model incorrectly says it cannot answer."""

    if "i don't know" not in answer.lower():
        return False

    question_words = {
        word.lower()
        for word in re.findall(r"\b[a-zA-Z]+\b", question)
    }

    context = " ".join(
        chunk["text"]
        for chunk in chunks
    ).lower()

    important_terms = [
        word
        for word in question_words
        if len(word) > 3 and word not in STOPWORDS
    ]

    if not important_terms:
        return False

    matched_terms = [
        term
        for term in important_terms
        if term in context
    ]

    return len(matched_terms) / len(important_terms) >= 0.6



def generate_answer(question, chunks):
    context = build_context(chunks)

    missing_detail_instruction = build_missing_detail_instruction(
        question,
        chunks
    )

    user_prompt = f"""Retrieved context:
{context}

User question:
{question}

Instructions:

Carefully compare the user's question against the retrieved context.

The user's question may contain multiple parts.

You MUST answer every part of the question.

If the retrieved context contains enough information to answer a
particular part, answer that part and cite the exact source filename.

If the retrieved context does NOT contain enough information to answer
a particular part, explicitly say:

"I don't know."

Do NOT omit an unanswered part.

Do NOT use outside knowledge to answer missing information.

Do NOT guess.

Do NOT invent facts.

Do NOT invent source filenames.

Do NOT discuss information that is not present in the retrieved
context.

Always cite factual claims with the exact source filename in square
brackets.

{missing_detail_instruction}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "stream": False
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            response_data = json.loads(
                response.read().decode("utf-8")
            )

        answer = response_data["message"]["content"].strip()

        if (
            missing_detail_instruction
            and "i don't know" not in answer.lower()
        ):
            return extract_supported_answer(
                chunks,
                question
            )

        if answer_incorrectly_refuses(
            question,
            answer,
            chunks
        ):
            return extract_supported_answer(
                chunks,
                question
            )

        return answer

    except urllib.error.URLError:
        return (
            "Error: Ollama is not running or cannot be reached. "
            "Please make sure Ollama is running and try again."
        )

    except urllib.error.HTTPError as error:
        return (
            f"Error: Ollama returned HTTP {error.code}. "
            "Please check that the model is available."
        )

    except TimeoutError:
        return (
            "Error: Ollama took too long to respond. "
            "Please try the question again."
        )

    except (KeyError, json.JSONDecodeError):
        return "Error: Ollama returned an unexpected response."


def rag_query(question, collection, model):
    """Run the complete guardrailed RAG pipeline."""

    retrieved_chunks = retrieve(
        question,
        collection,
        model
    )

    filtered_chunks = filter_by_distance(
        retrieved_chunks
    )

    chunks_retrieved = len(filtered_chunks)

    if not filtered_chunks:
        return {
            "answer": (
                "The provided documents do not contain enough "
                "relevant information to answer this question."
            ),
            "sources": [],
            "confidence": "low",
            "chunks_retrieved": 0
        }

    confidence = get_confidence(
        filtered_chunks
    )

    answer = generate_answer(
        question,
        filtered_chunks
    )

    sources = list(dict.fromkeys(
        chunk["source"]
        for chunk in filtered_chunks
    ))

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "chunks_retrieved": chunks_retrieved
    }


def display_structured_response(response):
    print("\n" + "=" * 60)
    print("STRUCTURED RESPONSE")
    print("=" * 60)

    print(json.dumps(
        response,
        indent=2
    ))


def main():
    print("=" * 60)
    print("GUARDRAILED RAG PIPELINE")
    print("=" * 60)

    print("\nLoading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Loading documents...")
    documents = load_documents()

    if not documents:
        print("No documents were found. Exiting.")
        return

    print(f"Loaded {len(documents)} documents.")

    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} paragraph chunks.")

    collection = create_collection()

    ingest_documents(
        collection,
        chunks,
        model
    )

    print("\n" + "=" * 60)
    print("Guardrailed RAG Pipeline Ready!")
    print(f"Distance threshold: {DISTANCE_THRESHOLD}")
    print(f"Top K: {TOP_K}")
    print("Ask questions about your documents.")
    print("Type 'quit' to exit.")
    print("=" * 60)

    while True:
        try:
            question = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not question:
            continue

        if question.lower() == "quit":
            print("\nGoodbye!")
            break

        print("\n" + "=" * 60)
        print(f"Question: {question}")
        print("=" * 60)

        retrieved_chunks = retrieve(
            question,
            collection,
            model
        )

        print(
            f"\nRetrieved {len(retrieved_chunks)} "
            f"candidate chunks."
        )

        filtered_chunks = filter_by_distance(
            retrieved_chunks
        )

        print(
            f"Chunks passing threshold: "
            f"{len(filtered_chunks)}"
        )

        if filtered_chunks:
            display_retrieved_chunks(
                filtered_chunks
            )

            confidence = get_confidence(
                filtered_chunks
            )

            print("\n" + "=" * 60)
            print(f"Confidence: {confidence}")
            print("=" * 60)

        print("\n" + "=" * 60)
        print("Generating structured response...")
        print("=" * 60)

        response = rag_query(
            question,
            collection,
            model
        )

        display_structured_response(response)


if __name__ == "__main__":
    main()