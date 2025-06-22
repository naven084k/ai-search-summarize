# app/api_logic.py

from app.search_engine import search_documents
from app.rag_engine import summarize_text
from app.upload_handler import process_and_store
from app.stats_manager import increment_stat

def run_upload(file_path):
    chunks = process_and_store(file_path)
    increment_stat("uploads")
    return chunks

def run_search(query):
    refined, results = search_documents(query)  # results = list of dicts

    formatted_results = []

    for r in results:
        summary = summarize_text(r.get("text") or r.get("content", ""))
        
        formatted_results.append({
            "text": r.get("text") or r.get("content", ""),
            "score": r.get("score", 0.0),
            "metadata": r.get("metadata", {"source": "Unknown"}),
            "summary": summary
        })

    increment_stat("queries")
    return refined, formatted_results
