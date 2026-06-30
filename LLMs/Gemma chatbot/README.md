# Gemma Chatbot

A local, privacy-friendly chat UI built with [Gradio](https://www.gradio.app/) that talks
to a [Gemma 3](https://ai.google.dev/gemma) model served locally through
[Ollama](https://ollama.com). Supports image uploads (vision) and document uploads
(PDF / TXT / DOCX) whose text is injected into the prompt as context. Responses stream
token-by-token.

## Features

- Streaming chat over the Ollama `/api/chat` endpoint
- Image attachments (sent to the model as base64)
- Document attachments (PDF, TXT, DOCX) — text is extracted and added to the prompt
- Clean single-page UI with example prompts and a clear-conversation button
- Automatically finds a free port if `7860` is taken

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- The `gemma3:4b` model pulled:

  ```bash
  ollama pull gemma3:4b
  ollama serve
  ```

## Setup

```bash
cd "LLMs/Gemma chatbot"
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The app launches at `http://127.0.0.1:7860` (or the next free port up to `7869`).

## Configuration

Edit the constants near the top of `app.py`:

| Variable | Description | Default |
|---|---|---|
| `OLLAMA_URL` | Ollama chat endpoint | `http://localhost:11434/api/chat` |
| `MODEL_NAME` | Model name as pulled in Ollama | `gemma3:4b` |
| `SYSTEM_PROMPT` | System prompt sent on every request | see `app.py` |

## Notes

- All processing happens locally; no data is sent to external services.
- DOCX support requires `python-docx`, which is included in `requirements.txt`.
