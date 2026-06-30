# RAG-Gemma

Retrieval-augmented generation (RAG) pipeline that grounds [Gemma 3](https://ai.google.dev/gemma)
(served locally via [Ollama](https://ollama.com)) on recent NLP/AI research papers fetched
from arXiv. Two notebooks: one to build the vector index, one to chat against it.

## How it works

1. **`ingest.ipynb`** — fetches papers from arXiv (categories `cs.CL`, `cs.AI` by
   default), chunks their abstracts/text, embeds the chunks with
   [`sentence-transformers`](https://www.sbert.net/) (`all-MiniLM-L6-v2`), and stores
   them in a local [ChromaDB](https://www.trychroma.com/) collection (`./chroma_db`).
2. **`ragapp.ipynb`** — a Gradio chat UI that, for every user question, embeds the
   query, retrieves the top-k most relevant chunks from ChromaDB, injects them into the
   system prompt alongside source citations, and streams a grounded answer from Gemma 3
   over Ollama.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running, with the model pulled:

  ```bash
  ollama pull gemma3:4b
  ollama serve
  ```
- Internet access for `ingest.ipynb` (to query the arXiv API)

## Setup

```bash
cd "LLMs/RAG-Gemma"
pip install -r requirements.txt
```

## Run

### 1. Build the index

Open and run `ingest.ipynb` top to bottom. Key config (top of notebook):

| Variable | Description | Default |
|---|---|---|
| `DATE_FROM` / `DATE_TO` | arXiv publish-date window | `2025-03-01` – `2025-06-01` |
| `ARXIV_CATS` | arXiv categories to pull | `["cs.CL", "cs.AI"]` |
| `MAX_PAPERS` | total papers to ingest | `300` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | text chunking (chars) | `512` / `64` |
| `EMBED_MODEL` | sentence-transformer model | `all-MiniLM-L6-v2` |
| `CHROMA_DIR` | persistent vector store path | `./chroma_db` |
| `COLLECTION_NAME` | Chroma collection name | `arxiv_nlp` |

This creates a `./chroma_db/` directory (ignored by git — regenerate it locally; don't
commit it).

### 2. Chat

Open and run `ragapp.ipynb`. It connects to the `./chroma_db` collection created above
and launches a Gradio app for asking questions, with retrieved sources shown above each
answer.

## Notes

- `ragapp.ipynb` expects `ingest.ipynb` to have been run first so the Chroma collection
  exists.
- The vector store (`chroma_db/`) is excluded via `.gitignore` since it's generated data,
  not source.
