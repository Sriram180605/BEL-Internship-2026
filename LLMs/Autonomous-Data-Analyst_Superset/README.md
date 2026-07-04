# Autonomous Data Analyst — BI-Backed Edition

A natural-language query assistant that sits on top of **Apache Superset** and **DuckDB**,
instead of replacing them. You ask a question in plain English; a local LLM pipeline turns
it into SQL and explains the result — but every query still runs, and is logged, inside a
real BI tool, not inside the AI.

> Full write-up with screenshots: [`AutonomousDataAnalyst_Superset_review.pdf`](./AutonomousDataAnalyst_Superset_review.pdf)

---

## Why this exists

An earlier version of this project had the LLM write **and execute** pandas code directly.
That's a black box: if the answer looks wrong there's no way to check why, and nothing
reusable is left behind for the next person to re-run or verify.

This version flips the division of labor:

| | LLM does everything (old) | BI tool does the analysis (this version) |
|---|---|---|
| **Who computes the answer** | LLM-generated pandas code, run in a local sandbox | **Apache Superset's SQL Lab**, against a real database |
| **Auditability** | Only by reading generated Python after the fact | Every query is logged in Superset's query history, can be re-run, saved as a chart, put on a dashboard |
| **Error surface** | Silent pandas bugs possible | Deterministic SQL engine (DuckDB) — same query, same answer, every time |
| **LLM's job** | Plan + write + execute + explain | **Only**: translate the question into SQL, and explain the result Superset returns |

## How it works

1. **Ingestion** — your CSV/Excel files are loaded and synced into a local DuckDB file. That
   file is registered as a **database connection inside Superset**, so Superset queries the
   real data directly, not a copy the LLM controls.
2. **Qwen2.5-Coder ("Hands")** — turns the natural-language question into one read-only SQL
   query. It never executes anything itself.
3. **Apache Superset ("The Analyst")** — the SQL is submitted to Superset's SQL Lab and run
   against DuckDB — the same code path as a human analyst typing a query by hand. It's
   logged there, and can be opened, verified, and turned into a chart by anyone on the team.
4. **Phi-4-mini-reasoning ("Explainer")** — reads only the result table Superset returns and
   writes a plain-language answer plus the business implication. It never sees raw data
   outside of what Superset actually returned.
5. **Self-correction** — if Superset rejects the SQL (syntax error, unknown column, etc.),
   the error is fed back to Qwen for up to 3 retries.
6. **Manual checkpoint by design** — even in the LLM-assisted path, a person still runs the
   generated SQL in SQL Lab and builds the chart. Nothing reaches a dashboard automatically.

A safety guard also rejects anything that isn't a single `SELECT` / `WITH` statement, so the
LLM layer can never write, alter, or drop data inside your BI tool.

**Multi-file folders:** every file becomes its own DuckDB table, named after the file
(`orders.csv` → table `orders`). When a question needs more than one file, Qwen sees every
relevant table's schema at once and writes the JOIN/UNION itself — Superset still runs it as
one auditable statement.

## Architecture at a glance

```
Data files (CSV/Excel)
        |
        v
     DuckDB  ── stores the data, runs every query
        |
        +-------------------+
        |                   |
   Write SQL manually   Ask a question (plain English)
   (Superset SQL Lab)          |
        |               LLM generates SQL + explanation
        |               (Qwen2.5-Coder + Phi-4-mini-reasoning)
        |                      |
        |               User runs the SQL manually (SQL Lab)
        |                      |
   Build chart manually   User builds the chart manually
        |                      |
        +----------+-----------+
                   |
                   v
        Output: dashboard chart
```

## Tech stack

- **Apache Superset** — BI platform, SQL Lab, charts, dashboards
- **DuckDB** — embedded analytical database (the single source of truth for both the
  notebook and Superset)
- **Ollama**, running two local models fully offline (no data leaves the machine, no
  per-query API cost):
  - `qwen2.5-coder:7b-instruct` — SQL generation
  - `phi4-mini-reasoning` — result explanation
- **Gradio** — the chat UI used to ask questions and upload files
- **Python / pandas** — data loading helpers

## Datasets used in the demo

- **Olist Brazilian E-Commerce** — ~100k orders (2016–2018) across orders, payments,
  customers, products, sellers, and reviews.
  [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Indian Weather Data** — daily weather and air quality observations across Indian
  locations (temperature, humidity, precipitation, wind, air quality).
  [kaggle.com/datasets/pratikjadhav05/indian-weather-data](https://www.kaggle.com/datasets/pratikjadhav05/indian-weather-data)

Neither dataset is included in this repo — download them from Kaggle and point the notebook
at your local copy (see below).

## Getting started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- Port `8088` free (Superset) and `7860` free (Gradio UI)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

This installs the notebook's dependencies, including `apache-superset` itself — Superset
runs as a local in-process Flask app (no Docker), on the same filesystem as the notebook, so
there's exactly one DuckDB file both sides read from.

### 2. Pull the models

```bash
ollama serve            # if not already running
ollama pull qwen2.5-coder:7b-instruct
ollama pull phi4-mini-reasoning
```

### 3. Run the notebook

Open `autonomous_data_analyst_bi_backed.ipynb` and run the cells in order. The notebook will:

- initialize and launch Superset in the background (first run creates a default `admin` /
  `admin` login — **change this if the machine is ever exposed beyond localhost**)
- launch the Gradio chat UI, printed as a local URL (e.g. `http://localhost:7860`)

### 4. Load your data and ask a question

Upload a folder of CSV/Excel files in the Gradio UI. Once loaded, ask a question in plain
English, then follow the on-screen link to open the generated SQL in Superset's SQL Lab, run
it, and build a chart.

## Repository structure

```
.
├── autonomous_data_analyst_bi_backed.ipynb   # main notebook — run this
├── AutonomousDataAnalyst_Superset_review.pdf # write-up with screenshots and walkthrough
├── requirements.txt
└── .gitignore
```

## Key takeaways

- Users can go from a raw file to a dashboard chart without writing SQL by hand.
- Every LLM-suggested answer is traceable back to a real, re-runnable Superset query —
  nothing is a black box.
- The pipeline correctly surfaced non-obvious relationships in the data (e.g., temperature
  vs. other weather metrics) with a query the user could verify themselves.
- Tested across two very different datasets: a small single-table dataset (Indian weather)
  and a larger multi-table dataset (Olist e-commerce).

## Notes & limitations

- Default Superset credentials (`admin` / `admin`) are for local, single-user use only —
  change `SUPERSET_PASSWORD` in the config cell before using this anywhere it might be
  network-reachable.
- SQL execution and chart-building are intentionally manual steps, even in the LLM-assisted
  path — this keeps a human checkpoint before anything reaches a dashboard.
- This project was built as part of an internship. See the accompanying PDF report for the
  full methodology and results.
