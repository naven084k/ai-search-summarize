# app/chroma_store.py

import chromadb
from chromadb.config import Settings
from uuid import uuid4

# app/chroma_store.py

import chromadb
from chromadb.config import Settings


client = chromadb.PersistentClient(path="data/chroma_store")
collection = client.get_or_create_collection(name="documents")



def add_document_chunks(chunks: list[dict]):
    collection.add(
        documents=[c["text"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[c["id"] for c in chunks]
    )
   


def search_similar_chunks(query_embedding: list[float], top_k: int = 5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return [
        {
            "text": doc,
            "score": round(score, 3),
            "metadata": metadata
        }
        for doc, score, metadata in zip(
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0]
        )
    ]
