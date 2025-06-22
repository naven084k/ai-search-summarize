# app/rag_engine.py

from transformers import pipeline

# Use same model as query refiner
model_id = "google/flan-t5-small"
summarizer = pipeline("text2text-generation", model=model_id)

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following document content:\n{text}"
    output = summarizer(prompt, max_new_tokens=100, do_sample=False)
    return output[0]["generated_text"].strip()
