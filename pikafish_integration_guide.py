# =============================================================================
# HOW TO ADD PIKAFISH TO main.py  —  DIFF-GUIDE
# =============================================================================
# Only 3 sections of main.py need changing. Everything else stays identical.
# =============================================================================

# ─── STEP 1: Add to config.py ─────────────────────────────────────────────────
# Open config.py and add these two lines anywhere:

PIKAFISH_EXE  = r"pikafish\pikafish-windows-x86-64-avx2.exe"   # path to the .exe
PIKAFISH_NNUE = r"pikafish\pikafish.nnue"                       # path to .nnue file
PIKAFISH_THINK_MS = 3000   # milliseconds Pikafish is allowed to think per move

# ─── STEP 2: Change imports at the top of main.py ────────────────────────────
# REMOVE this line:
#   import ai
#
# ADD these lines instead:
#   from pikafish_engine import PikafishEngine

# ─── STEP 3: Start engine after robot init (around line 110 in main.py) ───────
# ADD after the robot block:
#
#   engine = PikafishEngine(config.PIKAFISH_EXE)
#   engine.start(nnue_path=config.PIKAFISH_NNUE)

# ─── STEP 4: Replace the AI call inside _ai_worker() (around line 670) ────────
# BEFORE:
#   ai_result = ai.pick_best_move(board_snapshot, "b")
#
# AFTER:
#   ai_result = engine.pick_best_move(board_snapshot, "b", movetime_ms=config.PIKAFISH_THINK_MS)

# ─── STEP 5: Shut down engine cleanly at program exit (last lines of main.py) ─
# ADD before pygame.quit():
#   engine.stop()

# =============================================================================
# THAT'S IT. The rest of main.py is unchanged because engine.pick_best_move()
# returns the exact same format as ai.pick_best_move():
#   ((src_col, src_row), (dst_col, dst_row))
# =============================================================================
