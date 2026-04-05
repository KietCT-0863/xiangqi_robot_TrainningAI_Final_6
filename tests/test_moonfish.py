#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Moonfish engine - Chơi thử với Moonfish
"""
import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai.moonfish_engine import MoonfishEngine
from src.core.xiangqi import get_board

def print_simple_board(board):
    """In bàn cờ đơn giản"""
    print("\n  ", end="")
    for c in range(9):
        print(f" {c} ", end="")
    print()
    for r in range(10):
        print(f"{r} ", end="")
        for c in range(9):
            piece = board[r][c]
            if piece == '.':
                print(" . ", end="")
            else:
                print(f"{piece}", end="")
        print()

def main():
    print("=" * 60)
    print("🐟 TEST MOONFISH ENGINE")
    print("=" * 60)
    
    # Khởi tạo engine
    engine = MoonfishEngine("moonfish/moonfish_ucci.py")
    engine.start()
    
    # Tạo bàn cờ ban đầu
    board = get_board()
    
    print("\n📋 Bàn cờ ban đầu:")
    print_simple_board(board)
    
    # Test 1: Hỏi nước đi cho Đen (Black)
    print("\n🤔 Hỏi Moonfish: Đen đi nước gì?")
    move = engine.pick_best_move(board, 'b', movetime_ms=2000)
    
    if move:
        (s_col, s_row), (d_col, d_row) = move
        print(f"✅ Moonfish gợi ý: ({s_col},{s_row}) → ({d_col},{d_row})")
        
        # Thực hiện nước đi
        piece = board[s_row][s_col]
        board[d_row][d_col] = piece
        board[s_row][s_col] = '.'
        
        print("\n📋 Bàn cờ sau khi Đen đi:")
        print_simple_board(board)
        
        # Test 2: Hỏi nước đi cho Đỏ (Red)
        print("\n🤔 Hỏi Moonfish: Đỏ đi nước gì?")
        move2 = engine.pick_best_move(board, 'r', movetime_ms=2000)
        
        if move2:
            (s_col, s_row), (d_col, d_row) = move2
            print(f"✅ Moonfish gợi ý: ({s_col},{s_row}) → ({d_col},{d_row})")
            
            # Thực hiện nước đi
            piece = board[s_row][s_col]
            board[d_row][d_col] = piece
            board[s_row][s_col] = '.'
            
            print("\n📋 Bàn cờ sau khi Đỏ đi:")
            print_simple_board(board)
    else:
        print("❌ Moonfish không trả về nước đi")
    
    # Dọn dẹp
    engine.stop()
    print("\n" + "=" * 60)
    print("✅ Test hoàn tất!")
    print("=" * 60)

if __name__ == '__main__':
    main()
