# Islamic Knowledge Assistant

A Retrieval-Augmented Generation (RAG) chatbot that answers questions using the Quran and Hadith,
built with **Streamlit**, **ChromaDB**, and a local **Ollama** LLM.

---


## Project structure

```
.
├── app.py                     # Streamlit web UI
├── main.py                    # CLI chat loop (for testing without Streamlit)
├── requirements.txt
├── .env                       # local config (not committed)
├── .env.example                # template for .env
├── data/raw/                  # source CSVs (quran.csv, hadith.csv)
├── vector_db/                 # ChromaDB persistent store (generated, gitignored)
└── src/
    ├── config/settings.py     # pydantic-settings config, reads .env
    ├── models/                # pydantic data models
    ├── factories/document_factory.py   # CSV row -> document/vector record
    ├── repositories/chroma_repository.py  # ChromaDB read/write
    ├── services/
    │   ├── retrieval_service.py  # queries Quran + Hadith collections
    │   ├── llm_service.py        # talks to Ollama chat model
    │   └── qa_service.py         # orchestrates retrieval -> prompt -> answer
    └── ingestion/build_vector_db.py  # one-time script: CSV -> ChromaDB
```

---

## How to run the project locally

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/download) installed on your machine

### 2. Install Ollama models
```bash
ollama serve            # start the Ollama server (leave running in its own terminal)
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### 3. Set up the Python project
```bash
cd "Islamic Chatbot - Project -"
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure environment
`.env` is already set up with sensible defaults. Review/edit if needed:
```
CHROMA_PATH=./vector_db
QURAN_COLLECTION=quran
HADITH_COLLECTION=hadith
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
QURAN_TOP_K=3
HADITH_TOP_K=3
```

### 5. Build the vector database (one-time step)
This reads `data/raw/quran.csv` and `data/raw/hadith.csv`, embeds every verse/hadith via
Ollama, and stores them in ChromaDB. With ~6,236 Quran verses and ~34,500 hadiths, this
will take a while (embedding speed depends on your machine) — let it run to completion.
```bash
python -m src.ingestion.build_vector_db
```
You should see `=== Vector Database Build Complete ===` at the end.

### 6. Run the app
```bash
streamlit run app.py
```
Open the URL Streamlit prints (usually `http://localhost:8501`).

Alternatively, test from the command line without a browser:
```bash
python main.py
```

---

