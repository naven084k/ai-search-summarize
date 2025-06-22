# app/main.py

from fastapi import FastAPI, File, UploadFile,Query
import os
from app.document_processor import extract_text
from app.search_engine import search_documents
from app.rag_engine import summarize_text
from app.upload_handler import process_and_store
from app.stats_manager import increment_stat

UPLOAD_DIR = "data/raw/"
CHUNK_DIR = "data/chunks/"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHUNK_DIR, exist_ok=True)

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        temp_path = f"temp_uploads/{file.filename}"
        os.makedirs("temp_uploads", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(contents)

        chunks_added = process_and_store(temp_path)
        os.remove(temp_path)

        return {"message": f"Uploaded and processed {chunks_added} chunks from {file.filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/search/")
def search(query: str = Query(...)):
    try:
        refined_query, results = search_documents(query)
        full_response = []
        
        for result in results:
            summary = summarize_text(result["content"])
            full_response.append({
                "source": result["source"],
                "score": result["score"],
                "summary": summary,
                "chunks": result["chunks"]
            })
        increment_stat("queries")
        return {"refined_query": refined_query, "results": full_response}
    except Exception as e:
        return {"error": str(e)}