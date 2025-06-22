# app/query_refiner.py

from transformers import pipeline

# Load lightweight T5 model (will be <500MB in RAM)
model_id = "google/flan-t5-small"
refiner = pipeline("text2text-generation", model=model_id)

def refine_query(user_query: str) -> str:
    """
    Uses flan-t5-small to refine or clarify a user query for better vector search.
    Returns a cleaned, semantic-search-friendly intent phrase.
    """
    prompt = f"""Only consider Extracting keywords from the user question for semantic search and don't answer using your data:
    Query: {user_query}
    """
    output = refiner(prompt, max_new_tokens=50, do_sample=False)
    print('response is = '+output[0]["generated_text"].strip())
    return output[0]["generated_text"].strip()
