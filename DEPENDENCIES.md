# DEPENDENCIES & LIBRARIES DOCUMENTATION

## Project: Xiangqi Robot Training AI (FR3 Cobot Arm)

This is a comprehensive Chinese Chess (Xiangqi) playing robot system using a Fairino FR3 cobot arm with computer vision and AI.

---

## EXTERNAL DEPENDENCIES (Pip Packages)

### 1. **numpy** (>= 1.21.0)
- **Purpose**: Numerical computing and array operations
- **Used in**:
  - Matrix transformations for perspective calibration (main.py)
  - Board state manipulations (ai.py, xiangqi.py)
  - Calculation arrays for YOLO detections
- **Why needed**: Essential for scientific computing

### 2. **opencv-python** (>= 4.5.0)
- **Purpose**: Computer vision and image processing
- **Used in**:
  - Camera frame capture and processing (main.py)
  - Perspective transformation for board calibration
  - Drawing debug grids on camera output
  - Piece detection coordinate conversion
- **Why needed**: Critical for real-time camera vision system

### 3. **pygame** (>= 2.1.0)
- **Purpose**: Game interface rendering and input handling
- **Used in**:
  - GUI window creation (main.py)
  - Drawing the game board and pieces
  - Rendering Chinese chess characters (Traditional: 帥, 將, etc.)
  - Mouse input handling for dry-run mode
  - Game state display (captured pieces, turn indicator)
- **Why needed**: Provides complete game UI framework

### 4. **ultralytics** (>= 8.0.0)
- **Purpose**: YOLOv8 object detection framework
- **Used in**:
  - Real-time piece detection from camera feed (main.py)
  - Loading pre-trained model: `models_chinesechess1/content/runs/detect/train/weights/best.pt`
  - Board state recognition from camera
- **Why needed**: AI-powered piece detection from visual input

### 5. **torch** (>= 1.9.0)
- **Purpose**: PyTorch deep learning framework
- **Used by**: ultralytics (YOLO) - handles neural network inference
- **Why needed**: Required dependency for ultralytics

### 6. **torchvision** (>= 0.10.0)
- **Purpose**: PyTorch computer vision utilities
- **Used by**: YOLO model processing
- **Why needed**: Companion library for torch

### 7. **Cython** (>= 0.29.0)
- **Purpose**: C extension module compilation
- **Used for**: Building `robot_sdk_core.pyd` from `robot_sdk_core.c`
- **How to compile**:
  ```powershell
  python setup.py build_ext --inplace
  ```
- **Why needed**: Robot SDK requires compiled C extension for performance and robot hardware communication

---

## INTERNAL MODULES (Local Python Files)

### Core Game Engine
- **xiangqi.py**: Game rules, board management, move validation
- **config.py**: Configuration (IP, coordinates, speeds, DRY_RUN mode)
- **ai.py**: Minimax AI engine with alpha-beta pruning
- **ai_book.py**: Opening book database and machine learning
- **robot.py**: FR5Robot class for Fairino arm control
- **robot_sdk_core.c/.py**: Low-level robot hardware SDK (compiled to .pyd)

### User Interface & Audio
- **main.py**: Main game loop, camera integration, UI rendering
- **sound_player.py**: Audio playback for moves and captures

---

## HARDWARE-SPECIFIC DEPENDENCIES

### 1. **Fairino FR3 Cobot Arm**
- **SDK**: `robot_sdk_core` (compiled from C)
- **Connection**: Ethernet, IP-based (configured in config.py)
- **Purpose**: Physical piece manipulation

### 2. **Camera (USB Webcam)**
- **Library**: OpenCV
- **INDEX**: Configurable via `VIDEO_INDEX` environment variable
- **Purpose**: Real-time board state detection

### 3. **Gripper/Knepper**
- **Control**: Via robot SDK
- **Configuration**: GRIPPER_OPEN/GRIPPER_CLOSE in config.py

### 4. **Sound System**
- **Library**: pygame.mixer
- **Audio files**: Located in `/sounds` directory
- **Format**: Voice captures for piece movements

---

## INSTALLATION GUIDE

### Step 1: Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Compile Robot SDK (Important!)
```powershell
python setup.py build_ext --inplace
```

This creates `robot_sdk_core.cp312-win_amd64.pyd` (or similar for your Python version).

### Step 4: Verify Installation
```powershell
python -c "import robot_sdk_core; print('✅ Robot SDK OK')"
python -c "import torch; print('✅ PyTorch OK')"
python -c "from ultralytics import YOLO; print('✅ YOLO OK')"
```

