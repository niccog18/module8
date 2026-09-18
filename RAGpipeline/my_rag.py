import os
import json
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
DISTANCE_THRESHOLD = 1.2

SYSTEM_PROMPT = """You are a retrieval-augmented generation assistant.

Your job is to answer the user's question using ONLY the retrieved context provided to you.

IMPORTANT RULES:

1. If the answer is directly stated in the retrieved context, answer the question clearly and directly.
2. Use only information contained in the retrieved context.
3. Do not use outside knowledge.
4. Do not guess or invent information.
5. Do not fill in missing information using your general knowledge.
6. If the retrieved context does not contain enough information to answer the question, say:
   "The provided documents do not contain enough information to answer this question."
7. Do not invent source filenames.
8. Every factual claim must be supported by the retrieved context.
9. Cite the supporting source document using its exact filename in square brackets.
10. Use citations such as [fastapi.txt] or [streamlit.txt].
11. Keep answers concise and directly answer the user's question.
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


def is_relevant(chunks):
    if not chunks:
        return False

    best_distance = chunks[0]["distance"]

    return best_distance <= DISTANCE_THRESHOLD


def display_retrieved_chunks(chunks):
    print("\n" + "=" * 60)
    print(f"Retrieved {len(chunks)} chunks:")
    print("=" * 60)

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n[{index}] Source: {chunk['source']}")
        print(f"Distance: {chunk['distance']:.4f}")
        print("-" * 60)
        print(chunk["text"])


def build_context(chunks):
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"Source: {chunk['source']}\n"
            f"Context:\n{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def generate_answer(question, chunks):
    context = build_context(chunks)

    user_prompt = f"""Retrieved context:
{context}

User question:
{question}

Instructions:

First, check whether the answer to the user's question is explicitly
contained in the retrieved context.

If the answer is explicitly stated in the context, answer it directly
using that information.

If the context does not contain enough information to answer the
question, respond with:

"The provided documents do not contain enough information to answer this question."

Do not use outside knowledge.
Do not guess.
Do not invent facts.
Do not invent source filenames.

For every factual answer, cite the exact source filename in square
brackets, such as [fastapi.txt].
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

        return response_data["message"]["content"]

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


def main():
    print("=" * 60)
    print("RAG PIPELINE")
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
    print("RAG Pipeline Ready!")
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

        if not retrieved_chunks:
            print("\nNo relevant documents were found.")
            continue

        display_retrieved_chunks(retrieved_chunks)

        best_distance = retrieved_chunks[0]["distance"]

        print("\n" + "=" * 60)
        print(f"Best retrieval distance: {best_distance:.4f}")
        print(f"Relevance threshold: {DISTANCE_THRESHOLD:.4f}")
        print("=" * 60)

        if not is_relevant(retrieved_chunks):
            print(
                "\nThe provided documents do not contain enough "
                "relevant information to answer this question."
            )
            continue

        print("\n" + "=" * 60)
        print("Generating answer with Ollama...")
        print("=" * 60)

        answer = generate_answer(
            question,
            retrieved_chunks
        )

        print("\nAnswer:")
        print("-" * 60)
        print(answer)


if __name__ == "__main__":
    main()