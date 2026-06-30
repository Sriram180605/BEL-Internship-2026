# YOLO Fine-Tuning on SARDet-100K

Fine-tunes a [YOLO](https://github.com/ultralytics/ultralytics) object detector on the
[SARDet-100K](https://www.kaggle.com/datasets/greatbird/sardet-100k) SAR (Synthetic
Aperture Radar) imagery dataset, with evaluation and ground-truth-vs-prediction
visualizations.

## ⚠️ Designed for Kaggle

This notebook (`Sardet100k-YOLO.ipynb`) is written to run on **Kaggle Notebooks** and
expects:

- A GPU accelerator (T4 x2 or better) — the notebook asserts CUDA is available.
- The `greatbird/sardet-100k` dataset attached as a Kaggle input (mounted at
  `/kaggle/input/...`).
- Output is written to `/kaggle/working/results/`.

To run it elsewhere (local machine, Colab, etc.), update:

- `WORK_DIR` / `RESULTS_DIR` to a local output directory.
- `DATA_ROOT` resolution (`find_sardet_root`) to point at wherever you've downloaded
  SARDet-100K locally — the dataset isn't included in this repo (see below).

## Dataset

This repo does **not** include the SARDet-100K dataset (it's large and license-bound).
Download it from Kaggle: <https://www.kaggle.com/datasets/greatbird/sardet-100k>, or
attach it as a Kaggle input named `greatbird/sardet-100k` if running on Kaggle.

## Prerequisites

- Python 3.10+
- A CUDA-capable GPU
- PyTorch with CUDA support installed for your environment (see
  [pytorch.org](https://pytorch.org/get-started/locally/) — not pinned in
  `requirements.txt` since the right build depends on your CUDA version)

## Setup

```bash
cd "YOLO FINE TUNING"
pip install -r requirements.txt
```

## Run

Open `Sardet100k-YOLO.ipynb` and run all cells in order. The notebook:

1. Installs/pins `seaborn` and `ultralytics`.
2. Verifies GPU availability.
3. Locates the SARDet-100K dataset under the input directory.
4. Converts annotations, builds the YOLO dataset config, and trains.
5. Evaluates the fine-tuned model and saves metrics, plots, and
   ground-truth-vs-prediction panels to `results/`.

## Outputs

Training results, weights, and visualizations are written under `results/` (and
`runs/` from Ultralytics) — both are excluded from version control via `.gitignore`
since they're large generated artifacts. See `Yolo_FineTuning_Report.pdf` for a
write-up of the methodology and results.
