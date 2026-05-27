import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, BLACK, BLUE, CYAN, TOTAL_LEVELS

BLUE_FRAME = (0, 0, 255) 
BLACK = (0, 0, 0)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_name = "Courier New"
        self.font_small = pygame.font.SysFont(self.font_name, 30, bold=True)
        self.font_large = pygame.font.SysFont(self.font_name, 45, bold=True)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        
        title = self.font_large.render("Pac-Man Remake", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        play_rect = self.draw_button("PLAY", 250)
        levels_rect = self.draw_button("LEVELS", 350)
        exit_rect = self.draw_button("EXIT", 450)
        
        return play_rect, levels_rect, exit_rect
    
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

    def draw_button(self, text, center_y):
        text_surf = self.font_small.render(text, True, YELLOW)
        
        button_rect = pygame.Rect(0, 0, 180, 45)
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

    def draw_hud(self, score, lives, multiplier=1.0):
        y_poz = 20 
        
        score_surf = self.font_small.render(f"SCORE: {score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (30, y_poz))
        
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