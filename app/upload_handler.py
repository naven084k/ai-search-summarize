# app/upload_handler.py

import os
from uuid import uuid4
from app.text_chunker import chunk_text
from app.embedder import embed_text
from app.chroma_store import add_document_chunks
from app.stats_manager import increment_stat

import pdfplumber
import docx

def extract_text_from_file(file_path: str) -> str:
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")


def process_and_store(file_path: str):
    filename = os.path.basename(file_path)
    text = extract_text_from_file(file_path)

    chunks = chunk_text(text)
    embeddings = embed_text(chunks)

    chunk_entries = []
    for i in range(len(chunks)):
        chunk_entries.append({
            "id": str(uuid4()),
            "text": chunks[i],
            "embedding": embeddings[i],
            "metadata": {"source": filename}
        })

    add_document_chunks(chunk_entries)
    increment_stat("uploads")
    return len(chunks)
