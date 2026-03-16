# =============================================================================
# === FILE: config.py (CẤU HÌNH TOÀN HỆ THỐNG) ===
# =============================================================================

# --- THÔNG SỐ ROBOT BÀN CỜ (HARDCODED TOẠ ĐỘ TOÁN HỌC) ---
# Tọa độ gốc (Điểm R1 - tương ứng Xe Đen Trái, ô col=0, row=0)
# Tọa độ này sẽ được hệ thống Robot tự động ghi đè lúc khởi động bằng lệnh GetRobotTeachingPoint("R1")
BOARD_ORIGIN_X = 200.0  
BOARD_ORIGIN_Y = -100.0 

# Offset điều chỉnh (mm) - Dùng để tinh chỉnh vị trí gắp
# Nếu robot gắp lệch, điều chỉnh các giá trị này:
# - OFFSET_X: Dương = dịch xuống dưới (về phía row=9), Âm = dịch lên trên (về phía row=0)
# - OFFSET_Y: Dương = dịch sang phải (về phía col=8), Âm = dịch sang trái (về phía col=0)
OFFSET_X = 5.0   # Robot gắp lệch lên trên 5mm → cần dịch xuống 5mm
OFFSET_Y = 0.0   # Không lệch ngang

# Chiều hướng di chuyển so với gốc R1 (1 hoặc -1)
# LƯU Ý: Hệ tọa độ robot: X=dọc (row), Y=ngang (col)
# 1: row tăng thì X tăng, col tăng thì Y tăng
ROBOT_DIR_X = 1  
ROBOT_DIR_Y = 1  

# Kích thước vật lý từng ô bàn cờ (mm)
CELL_SIZE_X = 40.75  # 326mm chia cho 8 khoảng cột (ngang)
CELL_SIZE_Y = 41.00  # 370mm chia cho 9 khoảng hàng (dọc)
RIVER_GAP_Y = 1.00   # Bù thêm 1mm khe hở của con Sông (Nằm giữa row 4 và row 5)

# Tọa độ bãi chứa quân bị ăn (X, Y, Z)
CAPTURE_BIN_X = -226.123
CAPTURE_BIN_Y = 225.024
CAPTURE_BIN_Z = 291.68  # [QUAN TRỌNG] Độ cao khi thả quân vào thùng

# Độ cao an toàn (mm)
SAFE_Z  = 270.0    # Độ cao an toàn khi di chuyển giữa các ô (tăng lên để tránh hất quân)
EXTRA_SAFE_Z = 310.0  # Độ cao cực an toàn khi di chuyển xa (tránh đường cong quét qua nhiều quân)
PICK_Z  = 180.0   # Hạ xuống gắp (Đã nâng lên để tránh đập bàn, hạ từ từ)
PLACE_Z = 190.0   # Hạ xuống đặt

# Cấu hình Kẹp (Gripper) - Tùy chỉnh theo loại van của bạn
GRIPPER_CLOSE = 1
GRIPPER_OPEN = 0
MOVE_SPEED = 50

# Góc xoay của đầu Robot (Rx, Ry, Rz)
ROTATION = [89.658,-0.394, 174.148] 

# Kết nối Robot
ROBOT_IP = "192.168.58.2"
DRY_RUN = False # Đổi thành True nếu muốn test code mà không cần bật Robot

# Camera index (0 = built-in webcam, 1 = USB cam, etc.)
# main.py will auto-try 0, 1, 2 if this index fails.
VIDEO_SOURCE = 1

# --- THÔNG SỐ AI ---
AI_THINK_TIME = 10  # Time per move in seconds — AI gets 10s after subtracting TIME_BUFFER (0.5)
AI_DEPTH = 30          # Độ sâu mặc định (sẽ bị ghi đè bởi logic tự động)

# --- AI ENGINE CONFIGURATION ---
ENGINE_TYPE = "HYBRID" # "HYPrefixBRID" (Ưu tiên Cloud), "CLOUD" (Chỉ Cloud), "LOCAL" (Chỉ Local)
CLOUD_API_URL = "https://tuongkydaisu.com/api/engine/bestmove"
CLOUD_TIMEOUT_SEC = 5

# --- SIMULATION API CONFIGURATION ---
SIMULATION_API_URL = "https://tuongkydaisu.com"
SIMULATION_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzaW11bGF0aW9uMDAxIiwicm9sZSI6IlNJTVVMQVRJT04iLCJ0b2tlbklkIjoiMTlkYjRjMDEtNjk4My00MTU5LTllNzYtODk0NDU5YjJhMjM5IiwiaWF0IjoxNzczMTI3MTE5LCJleHAiOjE4MDQ2NjMxMTl9.cHQEzHS-SqrZqUZ9FRcJgUE_BzyxZ60iiy7xYzZPQOo" # Liên hệ admin để lấy Token cấp cho app. Điền vào đây.

# --- PIKAFISH ENGINE ---
# Hướng dẫn tải cho người mới clone repo:
# 1. Tải bản mới nhất từ: https://github.com/official-pikafish/Pikafish/releases/tag/Pikafish-2026-01-02
# 2. Giải nén vào thư mục `pikafish/` (giữ nguyên cấu trúc chứa thư mục con `Windows/`)
# 3. Tải file `pikafish.nnue` từ https://pikafish.org/api/nnue/download/latest và bỏ nó chung vào thư mục `pikafish/`
import os as _os
_BASE_DIR      = _os.path.dirname(_os.path.abspath(__file__))
_PIKAFISH_DIR = _os.path.join(_BASE_DIR, 'pikafish')
PIKAFISH_EXE  = _os.path.join(_PIKAFISH_DIR, 'Windows', 'pikafish-avx2.exe')
PIKAFISH_NNUE = _os.path.join(_PIKAFISH_DIR, 'pikafish.nnue')
PIKAFISH_THINK_MS = 3000  # Thời gian suy nghĩ mỗi nước (milliseconds)

# Tọa độ về nhà (Home) để né Camera
IDLE_X = -72.027
IDLE_Y = 200.248
IDLE_Z = 278.586  
