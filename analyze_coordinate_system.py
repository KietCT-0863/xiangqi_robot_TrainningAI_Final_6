# Script phân tích hệ tọa độ robot
# Giúp hiểu rõ trục X và Y nằm ở đâu

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

print("="*80)
print("PHÂN TÍCH HỆ TỌA ĐỘ ROBOT FR5")
print("="*80)

# Giả sử BOARD_ORIGIN từ log thực tế
ORIGIN_X = -191.8  # Từ log của bạn
ORIGIN_Y = 255.2   # Từ log của bạn

print(f"\n📍 BOARD_ORIGIN (R1 - Xe Đen Trái, góc trái-trên):")
print(f"   X = {ORIGIN_X:.1f}mm")
print(f"   Y = {ORIGIN_Y:.1f}mm")

print(f"\n📏 KÍCH THƯỚC BÀN CỜ:")
print(f"   Ngang (9 cột, 8 khoảng): {config.CELL_SIZE_X}mm × 8 = {config.CELL_SIZE_X * 8:.1f}mm")
print(f"   Dọc (10 hàng, 9 khoảng): {config.CELL_SIZE_Y}mm × 9 = {config.CELL_SIZE_Y * 9:.1f}mm")
print(f"   Khe sông: {config.RIVER_GAP_Y}mm")

print("\n" + "="*80)
print("TỌA ĐỘ 4 GÓC BÀN CỜ (Dự đoán)")
print("="*80)

def calc_pose(col, row):
    """Tính tọa độ theo công thức MỚI (đã hoán đổi)"""
    delta_x = row * config.CELL_SIZE_Y
    delta_y = col * config.CELL_SIZE_X
    
    if row >= 5:
        delta_x += config.RIVER_GAP_Y
    
    x = ORIGIN_X + (delta_x * config.ROBOT_DIR_X)
    y = ORIGIN_Y + (delta_y * config.ROBOT_DIR_Y)
    
    return x, y

corners = [
    (0, 0, "R1 - Xe Đen Trái (góc trái-trên)"),
    (8, 0, "R2 - Xe Đen Phải (góc phải-trên)"),
    (8, 9, "R3 - Xe Đỏ Phải (góc phải-dưới)"),
    (0, 9, "R4 - Xe Đỏ Trái (góc trái-dưới)"),
]

print("\n┌─────────────────────────────┬──────────┬────────────┬────────────┐")
print("│ Vị trí                      │ (col,row)│ X (mm)     │ Y (mm)     │")
print("├─────────────────────────────┼──────────┼────────────┼────────────┤")

for col, row, desc in corners:
    x, y = calc_pose(col, row)
    print(f"│ {desc:<27s} │ ({col},{row})    │ {x:>10.1f} │ {y:>10.1f} │")

print("└─────────────────────────────┴──────────┴────────────┴────────────┘")

print("\n" + "="*80)
print("PHÂN TÍCH HƯỚNG TRỤC TỌA ĐỘ")
print("="*80)

# Phân tích từ R1 đến R2 (di chuyển sang phải)
x1, y1 = calc_pose(0, 0)  # R1
x2, y2 = calc_pose(8, 0)  # R2
print(f"\n🔹 Từ R1 (0,0) đến R2 (8,0) - Di chuyển 8 cột sang PHẢI:")
print(f"   R1: X={x1:.1f}, Y={y1:.1f}")
print(f"   R2: X={x2:.1f}, Y={y2:.1f}")
print(f"   ΔX = {x2-x1:.1f}mm, ΔY = {y2-y1:.1f}mm")
if abs(x2-x1) < 1:
    print(f"   → X không đổi → Trục Y đi NGANG (trái-phải)")
else:
    print(f"   → X thay đổi → Trục X đi NGANG (trái-phải)")

