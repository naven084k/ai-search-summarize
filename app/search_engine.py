from app.embedder import embed_text
from app.query_refiner import refine_query
from app.chroma_store import search_similar_chunks

def search_documents(user_query, top_k=1):
    #refined_query = refine_query(user_query)
    embedding = embed_text([user_query])[0]
    results = search_similar_chunks(embedding, 1)

    # Group by source filename
    files = {}
    for r in results:
        src = r["metadata"].get("source", "")
        if src not in files:
            files[src] = {
                "source": src,
                "score": r["score"],
                "chunks": [r],
                "content": r["text"]
            }
        else:
            files[src]["chunks"].append(r)
            files[src]["content"] += "\n" + r["text"]
            files[src]["score"] = min(files[src]["score"], r["score"])

    return user_query, list(files.values())
