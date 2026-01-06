# =============================================================================
# === FILE: ai.py (FIXED: PST LOGIC + TT IMPLEMENTATION) ===
# =============================================================================
import time
import math
import xiangqi
import config
import random

# --- IMPORT BOOK ---
try:
    import ai_book as opening_book
except ImportError:
    opening_book = None

# --- CẤU HÌNH ENGINE ---
MAX_DEPTH_LIMIT = 20
TIME_BUFFER = 0.5 # Tăng buffer lên chút để tránh timeout phút chót
R_PRUNING = 2

# Transposition Table & History
# TT format: {zobrist_key: (depth, score, flag, best_move)}
# Flags: 0=EXACT, 1=LOWERBOUND (Alpha), 2=UPPERBOUND (Beta)
TT = {} 
HISTORY = {}
KILLERS = [[None]*2 for _ in range(MAX_DEPTH_LIMIT + 1)]

# --- GIÁ TRỊ QUÂN ---
VAL_PAWN = 20
VAL_ADVISOR = 40
VAL_ELEPHANT = 40
VAL_HORSE = 90
VAL_CANNON = 100
VAL_ROOK = 200
VAL_KING = 10000

PIECE_VALUES = {
    'r_P': VAL_PAWN, 'r_A': VAL_ADVISOR, 'r_E': VAL_ELEPHANT, 'r_N': VAL_HORSE, 'r_C': VAL_CANNON, 'r_R': VAL_ROOK, 'r_K': VAL_KING,
    'b_P': -VAL_PAWN, 'b_A': -VAL_ADVISOR, 'b_E': -VAL_ELEPHANT, 'b_N': -VAL_HORSE, 'b_C': -VAL_CANNON, 'b_R': -VAL_ROOK, 'b_K': -VAL_KING,
}

# --- PST TABLES (Bảng điểm vị trí) ---
# Quy ước: Index càng lớn (về phía 9) là càng áp sát cung tướng đối phương (đối với phe tấn công)
PST_PAWN = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[10,20,30,0,0,0,30,20,10],[20,30,40,50,60,50,40,30,20],[30,40,50,60,70,60,50,40,30],[40,50,60,70,80,70,60,50,40],[50,60,70,80,90,80,70,60,50]]
# Xe cơ động tốt ở hàng thông thoáng
PST_ROOK = [[0,0,0,0,0,0,0,0,0],[20,0,0,0,0,0,0,0,20],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[10,0,0,0,0,0,0,0,10],[-10,0,0,0,0,0,0,0,-10]]
# Mã thích ở trung tâm
PST_HORSE = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[10,10,10,10,10,10,10,10,10],[10,20,30,40,40,40,30,20,10],[10,20,30,40,40,40,30,20,10],[10,20,30,40,40,40,30,20,10],[10,20,30,40,40,40,30,20,10],[10,10,10,10,10,10,10,10,10],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
PST_CANNON = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,20,0,30,0,20,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[10,10,30,30,40,30,30,10,10],[10,10,10,10,10,10,10,10,10],[10,10,10,10,10,10,10,10,10]]
PST_MAP = {'P': PST_PAWN, 'R': PST_ROOK, 'N': PST_HORSE, 'C': PST_CANNON}

def get_pst(piece_type, r, c, color):
    table = PST_MAP.get(piece_type)
    if not table: return 0
    
    # --- FIX LOGIC PST ---
    # Đỏ (ở dưới r=9) đánh lên (r=0): Cần map r=9 -> index 0, r=0 -> index 9
    # Đen (ở trên r=0) đánh xuống (r=9): Cần map r=0 -> index 0, r=9 -> index 9 (nhưng bàn cờ đen thì r=0 là nhà)
    
    if color == 'r': 
        return table[9-r][c] # Đỏ càng lên cao (r nhỏ) thì index càng lớn (điểm cao)
    else: 
        return -table[r][c]  # Đen càng xuống thấp (r lớn) thì index càng lớn

