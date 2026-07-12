
# BEL Internship — Summer 2026

Work completed during the internship, covering local LLM applications (chatbot, RAG, and two iterations of an autonomous data-analyst agent) and computer-vision fine-tuning projects (YOLO on SAR imagery and maritime object detection)[cite: 5].

## Repository structure

```text
.
├── LLMs/
│   ├── Gemma chatbot/                           Local multimodal chatbot UI (Gradio + Ollama)[cite: 5]
│   ├── RAG-Gemma/                                Retrieval-augmented QA over arXiv NLP papers[cite: 5]
│   ├── Autonomous Data Analyst/                  Dual-model agent that analyzes spreadsheets/CSVs[cite: 5]
│   ├── Autonomous-Data-Analyst_Superset/         BI-backed version of the same agent — see note below[cite: 5]
│   ├── Autonomous_Data_Analyst_Review.pdf[cite: 5]
│   ├── AutonomousDataAnalyst_Superset_review.pdf[cite: 5]
│   └── Chatbot_and_LLM_RAG_Internship_progress.pdf[cite: 5]
├── Maritime Detection/
│   ├── Maritime_Detection_YOLO11s.ipynb          YOLO11s partial fine-tuning on maritime images[cite: 5]
│   └── MaritimeDetection_review.pdf              Maritime detection evaluation and metrics[cite: 5]
└── YOLO FINE TUNING/
    ├── Sardet100k-YOLO.ipynb                     YOLO fine-tuning on the SARDet-100K dataset[cite: 5]
    └── Yolo_FineTuning_Report.pdf[cite: 5]

```

Each project folder has its own `README.md` with setup and run instructions, and its own `requirements.txt`.

### A note on the two Autonomous Data Analyst folders

* **`Autonomous Data Analyst/`** — the original version. The LLM both writes and executes pandas code directly against the data.


* **`Autonomous-Data-Analyst_Superset/`** — a follow-up that changes who does the computation. The LLM only translates a question into SQL and explains the result; **Apache Superset + DuckDB** actually run every query, so every answer is logged, re-runnable, and independently verifiable instead of being a one-off chat response. See that folder's `README.md` and `AutonomousDataAnalyst_Superset_review.pdf` for the full writeup.



## Common prerequisites

* Python 3.10+


* [Ollama](https://www.google.com/search?q=https://ollama.com) installed and running locally, for the `LLMs/` projects (`Gemma chatbot`, `RAG-Gemma`, `Autonomous Data Analyst`, `Autonomous-Data-Analyst_Superset`)


* For `Autonomous-Data-Analyst_Superset` specifically: port `8088` free (Apache Superset) and port `7860` free (Gradio UI)


* A GPU (recommended) for `YOLO FINE TUNING` and `Maritime Detection`


## Quick start

```bash
git clone <this-repo-url>
cd BEL-Internship-2026
# pick a project and install its dependencies, e.g.
cd "LLMs/Gemma chatbot"
pip install -r requirements.txt
python app.py

```

See the per-project READMEs linked below for details:

* [LLMs/Gemma chatbot](https://www.google.com/search?q=./LLMs/Gemma%2520chatbot/README.md)

* [LLMs/RAG-Gemma](https://www.google.com/search?q=./LLMs/RAG-Gemma/README.md)

* [LLMs/Autonomous Data Analyst](https://www.google.com/search?q=./LLMs/Autonomous%2520Data%2520Analyst/README.md)

* [LLMs/Autonomous-Data-Analyst_Superset](https://www.google.com/search?q=./LLMs/Autonomous-Data-Analyst_Superset/README.md)

* [Maritime Detection](https://www.google.com/search?q=./Maritime%2520Detection/README.md)

* [YOLO FINE TUNING](https://www.google.com/search?q=./YOLO%2520FINE%2520TUNING/README.md)


## Reports

The PDFs in this repo document progress, evaluation, and dataset sources for the corresponding projects:

* `Autonomous_Data_Analyst_Review.pdf` — write-up for the original pandas-sandbox agent


* `AutonomousDataAnalyst_Superset_review.pdf` — write-up for the Superset/DuckDB-backed agent


* `Chatbot_and_LLM_RAG_Internship_progress.pdf` — chatbot and RAG progress


* `MaritimeDetection_review.pdf` — YOLO11s fine-tuning results on maritime dataset


* `Yolo_FineTuning_Report.pdf` — YOLO fine-tuning results


* `LinksToDatasetsUsed.pdf` — dataset sources across all projects



## License

No license has been added yet. Add a `LICENSE` file before making the repo public if you want to specify usage terms (e.g. MIT).

```

```
