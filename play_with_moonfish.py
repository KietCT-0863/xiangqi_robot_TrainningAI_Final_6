#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chơi cờ tướng với Moonfish Engine - Console Game
Không cần Camera, Robot - Chỉ cần bàn phím!
"""

from src.ai.moonfish_engine import MoonfishEngine
from src.core.xiangqi import get_board

def print_board(board):
    """In bàn cờ đẹp"""
    print("\n" + "=" * 50)
    print("  ", end="")
    for c in range(9):
        print(f"  {c} ", end="")
    print("\n" + "-" * 50)
    
    for r in range(10):
        print(f"{r} |", end="")
        for c in range(9):
            piece = board[r][c]
            if piece == '.':
                print("  . ", end="")
            else:
                # Màu cho quân cờ
                if piece.startswith('r_'):
                    print(f" {piece}", end="")  # Đỏ
                else:
                    print(f" {piece}", end="")  # Đen
        print(f" | {r}")
    
    print("-" * 50)
    print("  ", end="")
    for c in range(9):
        print(f"  {c} ", end="")
    print("\n" + "=" * 50)

def get_user_move():
    """Nhập nước đi từ người chơi"""
    print("\n📝 Nhập nước đi của bạn (ví dụ: 4,6,4,5 nghĩa là từ cột 4 hàng 6 đến cột 4 hàng 5)")
    print("   Hoặc gõ 'quit' để thoát")
    
    move_str = input("👉 Nước đi: ").strip()
    
    if move_str.lower() == 'quit':
        return None
    
    try:
        parts = move_str.replace(' ', '').split(',')
        if len(parts) != 4:
            print("❌ Sai định dạng! Cần 4 số: cột_nguồn,hàng_nguồn,cột_đích,hàng_đích")
            return get_user_move()
        
        s_col, s_row, d_col, d_row = map(int, parts)
        
        # Kiểm tra phạm vi
        if not (0 <= s_col <= 8 and 0 <= s_row <= 9 and 0 <= d_col <= 8 and 0 <= d_row <= 9):
            print("❌ Tọa độ nằm ngoài bàn cờ! (cột: 0-8, hàng: 0-9)")
            return get_user_move()
        
        return (s_col, s_row), (d_col, d_row)
    
    except ValueError:
        print("❌ Sai định dạng! Vui lòng nhập 4 số cách nhau bởi dấu phẩy")
        return get_user_move()

def is_valid_move(board, move, color):
    """Kiểm tra nước đi có hợp lệ không (đơn giản)"""
    (s_col, s_row), (d_col, d_row) = move
    
    # Kiểm tra ô nguồn có quân không
    piece = board[s_row][s_col]
    if piece == '.':
        print("❌ Ô nguồn không có quân cờ!")
        return False
    
    # Kiểm tra quân cờ có đúng màu không
    if color == 'r' and not piece.startswith('r_'):
        print("❌ Đây không phải quân Đỏ của bạn!")
        return False
    if color == 'b' and not piece.startswith('b_'):
        print("❌ Đây không phải quân Đen của bạn!")
        return False
    
    # Kiểm tra không ăn quân cùng màu
    target = board[d_row][d_col]
    if target != '.' and target.startswith(piece[0:2]):
        print("❌ Không thể ăn quân cùng màu!")
        return False
    
    return True

def apply_move(board, move):
    """Thực hiện nước đi"""
    (s_col, s_row), (d_col, d_row) = move
    piece = board[s_row][s_col]
    board[d_row][d_col] = piece
    board[s_row][s_col] = '.'
    return board

def main():
    print("=" * 60)
    print("🐟 CHƠI CỜ TƯỚNG VỚI MOONFISH ENGINE")
    print("=" * 60)
    
    # Chọn màu
    print("\n🎨 Bạn muốn chơi màu gì?")
    print("  1. Đỏ (Red) - Đi trước")
    print("  2. Đen (Black) - Đi sau")
    
    choice = input("👉 Chọn (1 hoặc 2): ").strip()
    
    if choice == '1':
        player_color = 'r'
        ai_color = 'b'
        print("\n✅ Bạn chơi màu ĐỎ - Bạn đi trước!")
    else:
        player_color = 'b'
        ai_color = 'r'
        print("\n✅ Bạn chơi màu ĐEN - AI đi trước!")
    
    # Khởi tạo engine
    print("\n🔧 Đang khởi động Moonfish engine...")
    engine = MoonfishEngine("moonfish/moonfish_ucci.py")
    
    try:
        engine.start()
    except Exception as e:
        print(f"❌ Lỗi khởi động Moonfish: {e}")
        print("\n💡 Gợi ý: Kiểm tra xem file moonfish/moonfish_ucci.py có tồn tại không")
        return
    
    # Tạo bàn cờ
    board = get_board()
    current_turn = 'r'  # Đỏ đi trước
    move_count = 0
    
    print("\n🎮 Bắt đầu game!")
    print_board(board)
    
    # Game loop
    while True:
        move_count += 1
        print(f"\n{'='*60}")
        print(f"🎯 Lượt {move_count} - {'ĐỎ' if current_turn == 'r' else 'ĐEN'} đi")
        print(f"{'='*60}")
        
        if current_turn == player_color:
            # Lượt người chơi
            print("\n👤 Lượt của BẠN")
            move = get_user_move()
            
            if move is None:
                print("\n👋 Cảm ơn bạn đã chơi!")
                break
            
            # Kiểm tra nước đi hợp lệ
            if not is_valid_move(board, move, player_color):
                print("⚠️ Nước đi không hợp lệ, thử lại!")
                continue
            
            # Thực hiện nước đi
            board = apply_move(board, move)
            (s_col, s_row), (d_col, d_row) = move
            print(f"✅ Bạn đã đi: ({s_col},{s_row}) → ({d_col},{d_row})")
            
        else:
            # Lượt AI
            print("\n🤖 Lượt của MOONFISH AI")
            print("🤔 Đang suy nghĩ...")
            
            try:
                move = engine.pick_best_move(board, ai_color, movetime_ms=3000)
                
                if move is None:
                    print("❌ Moonfish không tìm được nước đi - Có thể hết quân hoặc bị chiếu hết!")
                    print("🎉 BẠN THẮNG!")
                    break
                
                # Thực hiện nước đi
                board = apply_move(board, move)
                (s_col, s_row), (d_col, d_row) = move
                print(f"✅ Moonfish đã đi: ({s_col},{s_row}) → ({d_col},{d_row})")
                
            except Exception as e:
                print(f"❌ Lỗi khi Moonfish suy nghĩ: {e}")
                break
        
        # Hiển thị bàn cờ
        print_board(board)
        
        # Đổi lượt
        current_turn = 'b' if current_turn == 'r' else 'r'
    
    # Dọn dẹp
    engine.stop()
    print("\n" + "=" * 60)
    print("🏁 Game kết thúc!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Đã thoát game. Hẹn gặp lại!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
