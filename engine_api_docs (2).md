# Engine API — Tài Liệu Cho Bên Dùng Engine của App

> **Base URL:** `https://tuongkydaisu.com`  
> **Endpoint:** `POST /api/engine/bestmove`  
> **Auth:** Không cần (public API)

---

## 1. Gọi API

### Request

```bash
curl -X POST https://tuongkydaisu.com/api/engine/bestmove \
  -H "Content-Type: application/json" \
  -d '{"fen": "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"}'
```

### Response

```json
{
  "success": true,
  "data": {
    "bestMove": "h2e2",
    "fen": "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1",
    "nodes": 100000
  }
}
```

| Field | Mô tả |
|-------|--------|
| `bestMove` | Nước đi tốt nhất, format UCI (ví dụ `h2e2`) |
| [fen](file:///d:/DDD/xiangqi/ChinaChess/src/main/java/com/tusry/chinachess/common/utils/FENUtils.java#149-153) | FEN gốc bạn gửi lên |
| `nodes` | Số node engine đã tính (100,000) |

---

## 2. Bàn Cờ Tướng — Hệ Tọa Độ

### Bàn cờ 9 cột × 10 hàng

```
     a   b   c   d   e   f   g   h   i      ← CỘT (column)
   ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 9 │ r │ n │ b │ a │ k │ a │ b │ n │ r │    ← Hàng 9 (ĐEN xa nhất)
   ├───┼───┼───┼───╲───╱───┼───┼───┼───┤
 8 │   │   │   │   │ ╳ │   │   │   │   │
   ├───┼───┼───┼───╱───╲───┼───┼───┼───┤
 7 │   │ c │   │   │   │   │   │ c │   │    ← Pháo đen (c)
   ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 6 │ p │   │ p │   │ p │   │ p │   │ p │    ← Tốt đen (p)
   ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 5 │   │   │   │   │   │   │   │   │   │    ← SÔNG
   ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 4 │   │   │   │   │   │   │   │   │   │    ← SÔNG
   ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 3 │ P │   │ P │   │ P │   │ P │   │ P │    ← Tốt đỏ (P)
   ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
 2 │   │ C │   │   │   │   │   │ C │   │    ← Pháo đỏ (C)
   ├───┼───┼───┼───╲───╱───┼───┼───┼───┤
 1 │   │   │   │   │ ╳ │   │   │   │   │
   ├───┼───┼───┼───╱───╲───┼───┼───┼───┤
 0 │ R │ N │ B │ A │ K │ A │ B │ N │ R │    ← Hàng 0 (ĐỎ gần nhất)
   └───┴───┴───┴───┴───┴───┴───┴───┴───┘
     a   b   c   d   e   f   g   h   i

     ↑                                 ↑
   Cột a                            Cột i
```

### Quy ước

| Thứ | Giá trị | Mô tả |
|-----|---------|-------|
| **Cột** | `a` → `i` | Trái → Phải (9 cột) |
| **Hàng** | `0` → `9` | Dưới (ĐỎ) → Trên (ĐEN) (10 hàng) |
| **Phe Đỏ** | `RNBAKCP` | Chữ IN HOA |
| **Phe Đen** | `rnbakcp` | Chữ thường |

### Tên quân cờ

| Ký hiệu | Tên | ĐỎ | ĐEN |
|----------|-----|-----|------|
| K/k | **Tướng** (King) | `K` | `k` |
| A/a | **Sĩ** (Advisor) | `A` | `a` |
| B/b | **Tượng** (Bishop) | `B` | `b` |
| N/n | **Mã** (Knight) | `N` | `n` |
| R/r | **Xe** (Rook) | `R` | `r` |
| C/c | **Pháo** (Cannon) | `C` | `c` |
| P/p | **Tốt** (Pawn) | `P` | `p` |

---

## 3. Chuỗi FEN — Giải Thích Chi Tiết

### Format

```
rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1
│                                                              │ │ │ │ │
│                                                              │ │ │ │ └─ Số lượt đầy đủ
│                                                              │ │ │ └─── Đếm nửa nước (halfmove)
│                                                              │ │ └───── Không dùng (luôn "-")
│                                                              │ └─────── Không dùng (luôn "-")
│                                                              └───────── Lượt đi: w=Đỏ, b=Đen
└──────────────────────────────────────────────────────────────────────── Vị trí quân cờ
```

### Phần 1: Vị trí quân cờ

FEN mô tả bàn cờ **từ trên xuống dưới** (hàng 9 → hàng 0), mỗi hàng cách nhau bằng `/`.

**Ví dụ ban đầu:**

```
rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR
│         │ │       │         │ │ │         │       │ │
│         │ │       │         │ │ │         │       │ └ Hàng 0: Xe Mã Tượng Sĩ Tướng Sĩ Tượng Mã Xe (ĐỎ)
│         │ │       │         │ │ │         │       └── Hàng 1: 9 ô trống
│         │ │       │         │ │ │         └────────── Hàng 2: _Pháo____Pháo_ (ĐỎ)
│         │ │       │         │ │ └──────────────────── Hàng 3: Tốt_Tốt_Tốt_Tốt_Tốt (ĐỎ)
│         │ │       │         │ └────────────────────── Hàng 4: 9 ô trống (SÔNG)
│         │ │       │         └──────────────────────── Hàng 5: 9 ô trống (SÔNG)
│         │ │       └────────────────────────────────── Hàng 6: tốt_tốt_tốt_tốt_tốt (ĐEN)
│         │ └────────────────────────────────────────── Hàng 7: _pháo____pháo_ (ĐEN)
│         └──────────────────────────────────────────── Hàng 8: 9 ô trống
└────────────────────────────────────────────────────── Hàng 9: xe mã tượng sĩ tướng sĩ tượng mã xe (ĐEN)
```

**Quy tắc đọc:**
- Chữ cái = quân cờ tại ô đó
- Số = số ô trống liên tiếp (VD: `1c5c1` = 1 trống + pháo + 5 trống + pháo + 1 trống)

### Phần 2: Lượt đi

- `w` = **White** = phe Đỏ đi
- `b` = **Black** = phe Đen đi

---

## 4. bestMove — Format UCI

### Cấu trúc: `[cột_gốc][hàng_gốc][cột_đích][hàng_đích]`

Ví dụ: `h2e2`

```
h2e2
││││
││└┘── Đích: cột e, hàng 2
└┘──── Gốc:  cột h, hàng 2
```

→ Di chuyển quân ở **h2** sang **e2** (Pháo đỏ di ngang)

### Ví dụ thực tế

| bestMove | Nghĩa | Quân |
|----------|--------|------|
| `h2e2` | h2 → e2 | Pháo đỏ di ngang |
| `h9g7` | h9 → g7 | Mã đen nhảy |
| `b0c2` | b0 → c2 | Mã đỏ nhảy |
| `e0e1` | e0 → e1 | Tướng đỏ tiến 1 |
| `a9a0` | a9 → a0 | Xe đen ăn Xe đỏ |

### Minh họa trên bàn cờ

```
bestMove = "h2e2" (Pháo đỏ h2 → e2)

     a   b   c   d   e   f   g   h   i
   ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 2 │   │ C │   │   │[C]│   │   │(C)│   │
   └───┴───┴───┴───┴───┴───┴───┴───┴───┘
                     ↑               ↑
                   ĐẾN            TỪ ĐÂY
                  (e2)            (h2)
```

---

## 5. Ví Dụ Sử Dụng Đầy Đủ

### Python

```python
import requests

url = "https://tuongkydaisu.com/api/engine/bestmove"

# Thế cờ ban đầu, Đỏ đi trước
fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"

response = requests.post(url, json={"fen": fen})
data = response.json()

if data["success"]:
    best = data["data"]["bestMove"]  # ví dụ: "h2e2"
    
    from_col = best[0]   # 'h'
    from_row = int(best[1])  # 2
    to_col   = best[2]   # 'e'
    to_row   = int(best[3])  # 2
    
    print(f"Di chuyển quân từ {from_col}{from_row} → {to_col}{to_row}")
```

### JavaScript

```javascript
const res = await fetch("https://tuongkydaisu.com/api/engine/bestmove", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    fen: "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
  })
});

const { data } = await res.json();
console.log("Nước đi tốt nhất:", data.bestMove);
// → "h2e2"
```

---

## 6. Lưu Ý

- Engine sử dụng **100,000 nodes** (~depth 8-10), trả kết quả trong **1-3 giây**
- FEN phải đúng chuẩn Xiangqi (9 cột, 10 hàng, có lượt đi `w`/`b`)
- `bestMove` luôn trả 4 ký tự: `[a-i][0-9][a-i][0-9]`
- API hoàn toàn miễn phí, không cần đăng ký hay token
