# ==================================
# === FILE: VIP/ai_controller.py ===
# === AI Controller — Pikafish Engine Wrapper ===
# ==================================
import traceback


class AIController:
    """Wrapper cho Pikafish engine, chạy trong thread riêng (non-blocking).

    Cách dùng từ main_VIP.py:
        ai_ctrl = AIController(engine, config)
        # Trong game loop:
        ai_ctrl.start_thinking(board_snapshot)
        # Check kết quả:
        if ai_ctrl.is_done():
            move = ai_ctrl.get_result()
    """

    def __init__(self, engine, config):
        """
        Args:
            engine: PikafishEngine instance (đã start())
            config: module config (dùng PIKAFISH_THINK_MS)
        """
        self.engine = engine
        self.config = config

    def pick_move(self, board_snapshot, color="b", difficulty="HARD"):
        """Gọi Pikafish để lấy nước đi tốt nhất.

        Hàm này chạy BLOCKING — phải gọi trong thread riêng.

        Args:
            board_snapshot: bản sao board 10x9 tại thời điểm AI bắt đầu nghĩ
            color:          màu AI đang đánh ('b' = đen)
            difficulty:     mức độ khó ('EASY', 'MEDIUM', 'HARD')

        Returns:
            (src, dst) tuple nếu tìm được nước đi
            None nếu thất bại hoặc engine chưa khởi động
        """
        if self.engine is None:
            print("[AI] ❌ Pikafish engine chưa khởi động! "
                  "Kiểm tra file exe trong thư mục pikafish/.")
            return None

        try:
            diff_settings = self.config.DIFFICULTY_LEVELS.get(difficulty, self.config.DIFFICULTY_LEVELS["HARD"])
            if diff_settings["type"] == "depth":
                result = self.engine.pick_best_move(
                    board_snapshot, color, depth=diff_settings["value"]
                )
            else:
                result = self.engine.pick_best_move(
                    board_snapshot, color, movetime_ms=diff_settings["value"]
                )
            return result
        except Exception as e:
            print(f"[AI] ❌ Pikafish error: {e}")
            traceback.print_exc()
            return None