# --- HÀM ĐÁNH GIÁ (DANGER SENSE) ---
def evaluate(board):
    score = 0
    r_defenders, b_defenders = 0, 0
    r_king_pos, b_king_pos = None, None
    
    for r in range(10):
        for c in range(9):
            p = board[r][c]
            if p == '.': continue
            color, ptype = p[0], p[2]
            
            # Material score
            score += PIECE_VALUES.get(p, 0)
            # Positional score
            score += get_pst(ptype, r, c, color)
            
            if ptype == 'K':
                if color == 'r': r_king_pos = (c, r)
                else: b_king_pos = (c, r)
            if ptype in ['A', 'E']:
                if color == 'r': r_defenders += 1
                else: b_defenders += 1

    # King Safety
    if r_king_pos:
        kx, ky = r_king_pos
        if r_defenders < 2: score -= 150
        # Sợ Xe/Pháo đen áp sát
        for c in range(9):
            pc = board[ky][c]
            if pc.startswith('b_R') or pc.startswith('b_C'): score -= 80

    if b_king_pos:
        kx, ky = b_king_pos
        if b_defenders < 2: score += 150
        for c in range(9):
            pc = board[ky][c]
            if pc.startswith('r_R') or pc.startswith('r_C'): score += 80

    return score

# --- MOVE SORTING ---
def sort_moves(board, moves, depth, tt_move=None):
    scored_moves = []
    killer = KILLERS[depth] if depth < MAX_DEPTH_LIMIT else [None, None]
    
    for m in moves:
        score = 0
        if m == tt_move: score = 20000 # Ưu tiên nước đi Hash
        else:
            src, dst = m
            p_dst = board[dst[1]][dst[0]]
            
            if p_dst != '.':
                victim = abs(PIECE_VALUES.get(p_dst, 0))
                score = 10000 + victim * 10 
            elif m in killer: score = 9000
            else: score = HISTORY.get(m, 0)
        
        scored_moves.append((score, m))
    
    scored_moves.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored_moves]

# --- QUIESCENCE SEARCH ---
def quiescence(board, alpha, beta, color):
    stand_pat = evaluate(board)
    if color == 'b': stand_pat = -stand_pat
    if stand_pat >= beta: return beta
    if alpha < stand_pat: alpha = stand_pat
    
    moves = xiangqi.find_all_valid_moves(color, board)
    captures = [m for m in moves if board[m[1][1]][m[1][0]] != '.']
    captures = sort_moves(board, captures, 0)
    
    for m in captures:
        nb, _ = xiangqi.make_temp_move(board, m)
        score = -quiescence(nb, -beta, -alpha, 'r' if color == 'b' else 'b')
        if score >= beta: return beta
        if score > alpha: alpha = score
    return alpha

