# app/vector_store.py

import faiss
import os
import pickle
import numpy as np

INDEX_PATH = "data/faiss_index/index.faiss"
META_PATH = "data/faiss_index/meta.pkl"

def save_index(index, metadata):
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, 'wb') as f:
        pickle.dump(metadata, f)

def load_index():
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, 'rb') as f:
            metadata = pickle.load(f)
        return index, metadata
    else:
        return None, []

def create_or_update_index(embeddings, metadatas):
    index, metadata = load_index()
    dim = embeddings.shape[1]

    if index is None:
        index = faiss.IndexFlatL2(dim)
        metadata = []

    index.add(embeddings)
    metadata.extend(metadatas)
    save_index(index, metadata)
