import base64
import json
import warnings

import gradio as gr
import requests
from pypdf import PdfReader
from starlette.exceptions import StarletteDeprecationWarning

warnings.filterwarnings(
    "ignore",
    message=".*HTTP_422_UNPROCESSABLE_ENTITY.*",
    category=StarletteDeprecationWarning,
)

THEME = gr.themes.Default(
    primary_hue="violet",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("Inter"),
)

CSS = """
/* ── full-page layout, no boxed chat container ── */
.gradio-container { max-width: 900px !important; margin: 0 auto; padding-top: 0 !important; }

/* ── small top-right heading ── */
#header-row { display: flex; justify-content: flex-end; align-items: center;
              padding: 0.8rem 1rem 0.4rem; gap: 0.5rem; }
#header-row h1 {
    font-size: 1.05rem; font-weight: 600; margin: 0; letter-spacing: -0.2px;
    background: linear-gradient(135deg, #7c3aed, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* ── chat area takes the whole page, no card/box ── */
#chatbox { border: none !important; background: transparent !important; box-shadow: none !important; }
#chatbox .bubble-wrap { background: transparent !important; }

/* ── input row pinned with breathing room ── */
#input-row { align-items: flex-end; gap: 8px; padding: 0 1rem; }
#msg-box textarea { border-radius: 10px !important; font-size: 0.95rem; }
#send-btn { min-width: 80px; border-radius: 10px !important; }
#upload-btn { min-width: 46px !important; border-radius: 10px !important; }

#footer { text-align: center; color: #475569; font-size: 0.78rem;
          padding: 0.8rem 0 0.2rem; }
"""

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma3:4b"
SYSTEM_PROMPT = """You are a helpful, concise, and friendly AI assistant powered by Gemma 3.
Answer questions clearly. If you are unsure, say so honestly."""


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )
    return ""

def history_to_messages(history) -> list[dict]:
    messages = []
    for turn in history:
        if isinstance(turn, dict):
            text = extract_text(turn.get("content", "")).strip()
            if text:
                messages.append({"role": turn["role"], "content": text})
        elif isinstance(turn, (list, tuple)) and len(turn) == 2:
            user_text = extract_text(turn[0]).strip()
            asst_text = extract_text(turn[1]).strip()
            if user_text:
                messages.append({"role": "user",      "content": user_text})
            if asst_text:
                messages.append({"role": "assistant", "content": asst_text})
    return messages

