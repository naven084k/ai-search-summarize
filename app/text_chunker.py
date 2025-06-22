# app/text_chunker.py

def chunk_text(text: str, max_words: int = 200, overlap: int = 20) -> list[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words - overlap):
        chunk = words[i:i + max_words]
        chunks.append(" ".join(chunk))

    return chunks
