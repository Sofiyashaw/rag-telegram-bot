from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from rag.chunker import chunk_text
from config import CHUNK_SIZE, CHUNK_OVERLAP, SIMILARITY_THRESHOLD
from utils.logger import log

class Retriever:
    def __init__(self, data_path="data"):
        log("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.docs = []
        self.doc_names = []

        log("Loading & chunking documents...")
        for file in os.listdir(data_path):
            with open(f"{data_path}/{file}", "r", encoding="utf-8") as f:
                text = f.read()
                chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

                for chunk in chunks:
                    self.docs.append(chunk)
                    self.doc_names.append(file)

        log(f"Total chunks created: {len(self.docs)}")

        embeddings = self.model.encode(self.docs)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))

        log("Retriever READY ")

    def retrieve(self, query, top_k=2):
        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), top_k
        )

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if dist < SIMILARITY_THRESHOLD:
                results.append((self.docs[idx], self.doc_names[idx]))

        log(f"Retrieved {len(results)} relevant chunks")

        return results