def image_to_base64(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def extract_file_text(filepath: str, max_chars: int = 12000) -> str:
    """Extract readable text from pdf / txt / docx for injection into the prompt."""
    lower = filepath.lower()
    try:
        if lower.endswith(".pdf"):
            reader = PdfReader(filepath)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif lower.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif lower.endswith(".docx"):
            from docx import Document   # python-docx, optional dep
            doc = Document(filepath)
            text = "\n".join(p.text for p in doc.paragraphs)
        else:
            return ""
        return text[:max_chars]
    except Exception as e:
        return f"[Could not read file: {e}]"


# ── Ollama call ───────────────────────────────────────────────────────────────
def chat_with_ollama(history, image_path: str | None = None, file_text: str | None = None):
    """Normalise history, optionally attach an image or extracted file text, stream response."""
    messages = history_to_messages(history)

    if messages:
        for m in reversed(messages):
            if m["role"] == "user":
                if image_path:
                    m["images"] = [image_to_base64(image_path)]
                if file_text:
                    m["content"] = (
                        f"{m['content']}\n\n--- Attached document content ---\n{file_text}"
                    )
                break

    payload = {
        "model":    MODEL_NAME,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages],
        "stream":   True,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                token = chunk.get("message", {}).get("content", "")
                full_response += token
                yield full_response

    except requests.exceptions.ConnectionError:
        yield "⚠️  Cannot connect to Ollama. Make sure it's running: `ollama serve`"
    except Exception as e:
        yield f"⚠️  Error: {str(e)}"


# ── UI ────────────────────────────────────────────────────────────────────────
def build_ui():
    with gr.Blocks() as demo:

        # Small heading, top-right
        with gr.Row(elem_id="header-row"):
            gr.HTML("<h1>✦ Gemma Chatbot</h1>")

        # Chat window — full width, no boxed card
        chatbot = gr.Chatbot(
            elem_id="chatbox",
            height=600,
            show_label=False,
            avatar_images=(None, None),   # no avatar icons either side
        )

        # Input row: upload button + textbox + send
        with gr.Row(elem_id="input-row"):
            upload = gr.UploadButton(
                "📎",
                file_types=["image", ".pdf", ".txt", ".docx"],
                elem_id="upload-btn",
                scale=0,
            )
            msg = gr.Textbox(
                placeholder="Ask me anything…",
                show_label=False,
                elem_id="msg-box",
                scale=9,
                autofocus=True,
            )
            send = gr.Button("Send", variant="primary", elem_id="send-btn", scale=1)

        # Track the most recently uploaded file path
        uploaded_file_state = gr.State(None)
        file_badge = gr.HTML(visible=False)

        gr.Examples(
            examples=[
                "Explain transformers in simple terms.",
                "Write a Python function to reverse a linked list.",
                "What are the pros and cons of RAG vs fine-tuning?",
                "Summarise the history of large language models.",
            ],
            inputs=msg,
            label="Try an example",
        )

        clear = gr.Button("🗑  Clear conversation", variant="secondary", size="sm")
        gr.HTML('<div id="footer">Running 100% locally — your data never leaves your machine.</div>')

        # ── Wiring ──────────────────────────────────────────────────────────
        def on_upload(file):
            if file is None:
                return None, gr.update(visible=False)
            name = file.name.split("/")[-1].split("\\")[-1]
            return file.name, gr.update(value=f"📎 Attached: <b>{name}</b>", visible=True)

        upload.upload(on_upload, upload, [uploaded_file_state, file_badge])

        def user_turn(user_msg, history, file_path):
            history = history or []
            display_msg = user_msg
            if file_path:
                fname = file_path.split("/")[-1].split("\\")[-1]
                display_msg = f"{user_msg}\n\n📎 *{fname}*" if user_msg else f"📎 *{fname}*"
            history.append({"role": "user",      "content": display_msg})
            history.append({"role": "assistant", "content": ""})
            return "", history

        def bot_turn(history, file_path):
            history = history or []
            is_image = bool(file_path) and file_path.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            image_path = file_path if is_image else None
            file_text  = extract_file_text(file_path) if (file_path and not is_image) else None
            for partial in chat_with_ollama(history[:-1], image_path=image_path, file_text=file_text):
                history[-1]["content"] = partial
                yield history

        def reset_upload():
            return None, gr.update(visible=False)

        msg.submit(
            user_turn, [msg, chatbot, uploaded_file_state], [msg, chatbot], queue=False
        ).then(
            bot_turn, [chatbot, uploaded_file_state], chatbot
        ).then(
            reset_upload, None, [uploaded_file_state, file_badge]
        )

        send.click(
            user_turn, [msg, chatbot, uploaded_file_state], [msg, chatbot], queue=False
        ).then(
            bot_turn, [chatbot, uploaded_file_state], chatbot
        ).then(
            reset_upload, None, [uploaded_file_state, file_badge]
        )

        clear.click(lambda: [], None, chatbot, queue=False)

    return demo


def launch_demo(demo):
    base_port = 7860
    last_error = None
    for port in range(base_port, base_port + 10):
        try:
            demo.launch(
                server_name="127.0.0.1",
                server_port=port,
                share=False,
                show_error=True,
                theme=THEME,
                css=CSS,
            )
            return
        except OSError as error:
            last_error = error
            if "Cannot find empty port" not in str(error) and "only one usage of each socket address" not in str(error):
                raise
    raise last_error


if __name__ == "__main__":
    demo = build_ui()
    demo.queue()
    launch_demo(demo)