# Phân tích từ R1 đến R4 (di chuyển xuống dưới)
x1, y1 = calc_pose(0, 0)  # R1
x4, y4 = calc_pose(0, 9)  # R4
print(f"\n🔹 Từ R1 (0,0) đến R4 (0,9) - Di chuyển 9 hàng xuống DƯỚI:")
print(f"   R1: X={x1:.1f}, Y={y1:.1f}")
print(f"   R4: X={x4:.1f}, Y={y4:.1f}")
print(f"   ΔX = {x4-x1:.1f}mm, ΔY = {y4-y1:.1f}mm")
if abs(y4-y1) < 1:
    print(f"   → Y không đổi → Trục X đi DỌC (trên-dưới)")
else:
    print(f"   → Y thay đổi → Trục Y đi DỌC (trên-dưới)")

print("\n" + "="*80)
print("KẾT LUẬN VỀ HỆ TỌA ĐỘ")
print("="*80)

delta_x_horizontal = x2 - x1  # R1 → R2 (ngang)
delta_y_horizontal = y2 - y1
delta_x_vertical = x4 - x1    # R1 → R4 (dọc)
delta_y_vertical = y4 - y1

print(f"\n📊 Phân tích:")
print(f"   Di chuyển NGANG (trái→phải): ΔX={delta_x_horizontal:.1f}, ΔY={delta_y_horizontal:.1f}")
print(f"   Di chuyển DỌC (trên→dưới):   ΔX={delta_x_vertical:.1f}, ΔY={delta_y_vertical:.1f}")

if abs(delta_y_horizontal) > abs(delta_x_horizontal):
    print(f"\n✅ Trục Y đi NGANG (trái-phải)")
    print(f"   - Y tăng = đi sang phải")
    print(f"   - Y giảm = đi sang trái")
else:
    print(f"\n✅ Trục X đi NGANG (trái-phải)")
    print(f"   - X tăng = đi sang phải")
    print(f"   - X giảm = đi sang trái")

if abs(delta_x_vertical) > abs(delta_y_vertical):
    print(f"\n✅ Trục X đi DỌC (trên-dưới)")
    print(f"   - X tăng = đi xuống dưới")
    print(f"   - X giảm = đi lên trên")
else:
    print(f"\n✅ Trục Y đi DỌC (trên-dưới)")
    print(f"   - Y tăng = đi xuống dưới")
    print(f"   - Y giảm = đi lên trên")

print("\n" + "="*80)
print("SƠ ĐỒ HỆ TỌA ĐỘ (Nhìn từ trên xuống)")
print("="*80)

print("""
        Quân ĐEN (row=0)
    ┌─────────────────────┐
    │ R1              R2  │
    │ (0,0)          (8,0)│
    │                     │
    │                     │  
    │    BÀN CỜ TƯỚNG    │
    │                     │
    │                     │
    │ R4              R3  │
    │ (0,9)          (8,9)│
    └─────────────────────┘
        Quân ĐỎ (row=9)

Với hệ tọa độ hiện tại:
""")

if abs(delta_y_horizontal) > abs(delta_x_horizontal):
    print("  Y →  (Trục Y đi ngang, trái sang phải)")
    print("  ↓")
    print("  X    (Trục X đi dọc, trên xuống dưới)")
else:
    print("  X →  (Trục X đi ngang, trái sang phải)")
    print("  ↓")
    print("  Y    (Trục Y đi dọc, trên xuống dưới)")

print("\n" + "="*80)
print("HƯỚNG DẪN KIỂM TRA")
print("="*80)
print("""
Để xác nhận hệ tọa độ đúng:

1. Chạy script này: python analyze_coordinate_system.py
2. So sánh tọa độ 4 góc dự đoán với tọa độ thực tế từ robot
3. Nếu sai, cần điều chỉnh:
   - ROBOT_DIR_X hoặc ROBOT_DIR_Y (đổi dấu 1 → -1)
   - Hoặc hoán đổi lại công thức trong board_to_pose()

4. Test bằng cách:
   - Di chuyển robot đến (0,0) → kiểm tra có đúng R1 không
   - Di chuyển robot đến (8,0) → kiểm tra có đúng R2 không
   - Di chuyển robot đến (0,9) → kiểm tra có đúng R4 không
""")

print("="*80)
