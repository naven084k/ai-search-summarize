# app/query_refiner.py

from transformers import pipeline

# Load lightweight T5 model (will be <500MB in RAM)
model_id = "google/flan-t5-small"
refiner = pipeline("text2text-generation", model=model_id)

def refine_query(user_query: str) -> str:
    prompt = f"Rewrite this query to be more precise for document search:\n{user_query}"
    output = refiner(prompt, max_new_tokens=50, do_sample=False)
    return output[0]["generated_text"].strip()