---

## WHAT HAPPENS IF VENV IS REMOVED?

**Short Answer**: ❌ **NO, it will NOT work**

### Why?
1. **Missing compiled extensions**: `robot_sdk_core.pyd` is built inside venv
2. **Missing all pip packages**: numpy, opencv, torch, etc.
3. **Import errors**: Python cannot find any dependencies

### What To Do:
1. Recreate the virtual environment
2. Re-run: `pip install -r requirements.txt`
3. Re-compile: `python setup.py build_ext --inplace`

---

## WHAT ABOUT YOUR PROJECT AFTER REMOVING VENV?

**Short Answer**: ❌ **Will it still work? NO**

The `.py` files themselves are fine, but:
- `main.py` imports: numpy, cv2, pygame, YOLO → **CRASH**
- `robot.py` imports: robot_sdk_core → **CRASH**
- Camera won't work, AI won't run, robot won't connect

### Recovery:
Simply recreate venv + reinstall. Your source code is unaffected.

---

## DEPENDENCY TREE

```
main.py
├── numpy (camera transforms, board arrays)
├── cv2 (camera, perspective transform)
├── pygame (GUI, game render)
├── ultralytics.YOLO (piece detection)
│   └── torch (neural network)
│       └── torchvision (image ops)
├── config (configuration)
├── xiangqi (game rules)
├── ai (chess AI engine)
├── ai_book (opening book & learning)
├── sound_player
│   └── pygame (audio playback)
└── robot.FR5Robot
    └── robot_sdk_core (C extension → requires Cython to build)
```

---

## OPTIONAL DEPENDENCIES FOR DEVELOPMENT

If you want to extend or debug:

```bash
pip install pytest pytest-cov          # Testing
pip install black flake8 mypy          # Code quality
pip install jupyter notebook           # Interactive development
pip install debugpy                    # Python debugger
```

---

## ENVIRONMENT VARIABLES

Set in your shell before running:
```powershell
$env:VIDEO_INDEX = "1"           # Camera device index (default: 1)
$env:PYTHONPATH = "."            # Ensure current dir is in path
```

Or in Python:
```python
import os
os.environ["VIDEO_INDEX"] = "1"
os.environ["DRY_RUN"] = "True"
```

---

## TROUBLESHOOTING

### ❌ "ModuleNotFoundError: No module named 'robot_sdk_core'"
**Fix**: Run `python setup.py build_ext --inplace`

### ❌ "ModuleNotFoundError: No module named 'ultralytics'"
**Fix**: Run `pip install ultralytics`

### ❌ "Cannot load YOLO model: best.pt not found"
**Fix**: Check model path in main.py (line ~135):
```python
MODEL_PATH = r"D:\xiangqi_robot_TrainningAI_Final_6\models_chinesechess1\content\runs\detect\train\weights\best.pt"
```

### ❌ "Robot connection failed"
**Fix**: Check `config.ROBOT_IP` and physical connection. Test with `DRY_RUN = True` first.

### ❌ "Camera not opening"
**Fix**: Check `VIDEO_INDEX` environment variable (may be 0 or 1 depending on system)

---

## PRODUCTION VS DEVELOPMENT

### DRY_RUN Mode (Testing without hardware)
Set in `config.py`:
```python
DRY_RUN = True  # Uses mouse for moves, no camera, no robot
```

### Real Mode (With hardware)
```python
DRY_RUN = False  # Uses camera for detection, controls real robot
```

---

## VERSION COMPATIBILITY

**Tested with:**
- Python 3.10, 3.11, 3.12, 3.13 (evidenced by pycache files)
- Windows 10/11
- PyTorch 1.9-2.0+
- OpenCV 4.5-4.9+

---

## SUMMARY TABLE

| Category | Package | Version | Purpose |
|----------|---------|---------|---------|
| **Scientific** | numpy | >=1.21 | Array operations |
| **Vision** | opencv-python | >=4.5 | Camera & perspective |
| **GUI** | pygame | >=2.1 | Game rendering |
| **AI/ML** | ultralytics | >=8.0 | YOLO detection |
| | torch | >=1.9 | Neural nets |
| | torchvision | >=0.10 | Vision utils |
| **Build** | Cython | >=0.29 | Compile robot SDK |

---

**Created**: January 2026
**Project**: Xiangqi Robot Training AI for Fairino FR3 Cobot

