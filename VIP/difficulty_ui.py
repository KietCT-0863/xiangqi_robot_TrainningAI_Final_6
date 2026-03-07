import pygame
import sys

def show_difficulty_selection(screen):
    """
    Hiển thị overlay chọn độ khó, block execution cho tới khi user chọn xong.
    Returns: "EASY", "MEDIUM", hoặc "HARD"
    """
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Nền mờ đục 180/255
    
    font_title = pygame.font.SysFont("Verdana", 48, bold=True)
    font_btn = pygame.font.SysFont("Verdana", 32, bold=True)
    font_desc = pygame.font.SysFont("Arial", 20, italic=True)
    
    title_surf = font_title.render("CHỌN MỨC ĐỘ KHÓ", True, (255, 255, 255))
    
    btn_w, btn_h = 300, 80
    cx = screen.get_width() // 2
    cy = screen.get_height() // 2
    
    # Định nghĩa các nút
    buttons = [
        {"id": "EASY", "label": "DỄ", "color": (100, 200, 100), "y_offset": -80, "desc": "(Nhập môn, tính trước 3 nước)"},
        {"id": "MEDIUM", "label": "TRUNG BÌNH", "color": (200, 200, 100), "y_offset": 50, "desc": "(Phong trào, tính trước 10 nước)"},
        {"id": "HARD", "label": "KHÓ", "color": (255, 100, 100), "y_offset": 180, "desc": "(Siêu cấp, tính vắt kiệt 3 giây)"}
    ]
    
    for b in buttons:
        b["rect"] = pygame.Rect(cx - btn_w//2, cy + b["y_offset"], btn_w, btn_h)

    clock = pygame.time.Clock()
    
    while True:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for b in buttons:
                    if b["rect"].collidepoint(mx, my):
                        return b["id"]
        
        # Vẽ giao diện
        screen.blit(overlay, (0, 0))
        screen.blit(title_surf, title_surf.get_rect(center=(cx, cy - 200)))
        
        mx, my = pygame.mouse.get_pos()
        for b in buttons:
            # Hover effect
            is_hover = b["rect"].collidepoint(mx, my)
            color = tuple(min(255, c + 30) if is_hover else c for c in b["color"])
            
            # Vẽ nút
            pygame.draw.rect(screen, color, b["rect"], border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), b["rect"], width=3, border_radius=15)
            
            # Label
            lbl_surf = font_btn.render(b["label"], True, (20, 20, 20))
            screen.blit(lbl_surf, lbl_surf.get_rect(center=b["rect"].center))
            
            # Desc
            desc_surf = font_desc.render(b["desc"], True, (200, 200, 200))
            screen.blit(desc_surf, desc_surf.get_rect(center=(b["rect"].centerx, b["rect"].bottom + 15)))

        pygame.display.flip()
        clock.tick(30)
