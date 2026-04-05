# Moonfish Engine Folder

## Cấu trúc thư mục

```
moonfish/
├── .keep                    # File giữ thư mục trong Git
├── README.md                # File này
├── moonfish.nnue            # Neural Network file (cần tải về)
└── Windows/
    └── moonfish-avx2.exe    # Engine executable (cần tải về)
```

## Hướng dẫn cài đặt

### Bước 1: Tải Moonfish Engine

**Lưu ý:** Hiện tại chưa có Moonfish engine chính thức cho Xiangqi dạng UCI executable.

Các lựa chọn thay thế:

1. **Tiếp tục dùng Pikafish** (khuyến nghị)
   - Mạnh nhất hiện tại cho Xiangqi
   - Tải từ: https://github.com/official-pikafish/Pikafish/releases

2. **Fairy-Stockfish** (hỗ trợ Xiangqi)
   - Tải từ: https://github.com/fairy-stockfish/Fairy-Stockfish/releases
   - Hỗ trợ nhiều biến thể cờ

3. **Tự build từ source**
   - walker8088/moonfish (Python): https://github.com/walker8088/moonfish
   - Cần compile thành executable

### Bước 2: Đặt file vào đúng vị trí

1. Copy file `moonfish-avx2.exe` vào thư mục `Windows/`
2. Copy file `moonfish.nnue` vào thư mục gốc `moonfish/`

### Bước 3: Kiểm tra

Chạy lệnh để test engine:
```bash
moonfish/Windows/moonfish-avx2.exe
```

Nếu thành công, bạn sẽ thấy prompt UCI.

## Cấu hình trong config.py

```python
MOONFISH_EXE  = 'moonfish/Windows/moonfish-avx2.exe'
MOONFISH_NNUE = 'moonfish/moonfish.nnue'
MOONFISH_THINK_MS = 3000
```

## Lưu ý

- File `.keep` giúp Git giữ thư mục rỗng
- Các file `.exe` và `.nnue` KHÔNG được push lên Git (đã có trong .gitignore)
- Mỗi người phải tự tải về và cài đặt
