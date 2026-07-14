# Maritime RF-DETR Video Inference

RF-DETR-Small + ByteTrack video inference for marine object detection, with an
identity-smoothing layer so each tracked object keeps a stable class label
across the clip.

RF-DETR has no built-in `.track()` like Ultralytics YOLO, so this notebook
wires it up manually: `model.predict()` per frame → class-agnostic NMS →
`sv.ByteTrack` → identity smoothing.

## Why the identity layer

- **Class flicker** (e.g. `cargo` briefly misread as `tug`) is damped by
  accumulating per-class confidence with decay, then permanently **locking**
  the class after enough confirmed hits. A **size-growth unlock** re-opens
  classification if the box later grows a lot (partial/distant view →
  full view).
- **ID switching**, where ByteTrack assigns a new ID to a briefly-occluded
  object, is fixed by **re-linking** new IDs to recently lost identities
  based on position/size, and **coasting** the last box for a few frames so
  it doesn't flicker off-screen.

## Setup

```bash
pip install rfdetr supervision opencv-python numpy torch
```

## Usage

Open `Maritime_Video_Inference_RFDETR.ipynb` and set, in the first code cell:

- `MODEL_PATH` — your fine-tuned RF-DETR checkpoint (e.g. `checkpoint_best_ema.pth`)
- `VIDEO_PATH` / `OUTPUT_PATH` — input/output video paths
- `CLASS_NAMES` — class names in the **exact order used during training**
  (RF-DETR checkpoints don't store names the way Ultralytics `.pt` files do)
- `DEVICE` — `"cpu"` or `"cuda"`

Then run all cells. All detection, tracking, and smoothing thresholds
(`CONF_THRESH`, `LOCK_AFTER_HITS`, `RELINK_MAX_*`, etc.) are defined as
constants in the same cell.

## Output

Annotated copy of the input video — solid boxes for confirmed identities,
a differently-shaded `(coasting)` box for identities briefly undetected.
