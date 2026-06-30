# Autonomous Data Analyst (Dual-Model Agent)

A Gradio app that turns natural-language questions about your spreadsheets/CSVs into
pandas analysis, automatically — using two locally-hosted models in tandem via
[Ollama](https://ollama.com): one for reasoning/planning, one for code generation.

## How it works

- **Reasoning model** (`phi4-mini-reasoning`): classifies the question, plans the
  analysis steps, checks results, and explains the answer in plain language.
- **Coding model** (`qwen2.5-coder:7b-instruct`): writes the pandas code for each step.
- Generated code runs in a sandboxed execution environment against the uploaded
  table(s), and results (text, tables, and matplotlib/seaborn charts) are returned to
  the user.

Supported input formats: `.csv`, `.tsv`, `.xlsx`, `.xlsm`, `.xlsb`, `.xls` — including
multi-sheet Excel workbooks and multiple files/folders at once. CSV loading auto-detects
encoding and delimiter.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- Both models pulled:

  ```bash
  ollama pull phi4-mini-reasoning
  ollama pull qwen2.5-coder:7b-instruct
  ollama serve
  ```

## Setup

```bash
cd "LLMs/Autonomous Data Analyst"
pip install -r requirements.txt
```

## Run

Open `autonomous_data_analyst_dual_model.ipynb` and run all cells in order — the first
two cells install Python packages and pull the Ollama models for you (safe to re-run /
skip if already set up), then later cells launch a Gradio app for uploading files and
asking questions.

## Configuration

Key settings near the top of the notebook:

| Variable | Description | Default |
|---|---|---|
| `REASONING_MODEL` | Model used for planning/checking/explaining | `phi4-mini-reasoning` |
| `CODING_MODEL` | Model used for code generation | `qwen2.5-coder:7b-instruct` |
| `MAX_ROWS_CTX` / `MAX_COLS_CTX` | Rows/columns sampled into the model's context | `30` / `20` |
| `REASONING_CTX` / `CODING_CTX` | Context window size given to each model | `8192` / `12288` |
| `SUPPORTED_EXTENSIONS` | File types accepted for upload | csv/tsv/xlsx/xlsm/xlsb/xls |

## Reference material

- `LinksToDatasetsUsed.pdf` — datasets used while testing this notebook.
- `../Autonomous_Data_Analyst_Review.pdf` — write-up of the approach and evaluation.

## Notes

- Everything runs locally through Ollama; uploaded data is not sent to any external
  service.
