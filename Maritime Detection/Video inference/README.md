# Maritime Video Inference

Runs the fine-tuned YOLO11s maritime detector (`best.pt`) on a video, producing an annotated output with stable, flicker-resistant class labels per tracked vessel.

## What it does

- Loads your model, opens the video, sets up the output writer
- Runs YOLO tracking frame-by-frame (with a custom tracker config that holds onto objects longer through occlusions)
- Gives each tracked object a persistent "identity" instead of trusting raw tracker IDs
- If the tracker loses an object and gives it a new ID, re-links it to its old identity (same position/size) so history isn't lost
- Builds up confidence-weighted "votes" for each object's class over time, with older votes slowly fading
- Only switches the displayed label if the new class clearly outvotes the old one
- Once an object has been seen enough times, locks its class permanently — nothing can change it after that
- If an object briefly isn't detected, keeps drawing its last box for a few frames instead of it vanishing
- Fully forgets an object if it's gone too long

## Restrictions / limits imposed

- Detection confidence must be ≥ 0.40 to count
- Needs 5 detections before showing any label
- Needs 20 detections before locking the class forever
- A new class needs 2× the vote score to override the current one (pre-lock)
- Old evidence fades by 2% each frame
- Objects can be "lost" up to 45 frames and still be re-linked
- Re-linking only allowed if position moved < 80px and size changed < 1.6×
- Missing boxes are still drawn for up to 8 frames ("coasting")
- Tracker itself is set to tolerate longer gaps (60 frames) before dropping a track

**Overall tradeoff:** favors staying consistent over being quick to correct itself.

## Usage

1. Update the paths at the top of the notebook's code cell:
   - `MODEL_PATH` — path to your trained `best.pt`
   - `VIDEO_PATH` — input video to run inference on
   - `OUTPUT_PATH` — where the annotated video will be saved
   - `TRACKER_CFG_PATH` — where the auto-generated tracker config gets written
2. Run the notebook. It will:
   - Write a custom ByteTrack config (`bytetrack_stable.yaml`)
   - Stream through the video frame-by-frame, running detection + tracking
   - Write the annotated output video to `OUTPUT_PATH`

## Requirements

- `ultralytics`
- `opencv-python`
- `numpy`
- `pyyaml`

## Tuning

If labels are still flickering or locking in too early/late, the key constants at the top of the notebook can be adjusted:

| Parameter | Default | Effect |
|---|---|---|
| `conf` | 0.40 | Detector confidence floor |
| `MIN_HITS_TO_DISPLAY` | 5 | Detections needed before a label is shown |
| `SWITCH_MARGIN` | 2.0 | How dominant a new class's vote must be to override the current one |
| `DECAY` | 0.98 | Per-frame decay applied to accumulated class evidence |
| `LOCK_AFTER_HITS` | 20 | Detections needed before an identity's class is frozen permanently |
| `RELINK_MAX_FRAMES_GONE` | 45 | Max frames an identity can be missing and still be re-linked |
| `RELINK_MAX_CENTER_DIST` | 80 | Max pixel movement to count as the same object when re-linking |
| `RELINK_MAX_SIZE_RATIO` | 1.6 | Max box-area change to count as the same object when re-linking |
| `COAST_MAX_FRAMES` | 8 | How many frames a missing box is still drawn before disappearing |
| `track_buffer` (tracker config) | 60 | Frames ByteTrack keeps a lost track alive before dropping it |
