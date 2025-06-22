# app/embedder.py

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim embeddings

def embed_text(text_list: list[str]) -> list[list[float]]:
    return model.encode(text_list).tolist()
