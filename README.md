# 🔍 Document QnA Search App

A lightweight, fast, and privacy-friendly app to upload documents, search semantically using vector embeddings, and answer questions using a small LLM that runs even on CPU.

Built with **ChromaDB**, **Sentence Transformers**, and **google/flan-t5-small** to ensure you get fast and relevant answers with minimal resource usage.

---

## 🚀 Features

- 📁 Upload PDF, TXT, or DOCX documents
- 🧠 Search using semantic embeddings (not just keyword match)
- 🧾 Ask questions and get multi-line answers using a small language model
- ⚡ Runs entirely on CPU — ideal for local or cloud deployments
- 📊 Internal dashboard for query and upload stats
- 💾 Uses [ChromaDB](https://www.trychroma.com/) for fast vector similarity

---

## 🛠️ Tech Stack

| Layer           | Tool / Library                      |
|-----------------|-------------------------------------|
| UI              | Streamlit                           |
| Embeddings      | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector DB       | ChromaDB                            |
| QnA Model       | `google/flan-t5-small` (Generative) |
| File Parsing    | `PyMuPDF`, `python-docx`, `langchain` |
| Data Storage    | Chroma local persistence (`./data/`) |

---

## 💡 Use Case

> Upload any set of documents — manuals, policies, books, PDFs — and ask natural language questions like:
>
> - "What are the key features of this product?"
> - "When was this regulation last updated?"
> - "Summarize the main idea of chapter 3"
>
> Useful for:
> - Internal knowledge base search
> - Support tools
> - Enterprise document review

---

## 🖥️ Local Development

### ✅ Requirements

- Python 3.8+
- `virtualenv` (recommended)

### 📦 Setup

```bash
# 1. Clone the repo
git clone https://github.com/naven084k/ai-search-summarize.git
cd ai-search-summarize

# 2. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run ui/interface.py
