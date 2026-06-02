import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, BLACK, BLUE, CYAN, RED, GREEN, GRAY,
    TOTAL_LEVELS, MP_SCREEN_WIDTH, MP_DIVIDER,
)

BLUE_FRAME = (0, 0, 255) 
BLACK = (0, 0, 0)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_name = "Courier New"
        self.font_tiny = pygame.font.SysFont(self.font_name, 20, bold=True)
        self.font_small = pygame.font.SysFont(self.font_name, 30, bold=True)
        self.font_large = pygame.font.SysFont(self.font_name, 45, bold=True)
        self.font_huge = pygame.font.SysFont(self.font_name, 140, bold=True)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        title = self.font_large.render("Pac-Man Remake", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        play_rect = self.draw_button("PLAY", 220)
        multiplayer_rect = self.draw_button("MULTIPLAYER", 300)
        levels_rect = self.draw_button("LEVELS", 380)
        exit_rect = self.draw_button("EXIT", 460)
        
        return play_rect, multiplayer_rect, levels_rect, exit_rect
    
    def draw_levels_menu(self):
        self.screen.fill(BLACK)
        
        title = self.font_large.render("SELECT LEVEL", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        lvl1_rect = self.draw_button("LEVEL 1", 220)
        lvl2_rect = self.draw_button("LEVEL 2", 300)
        lvl3_rect = self.draw_button("LEVEL 3", 380)
        back_rect = self.draw_button("BACK", 500)
        
        return lvl1_rect, lvl2_rect, lvl3_rect, back_rect

    def draw_multiplayer_difficulty(self):
        self.screen.fill(BLACK)

        title = self.font_large.render("DIFFICULTY", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        easy_rect = self.draw_button("EASY", 220)
        normal_rect = self.draw_button("NORMAL", 300)
        hard_rect = self.draw_button("HARD", 380)
        back_rect = self.draw_button("BACK", 500)

        self._draw_difficulty_info()

        return easy_rect, normal_rect, hard_rect, back_rect

    def _draw_difficulty_info(self):
        rows = [
            ("EASY", "5", "SLOW", GREEN),
            ("NORMAL", "3", "NORMAL", YELLOW),
            ("HARD", "1", "FAST", RED),
        ]

        panel_w = 540
        header_h = 50
        row_h = 54
        panel_h = header_h + row_h * len(rows) + 24
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = 575

        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (16, 16, 32), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLUE, panel_rect, width=2, border_radius=10)

        col_mode = panel_x + 110
        col_lives = panel_x + 330
        col_ghosts = panel_x + 455

        header_y = panel_y + header_h // 2
        for label, cx in (("MODE", col_mode), ("LIVES", col_lives), ("GHOSTS", col_ghosts)):
            h_surf = self.font_tiny.render(label, True, GRAY)
            self.screen.blit(h_surf, h_surf.get_rect(center=(cx, header_y)))

        pygame.draw.line(
            self.screen, (60, 60, 90),
            (panel_x + 18, panel_y + header_h),
            (panel_x + panel_w - 18, panel_y + header_h),
            1,
        )

        y = panel_y + header_h + row_h // 2 + 4
        for name, lives, ghosts, color in rows:
            name_surf = self.font_small.render(name, True, color)
            self.screen.blit(name_surf, name_surf.get_rect(center=(col_mode, y)))

            lives_surf = self.font_small.render(lives, True, WHITE)
            self.screen.blit(lives_surf, lives_surf.get_rect(center=(col_lives, y)))

            ghosts_surf = self.font_tiny.render(ghosts, True, WHITE)
            self.screen.blit(ghosts_surf, ghosts_surf.get_rect(center=(col_ghosts, y)))

            y += row_h

    def draw_button(self, text, center_y):
        text_surf = self.font_small.render(text, True, YELLOW)
        
        button_rect = pygame.Rect(0, 0, 220, 45)
        button_rect.center = (SCREEN_WIDTH // 2, center_y)
        
        pygame.draw.rect(self.screen, BLACK, button_rect, border_radius=5)
        pygame.draw.rect(self.screen, BLUE, button_rect, width=3, border_radius=5)
        
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return button_rect

    def draw_level_complete(self, current_level, score, time_bonus=0):
        YELLOW = (255, 255, 0)

        victory_text = self.font_large.render("VICTORY!", True, YELLOW)
        vic_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110))
        self.screen.blit(victory_text, vic_rect)

        level_text = self.font_small.render(f"LEVEL {current_level} COMPLETED", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(level_text, level_rect)

        bonus_text = self.font_small.render(f"TIME BONUS: +{time_bonus}", True, CYAN)
        bonus_rect = bonus_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
        self.screen.blit(bonus_text, bonus_rect)

        if current_level < TOTAL_LEVELS:
            score_label = f"CURRENT SCORE: {score}"
        else:
            score_label = f"FINAL SCORE: {score}"

        score_text = self.font_small.render(score_label, True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
        self.screen.blit(score_text, score_rect)

        if current_level < TOTAL_LEVELS:
            text_surf1 = self.font_small.render("NEXT LEVEL", True, YELLOW)
            next_rect = pygame.Rect(0, 0, 220, 45)
            next_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
            
            pygame.draw.rect(self.screen, BLACK, next_rect, border_radius=5)
            pygame.draw.rect(self.screen, BLUE, next_rect, width=3, border_radius=5)
            self.screen.blit(text_surf1, text_surf1.get_rect(center=next_rect.center))

            text_surf2 = self.font_small.render("MAIN MENU", True, YELLOW)
            menu_rect = pygame.Rect(0, 0, 220, 45)
            menu_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140)
            
            pygame.draw.rect(self.screen, BLACK, menu_rect, border_radius=5)
            pygame.draw.rect(self.screen, BLUE, menu_rect, width=3, border_radius=5)
            self.screen.blit(text_surf2, text_surf2.get_rect(center=menu_rect.center))

            return next_rect, menu_rect
        else:
            text_surf2 = self.font_small.render("MAIN MENU", True, YELLOW)
            menu_rect = pygame.Rect(0, 0, 220, 45)
            menu_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
            
            pygame.draw.rect(self.screen, BLACK, menu_rect, border_radius=5)
            pygame.draw.rect(self.screen, BLUE, menu_rect, width=3, border_radius=5)
            self.screen.blit(text_surf2, text_surf2.get_rect(center=menu_rect.center))
            
            return None, menu_rect

    def draw_hud(self, score, lives, multiplier=1.0, muted=False):
        y_poz = 20 
        
        score_surf = self.font_small.render(f"SCORE: {score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (30, y_poz))

        audio_status = "AUDIO: OFF" if muted else "AUDIO: ON"

        audio_surf = self.font_small.render(audio_status, True, WHITE)
        audio_rect = audio_surf.get_rect(bottomleft=(20, SCREEN_HEIGHT - 10))
        self.screen.blit(audio_surf, audio_rect)
        
        lives_surf = self.font_small.render(f"LIVES: {lives}", True, (255, 255, 0))
        lives_rect = lives_surf.get_rect(topright=(SCREEN_WIDTH - 30, y_poz))
        self.screen.blit(lives_surf, lives_rect)

    def draw_game_over(self, score):
        YELLOW = (255, 255, 0)

        game_over_text = self.font_large.render("GAME OVER", True, (255, 49, 49))
        go_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, go_rect)

        score_text = self.font_small.render(f"FINAL SCORE: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)

        restart_rect = self.draw_button("RESTART", SCREEN_HEIGHT // 2 + 50)

        return restart_rect

    def draw_pause(self):        
        self.screen.fill(BLACK)

        title = self.font_large.render("PAUSED", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        resume_rect = self.draw_button("RESUME", 300)
        menu_rect = self.draw_button("MAIN MENU", 400)
        
        return resume_rect, menu_rect

    def draw_multiplayer_ready(self, ready1, ready2, title_text="MULTIPLAYER"):
        self.screen.fill(BLACK)

        w = self.screen.get_width()
        h = self.screen.get_height()

        title = self.font_large.render(title_text, True, YELLOW)
        title_rect = title.get_rect(center=(w // 2, 90))
        self.screen.blit(title, title_rect)

        left_cx = w // 4
        right_cx = w * 3 // 4

        self._draw_ready_panel(left_cx, "PLAYER 1", ["W", "A  S  D"], "READY: SPACE", ready1)
        self._draw_ready_panel(right_cx, "PLAYER 2", ["UP", "LEFT  DOWN  RIGHT"], "READY: ENTER", ready2)

        pygame.draw.line(
            self.screen, BLUE,
            (w // 2, 0),
            (w // 2, h),
            MP_DIVIDER,
        )

    def _draw_ready_panel(self, center_x, label, control_lines, ready_hint, is_ready):
        label_surf = self.font_large.render(label, True, WHITE)
        self.screen.blit(label_surf, label_surf.get_rect(center=(center_x, 220)))

        y = 320
        for line in control_lines:
            line_surf = self.font_small.render(line, True, CYAN)
            self.screen.blit(line_surf, line_surf.get_rect(center=(center_x, y)))
            y += 45

        hint_surf = self.font_small.render(ready_hint, True, YELLOW)
        self.screen.blit(hint_surf, hint_surf.get_rect(center=(center_x, y + 40)))

        status_text = "READY!" if is_ready else "NOT READY"
        status_color = GREEN if is_ready else GRAY
        status_surf = self.font_large.render(status_text, True, status_color)
        self.screen.blit(status_surf, status_surf.get_rect(center=(center_x, y + 120)))

    def draw_multiplayer_hud(self, side_x, score, lives, label):
        y_poz = 12

        label_surf = self.font_small.render(label, True, YELLOW)
        label_rect = label_surf.get_rect(midtop=(side_x + SCREEN_WIDTH // 2, y_poz))
        self.screen.blit(label_surf, label_rect)

        score_surf = self.font_small.render(f"SCORE: {score}", True, WHITE)
        self.screen.blit(score_surf, (side_x + 20, y_poz))

        lives_surf = self.font_small.render(f"LIVES: {lives}", True, YELLOW)
        lives_rect = lives_surf.get_rect(topright=(side_x + SCREEN_WIDTH - 20, y_poz))
        self.screen.blit(lives_surf, lives_rect)

    def _draw_centered_button(self, text, center_x, center_y, width=240):
        surf = self.font_small.render(text, True, YELLOW)
        rect = pygame.Rect(0, 0, width, 45)
        rect.center = (center_x, center_y)
        pygame.draw.rect(self.screen, BLACK, rect, border_radius=5)
        pygame.draw.rect(self.screen, BLUE, rect, width=3, border_radius=5)
        self.screen.blit(surf, surf.get_rect(center=rect.center))
        return rect

    def draw_multiplayer_pause(self):
        w = self.screen.get_width()
        h = self.screen.get_height()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        cx = w // 2

        title = self.font_large.render("PAUSED", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(cx, h // 2 - 120)))

        resume_rect = self._draw_centered_button("RESUME", cx, h // 2 - 20)
        menu_rect = self._draw_centered_button("MAIN MENU", cx, h // 2 + 50)

        return resume_rect, menu_rect

    def draw_multiplayer_countdown(self, number):
        w = self.screen.get_width()
        h = self.screen.get_height()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        cx = w // 2

        num_surf = self.font_huge.render(str(number), True, YELLOW)
        self.screen.blit(num_surf, num_surf.get_rect(center=(cx, h // 2)))

    def draw_multiplayer_overlay(self, side_x, finish_reason, score):
        board_height = SCREEN_HEIGHT - 50

        overlay = pygame.Surface((SCREEN_WIDTH, board_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (side_x, 50))

        cx = side_x + SCREEN_WIDTH // 2
        cy = 50 + board_height // 2

        if finish_reason == "cleared":
            title_text = "FINISHED!"
            title_color = GREEN
        else:
            title_text = "GAME OVER"
            title_color = RED

        title_surf = self.font_large.render(title_text, True, title_color)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, cy - 50)))

        score_surf = self.font_small.render(f"SCORE: {score}", True, WHITE)
        self.screen.blit(score_surf, score_surf.get_rect(center=(cx, cy + 5)))

        wait_surf = self.font_small.render("WAITING...", True, YELLOW)
        self.screen.blit(wait_surf, wait_surf.get_rect(center=(cx, cy + 55)))

    def draw_multiplayer_result(self, score1, score2):
        self.screen.fill(BLACK)

        if score1 > score2:
            result_text = "PLAYER 1 WINS"
            result_color = YELLOW
        elif score2 > score1:
            result_text = "PLAYER 2 WINS"
            result_color = YELLOW
        else:
            result_text = "DRAW"
            result_color = WHITE

        cx = MP_SCREEN_WIDTH // 2

        title = self.font_large.render(result_text, True, result_color)
        self.screen.blit(title, title.get_rect(center=(cx, SCREEN_HEIGHT // 2 - 140)))

        p1_surf = self.font_small.render(f"PLAYER 1: {score1}", True, WHITE)
        self.screen.blit(p1_surf, p1_surf.get_rect(center=(cx, SCREEN_HEIGHT // 2 - 60)))

        p2_surf = self.font_small.render(f"PLAYER 2: {score2}", True, WHITE)
        self.screen.blit(p2_surf, p2_surf.get_rect(center=(cx, SCREEN_HEIGHT // 2 - 15)))

        again_surf = self.font_small.render("PLAY AGAIN", True, YELLOW)
        again_rect = pygame.Rect(0, 0, 240, 45)
        again_rect.center = (cx, SCREEN_HEIGHT // 2 + 60)
        pygame.draw.rect(self.screen, BLACK, again_rect, border_radius=5)
        pygame.draw.rect(self.screen, BLUE, again_rect, width=3, border_radius=5)
        self.screen.blit(again_surf, again_surf.get_rect(center=again_rect.center))

        menu_surf = self.font_small.render("MAIN MENU", True, YELLOW)
        menu_rect = pygame.Rect(0, 0, 240, 45)
        menu_rect.center = (cx, SCREEN_HEIGHT // 2 + 120)
        pygame.draw.rect(self.screen, BLACK, menu_rect, border_radius=5)
        pygame.draw.rect(self.screen, BLUE, menu_rect, width=3, border_radius=5)
        self.screen.blit(menu_surf, menu_surf.get_rect(center=menu_rect.center))

        return again_rect, menu_rect

    def draw_multiplayer_mode_select(self):
        self.screen.fill(BLACK)

        title = self.font_large.render("MULTIPLAYER", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        battle_rect = self.draw_button("BATTLE", 240)
        coop_rect = self.draw_button("CO-OP", 320)
        back_rect = self.draw_button("BACK", 440)

        info = [
            "BATTLE: most points wins",
            "CO-OP: team up on one map",
        ]
        y = 510
        for line in info:
            line_surf = self.font_tiny.render(line, True, CYAN)
            self.screen.blit(line_surf, line_surf.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 32

        return battle_rect, coop_rect, back_rect

    def draw_coop_hud(self, score, screen_width, shared=False, lives1=0, lives2=0, shared_lives=0):
        y_poz = 12

        score_surf = self.font_small.render(f"SCORE: {score}", True, WHITE)
        self.screen.blit(score_surf, score_surf.get_rect(midtop=(screen_width // 2, y_poz)))

        if shared:
            team_surf = self.font_small.render(f"TEAM LIVES: {shared_lives}", True, CYAN)
            self.screen.blit(team_surf, (20, y_poz))
            return

        l1_text = f"P1: {lives1}" if lives1 > 0 else "P1: OUT"
        l1_surf = self.font_small.render(l1_text, True, YELLOW)
        self.screen.blit(l1_surf, (20, y_poz))

        l2_text = f"P2: {lives2}" if lives2 > 0 else "P2: OUT"
        l2_surf = self.font_small.render(l2_text, True, GREEN)
        l2_rect = l2_surf.get_rect(topright=(screen_width - 20, y_poz))
        self.screen.blit(l2_surf, l2_rect)

    def _draw_option_button(self, text, center_x, center_y, selected, width=150, height=45):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (center_x, center_y)

        if selected:
            pygame.draw.rect(self.screen, (10, 40, 16), rect, border_radius=5)
            pygame.draw.rect(self.screen, GREEN, rect, width=3, border_radius=5)
            text_color = WHITE
        else:
            pygame.draw.rect(self.screen, BLACK, rect, border_radius=5)
            pygame.draw.rect(self.screen, BLUE, rect, width=3, border_radius=5)
            text_color = YELLOW

        text_surf = self.font_small.render(text, True, text_color)
        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
        return rect

    def _draw_section_label(self, text, center_y):
        surf = self.font_tiny.render(text, True, GRAY)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, center_y)))

    def draw_coop_config(self, lives_mode, lives, difficulty):
        self.screen.fill(BLACK)
        cx = SCREEN_WIDTH // 2

        title = self.font_large.render("CO-OP SETUP", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(cx, 80)))

        buttons = {}

        self._draw_section_label("LIVES", 165)
        buttons["mode_separate"] = self._draw_option_button(
            "SEPARATE", cx - 95, 210, lives_mode == "separate", width=175
        )
        buttons["mode_shared"] = self._draw_option_button(
            "SHARED", cx + 95, 210, lives_mode == "shared", width=175
        )

        self._draw_section_label("COUNT", 285)
        for i, value in enumerate((1, 3, 5)):
            x = cx + (i - 1) * 130
            buttons[f"lives_{value}"] = self._draw_option_button(
                str(value), x, 330, lives == value, width=100
            )

        self._draw_section_label("DIFFICULTY", 405)
        for i, name in enumerate(("EASY", "NORMAL", "HARD")):
            x = cx + (i - 1) * 175
            buttons[f"diff_{name}"] = self._draw_option_button(
                name, x, 450, difficulty == name, width=160
            )

        info = [
            "EASY/NORMAL/HARD = ghost speed",
            "HARD: players collide -> lose a life",
        ]
        y = 520
        for line in info:
            line_surf = self.font_tiny.render(line, True, CYAN)
            self.screen.blit(line_surf, line_surf.get_rect(center=(cx, y)))
            y += 30

        buttons["start"] = self.draw_button("START", 620)
        buttons["back"] = self.draw_button("BACK", 690)

        return buttons

    def draw_coop_result(self, score, result):
        self.screen.fill(BLACK)

        w = self.screen.get_width()
        h = self.screen.get_height()
        cx = w // 2

        if result == "win":
            title_text = "YOU WIN!"
            title_color = GREEN
        else:
            title_text = "GAME OVER"
            title_color = RED

        title = self.font_large.render(title_text, True, title_color)
        self.screen.blit(title, title.get_rect(center=(cx, h // 2 - 120)))

        score_surf = self.font_small.render(f"SCORE: {score}", True, WHITE)
        self.screen.blit(score_surf, score_surf.get_rect(center=(cx, h // 2 - 40)))

        again_rect = self._draw_centered_button("PLAY AGAIN", cx, h // 2 + 30)
        menu_rect = self._draw_centered_button("MAIN MENU", cx, h // 2 + 90)

        return again_rect, menu_rect