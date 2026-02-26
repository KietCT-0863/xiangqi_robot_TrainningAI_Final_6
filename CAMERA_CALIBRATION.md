# 📷 Camera Calibration Guide
### Xiangqi Robot — Sideways / Tilted Camera Setup

---

## How It Works

Both `calibrate_tool.py` and `main.py` use `cv2.getPerspectiveTransform()` — a **full homography (projective) transform**.  
This means it mathematically corrects for **any** camera angle: overhead, sideways, diagonal, tilted. It does not require the camera to be perfectly straight.

The transform maps **4 pixel corners** you click on the camera image → **4 logical board corners** `(col, row)`:

| Click # | Physical Corner | Logical Grid |
|---------|----------------|--------------|
| 1 | Black Rook — Left  | `(0, 0)` |
| 2 | Black Rook — Right | `(8, 0)` |
| 3 | Red Rook — Right   | `(8, 9)` |
| 4 | Red Rook — Left    | `(0, 9)` |

The result is saved to `perspective.npy` and loaded by `main.py` at runtime.

---

## Step-by-Step: Calibrating a Tilted / Sideways Camera

### Step 1 — Fix the camera in its final position
> ⚠️ Do **not** move the camera after calibration. Even a small shift invalidates `perspective.npy`.

Mount the camera so the **entire board is visible** in frame. Angle does not matter as long as all 4 corners are clearly visible.

---

### Step 2 — Run `calibrate_tool.py`

```bash
python calibrate_tool.py
```

A live camera window named **CALIBRATE** will open.

---

### Step 3 — Click the 4 corners in exact order

```
1️⃣  Black Rook corner — LEFT   (top-left of board from player view)
2️⃣  Black Rook corner — RIGHT  (top-right of board from player view)
3️⃣  Red Rook corner  — RIGHT   (bottom-right of board from player view)
4️⃣  Red Rook corner  — LEFT    (bottom-left of board from player view)
```

> ✅ After clicking all 4, a **yellow grid** overlays the board. If the grid lines align with the physical board lines → calibration is correct.  
> ❌ If the grid is misaligned → press `R` to reset and click again.

---

### Step 4 — Save

Press **`S`** to save `perspective.npy`.  
Press **`R`** to reset and re-click.  
Press **`Q`** to quit without saving.

---

### Step 5 — Verify in `main.py`

Run `main.py`. The **Camera Monitor** window shows red dots drawn at each grid intersection.  
If the red dots land on the physical board intersections → calibration is working correctly.

---

## Tilted Camera: Parallax Fix

When the camera is **not directly overhead**, piece bounding boxes from YOLO will be offset because the **top of the piece** visually leans away from its base square. This is called **parallax error**.

The code in `main.py` (`detections_to_grid_occupancy`) already compensates:

```python
# Uses 85% down the bounding box (near the base of the piece), not the center
cy = y1 + (y2 - y1) * 0.85
```

### Tuning the parallax fix

| Camera angle | Recommended value |
|---|---|
| Nearly overhead (top-down) | `* 0.5` (center of box) |
| Moderate tilt (~30–45°) | `* 0.75` — `* 0.85` ← default |
| Steep tilt / sideways (>45°) | `* 0.90` — `* 1.0` (bottom of box) |

### Still wrong after tuning?

If pieces **consistently map one row too high**, uncomment this line in `detections_to_grid_occupancy` and tune the offset:

```python
# cy = cy + 10  ← uncomment and increase until pieces land on the correct row
```

---

## Resolution Must Match

Both files must use the same resolution. Currently set to:

| File | Resolution |
|---|---|
| `calibrate_tool.py` | `1920 × 1080` |
| `main.py` | `1920 × 1080` ✅ |

> ⚠️ If you change resolution in one file, change it in **both**, then **re-run `calibrate_tool.py`** to regenerate `perspective.npy`. The saved matrix is resolution-dependent.

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| Yellow grid is warped/skewed | Camera is tilted — **this is normal** | Check that grid lines still follow board lines |
| Pieces map to wrong column | Click order was wrong | Re-run `calibrate_tool.py`, click in correct order |
| Pieces map to wrong row | Parallax from camera tilt | Increase `* 0.85` toward `1.0`, or add `cy + N` offset |
| Grid looks correct but detections are off | Resolution mismatch | Ensure both files use `1920×1080` and re-calibrate |
| `perspective.npy` loads but board is shifted | Camera moved after calibration | Re-run calibration with camera in final position |

---

## Quick Reference

```
calibrate_tool.py keyboard shortcuts:
  R  →  Reset points (re-click)
  S  →  Save perspective.npy and exit
  Q  →  Quit without saving

main.py keyboard shortcuts (during game):
  V  →  Re-open calibration window (re-calibrate without restarting)
  Q  →  Close Camera Monitor window
```

---

## File Locations

| File | Purpose |
|---|---|
| `calibrate_tool.py` | Standalone calibration tool — run once per camera setup |
| `perspective.npy` | Saved perspective matrix — loaded by `main.py` at startup |
| `main.py` → `calibrate_perspective_camera()` | In-game re-calibration (press `V`) |
| `main.py` → `detections_to_grid_occupancy()` | Converts YOLO pixel detections → board grid using `perspective.npy` |