# --- PVS (PRINCIPAL VARIATION SEARCH) ---
def pvs(board, depth, alpha, beta, color, start_time, time_limit, allow_null):
    if time.time() - start_time > time_limit: raise TimeoutError
    
    # 1. TT Lookup
    board_hash = xiangqi.get_zobrist_key(board)
    tt_entry = TT.get(board_hash)
    tt_move = None
    if tt_entry:
        tt_depth, tt_score, tt_flag, tt_move = tt_entry
        if tt_depth >= depth:
            if tt_flag == 0: return tt_score # Exact
            if tt_flag == 1 and tt_score <= alpha: return alpha # Upperbound (Fail Low)
            if tt_flag == 2 and tt_score >= beta: return beta # Lowerbound (Fail High)

    in_check = xiangqi.is_king_in_check(color, board)
    if in_check: depth += 1 
    
    if depth <= 0: return quiescence(board, alpha, beta, color)
    
    # 2. Null Move Pruning
    if allow_null and not in_check and depth >= 3:
        # Pass a COPY or just logical pass? PVS is recursive, we must not modify board.
        # Logic here: Enemy moves, I do nothing.
        R = R_PRUNING
        if depth > 6: R = 3
        
        # PVS call with swapped color (enemy plays again)
        score = -pvs(board, depth - 1 - R, -beta, -beta + 1, 'r' if color == 'b' else 'b', start_time, time_limit, False)
        if score >= beta: return beta

    moves = xiangqi.find_all_valid_moves(color, board)
    if not moves:
        if in_check: return -20000 + (MAX_DEPTH_LIMIT - depth)
        return 0
        
    moves = sort_moves(board, moves, depth, tt_move)
    
    best_move = moves[0]
    tt_flag = 1 # Default Alpha (Upperbound)
    
    for i, m in enumerate(moves):
        nb, _ = xiangqi.make_temp_move(board, m)
        
        if i == 0:
            score = -pvs(nb, depth - 1, -beta, -alpha, 'r' if color == 'b' else 'b', start_time, time_limit, True)
        else:
            # Null Window Search
            score = -pvs(nb, depth - 1, -alpha - 1, -alpha, 'r' if color == 'b' else 'b', start_time, time_limit, True)
            if alpha < score < beta:
                # Re-search full window
                score = -pvs(nb, depth - 1, -beta, -alpha, 'r' if color == 'b' else 'b', start_time, time_limit, True)
        
        if score >= beta:
            # Store TT (Lowerbound / Fail High)
            TT[board_hash] = (depth, beta, 2, m)
            if board[m[1][1]][m[1][0]] == '.':
                KILLERS[depth][1] = KILLERS[depth][0]
                KILLERS[depth][0] = m
            return beta
            
        if score > alpha:
            alpha = score
            best_move = m
            tt_flag = 0 # Exact score found
            if board[m[1][1]][m[1][0]] == '.':
                HISTORY[m] = HISTORY.get(m, 0) + depth * depth

    # Store TT (Exact or Alpha)
    TT[board_hash] = (depth, alpha, tt_flag, best_move)
    return alpha

# --- MAIN SEARCH ---
def pick_best_move(board, player_color):
    # Clear TT if too big to avoid memory leak (optional)
    if len(TT) > 1000000: TT.clear()
    if len(HISTORY) > 50000: HISTORY.clear()
    
    # Check sách khai cuộc
    current_hash = xiangqi.get_zobrist_key(board)
    if player_color == 'b' and opening_book:
        bk = opening_book.get_book_move(current_hash)
        if bk:
            print(f"[AI] 📖 Book: {bk}")
            return bk
            
    start_time = time.time()
    limit = config.AI_THINK_TIME - TIME_BUFFER
    best_move = None
    
    moves = xiangqi.find_all_valid_moves(player_color, board)
    if not moves: return None
    
    # Initial sort
    moves = sort_moves(board, moves, 0)
    best_move = moves[0]
    
    print(f"[AI] 🚀 PVS Thinking (Max {limit}s)...")
    
    try:
        for d in range(1, MAX_DEPTH_LIMIT):
            alpha, beta = -30000, 30000
            current_best_val = -30000
            current_best_move = None
            
            # Note: Moves are re-sorted inside loop implicitly by TT hits in PVS
            # But we can also re-sort root moves here based on previous iteration
            if d > 1:
                moves = sort_moves(board, moves, 0, best_move)

            for i, m in enumerate(moves):
                if time.time() - start_time > limit: raise TimeoutError
                nb, _ = xiangqi.make_temp_move(board, m)
                
                val = -pvs(nb, d - 1, -beta, -alpha, 'r' if player_color == 'b' else 'b', start_time, limit, True)
                
                if val > current_best_val:
                    current_best_val = val
                    current_best_move = m
                
                if val > alpha: alpha = val
            
            if current_best_move:
                best_move = current_best_move
                print(f"   -> Depth {d}: Score {current_best_val} | Move {best_move}")
                
                if current_best_val > 19000: # Found Checkmate
                    print("[AI] ⚡ Found Checkmate!")
                    break

    except TimeoutError:
        print("[AI] ⏰ Timeout! Move Sent.")
        
    print(f"[AI] ✅ Chốt: {best_move} ({time.time() - start_time:.2f}s)")
    return best_move