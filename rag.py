from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import requests

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

docs = []
doc_names = []

# Load documents
print("Loading documents...")
for file in os.listdir("data"):
    with open(f"data/{file}", "r", encoding="utf-8") as f:
        text = f.read()
        docs.append(text)
        doc_names.append(file)

# Create embeddings
print("Creating embeddings...")
embeddings = model.encode(docs)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

print("RAG system READY ✅")

# 🔹 CACHE for queries
query_cache = {}

def retrieve(query, top_k=1):
    # Check cache
    if query in query_cache:
        print("Cache hit ✅")
        return query_cache[query]

    query_embedding = model.encode([query])
    distances, indices = index.search(
        np.array(query_embedding).astype('float32'), top_k
    )

    results = [(docs[i], doc_names[i]) for i in indices[0]]

    query_cache[query] = results  # store in cache
    print(f"Retrieved docs for query '{query}':", results)

    return results


def generate_answer(query, context):
    try:
        prompt = f"""
        Answer ONLY using the context below.
        If not found, say "I don't know".
        Keep answer short.

        Context:
        {context}

        Question:
        {query}
        """

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json().get("response", "No response")

    except Exception as e:
        return f"Error: {str(e)}. Is Ollama running?"


# 🔹 Summarization function
def summarize_text(text):
    try:
        prompt = f"Summarize this in 2-3 lines:\n{text}"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json().get("response", "No summary")

    except Exception as e:
        return f"Error: {str(e)}"