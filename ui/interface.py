# ui/interface.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from transformers import pipeline

import streamlit as st

from app.api_logic import run_search


import requests
from app.upload_handler import process_and_store
from app.stats_manager import read_stats

@st.cache_resource
def load_flan_generator():
    return pipeline("text2text-generation", model="google/flan-t5-small")

flan_generator = load_flan_generator()

def generative_qna(question, results, max_chunks=5, min_len=10):
    answers = []

    prompt_template = (
        "Answer the question in 2-3 sentences based on the context.\n\n"
        "Question: {question}"
        "Context:\n{context}\n\n"
        
    )

    for r in results[:max_chunks]:
        context = r["text"]
        prompt = prompt_template.format(context=context, question=question)

        try:
            response = flan_generator(prompt, max_length=512, do_sample=False)
            answer = response[0]["generated_text"].strip()

            if (
                answer and
                len(answer) >= min_len and
                answer.lower() not in {"", "yes", "no", "none", "n/a", "unknown"}
            ):
                answers.append({
                    "answer": answer,
                    "source": r.get("metadata", {}).get("source", "unknown"),
                    "score": r.get("score"),
                    "chunk": context
                })

        except Exception as e:
            print("Flan error:", e)
            continue

    if not answers:
        return {"answer": "🤷 I couldn't find a clear answer.", "sources": [], "chunks": []}

    combined = "\n\n".join([f"• {a['answer']}" for a in answers])

    return {
        "answer": combined,
        "sources": list({a["source"] for a in answers}),
        "chunks": [a["chunk"] for a in answers]
    }


st.set_page_config(page_title="Document Semantic Search", layout="wide")
st.title("Semantic Document Search with LLM Support")

st.sidebar.subheader("📈 App Stats")

stats = read_stats()

st.sidebar.metric("📤 Documents Uploaded", stats.get("uploads", 0))
st.sidebar.metric("🔍 Search Queries", stats.get("queries", 0))


st.sidebar.header("📤 Upload a Document")
uploaded_file = st.sidebar.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])


if uploaded_file:
    temp_path = f"temp_uploads/{uploaded_file.name}"
    os.makedirs("temp_uploads", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        with st.spinner("Embedding and storing in Chroma..."):
            num_chunks = process_and_store(temp_path)
        st.success(f"✅ Successfully added {num_chunks} chunks from {uploaded_file.name}")
    except Exception as e:
        st.error(f"❌ Failed: {str(e)}")

    os.remove(temp_path)

st.divider()

# --- Combined Search & QnA ---
st.header("🧠 Ask or Search")
query = st.text_input("Type your question or topic and choose an action:")

col1, col2, _ = st.columns([2, 2, 3])  # 3rd column pushes them together

with col1:
    run_search_button = st.button("🔍 Search", use_container_width=True)

with col2:
    run_qna_button = st.button("🧠 Get Answer", use_container_width=True)

if query:
    # --- Search: for summarization / document overview ---
    if run_search_button:
        with st.spinner("Running semantic search..."):
            refined_query, results = run_search(query)
            if results:
                st.session_state["search_results"] = results
                st.session_state["query"] = query
            else:
                st.warning("❌ No results found.")

    # --- QnA: directly answer using top chunks ---
    elif run_qna_button:
        if "search_results" not in st.session_state:
            # Run a fresh search before attempting QnA
            with st.spinner("Searching..."):
                _, results = run_search(query)
                st.session_state["search_results"] = results
                st.session_state["query"] = query
        else:
            results = st.session_state["search_results"]

        with st.spinner("Generating answer using flan-t5-small..."):
            result = generative_qna(
                question=query,
                results=st.session_state.get("search_results", []),
                max_chunks=5
            )

        st.success("🟢 Answer:")
        st.markdown(result["answer"])
        st.caption(f"📄 Sources: {', '.join(result['sources'])}")

        with st.expander("🔍 View source chunks"):
            for chunk in result["chunks"]:
                st.markdown(chunk)

# --- Show search results if available ---
if "search_results" in st.session_state and run_search_button:
    st.markdown(f"### 🔍 Top matching chunks for: **{query}**")
    for i, r in enumerate(st.session_state["search_results"]):
        st.markdown(f"Summary: {r['summary']}")
        with st.expander("Show original text"):
            st.markdown(r["text"])

