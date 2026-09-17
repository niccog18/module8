┌─────────────────────────────┐
│ 1. USER QUESTION INPUT      │
│                             │
│ User asks a question        │
│ Technology: Streamlit       │
│ Data: question text         │
└──────────────┬──────────────┘
               │
               │ question
               ▼
┌─────────────────────────────┐
│ 2. QUERY EMBEDDING          │
│                             │
│ Convert question into a     │
│ numerical vector            │
│ Technology:                 │
│ SentenceTransformers        │
│ Model: all-MiniLM-L6-v2     │
│ Data: question → embedding  │
└──────────────┬──────────────┘
               │
               │ query vector
               ▼
┌─────────────────────────────┐
│ 3. VECTOR DATABASE          │
│    RETRIEVAL                │
│                             │
│ Compare query embedding     │
│ with stored document        │
│ embeddings and retrieve     │
│ relevant chunks             │
│ Technology: ChromaDB        │
│ Data: vector → chunks       │
└──────────────┬──────────────┘
               │
               │ retrieved chunks
               │ + source metadata
               ▼
┌─────────────────────────────┐
│ 4. PROMPT ASSEMBLY          │
│                             │
│ Combine:                    │
│ • System instructions       │
│ • Retrieved context         │
│ • User question             │
│ • Citation instructions     │
│                             │
│ Technology: Python          │
│ Data: prompt containing     │
│ instructions + context +   │
│ question                    │
└──────────────┬──────────────┘
               │
               │ complete RAG prompt
               ▼
┌─────────────────────────────┐
│ 5. LLM GENERATION           │
│    + RESPONSE               │
│                             │
│ LLM generates an answer     │
│ using the supplied context  │
│ Technology: Ollama          │
│ Model: llama3.2:1b          │
│ Data: prompt → answer       │
└──────────────┬──────────────┘
               │
               │ generated response
               ▼
        ┌───────────────┐
        │ USER RECEIVES │
        │    ANSWER     │
        └───────────────┘