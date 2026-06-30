# BEL Internship — June 2026

Work completed during the internship, covering local LLM applications (chatbot, RAG, an
autonomous data-analyst agent) and a computer-vision fine-tuning project (YOLO on SAR
imagery).

## Repository structure

```
.
├── LLMs/
│   ├── Gemma chatbot/                 Local multimodal chatbot UI (Gradio + Ollama)
│   ├── RAG-Gemma/                     Retrieval-augmented QA over arXiv NLP papers
│   ├── Autonomous Data Analyst/       Dual-model agent that analyzes spreadsheets/CSVs
│   ├── Autonomous_Data_Analyst_Review.pdf
│   └── Chatbot_and_LLM_RAG_Internship_progress.pdf
└── YOLO FINE TUNING/
    ├── Sardet100k-YOLO.ipynb          YOLO fine-tuning on the SARDet-100K dataset
    └── Yolo_FineTuning_Report.pdf
```

Each project folder has its own `README.md` with setup and run instructions, and its own
`requirements.txt`.

## Common prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally, for the three `LLMs/`
  projects (`Gemma chatbot`, `RAG-Gemma`, `Autonomous Data Analyst`)
- A GPU (recommended) for `YOLO FINE TUNING`

## Quick start

```bash
git clone <this-repo-url>
cd BEL-Internship-June-2026

# pick a project and install its dependencies, e.g.
cd "LLMs/Gemma chatbot"
pip install -r requirements.txt
python app.py
```

See the per-project READMEs linked below for details:

- [LLMs/Gemma chatbot](./LLMs/Gemma%20chatbot/README.md)
- [LLMs/RAG-Gemma](./LLMs/RAG-Gemma/README.md)
- [LLMs/Autonomous Data Analyst](./LLMs/Autonomous%20Data%20Analyst/README.md)
- [YOLO FINE TUNING](./YOLO%20FINE%20TUNING/README.md)

## Reports

The PDFs in this repo (`Autonomous_Data_Analyst_Review.pdf`,
`Chatbot_and_LLM_RAG_Internship_progress.pdf`, `Yolo_FineTuning_Report.pdf`,
`LinksToDatasetsUsed.pdf`) document progress, evaluation, and dataset sources for the
corresponding projects.

## License

No license has been added yet. Add a `LICENSE` file before making the repo public if you
want to specify usage terms (e.g. MIT).
