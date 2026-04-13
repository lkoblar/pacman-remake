import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, BLACK

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

    def draw_button(self, text, center_y):
        text_surf = self.font_small.render(text, True, YELLOW)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, center_y))
        
        padding_x, padding_y = 20, 10
        button_rect = pygame.Rect(
            text_rect.left - padding_x, 
            text_rect.top - padding_y, 
            text_rect.width + (padding_x * 2), 
            text_rect.height + (padding_y * 2)
        )
        
        pygame.draw.rect(self.screen, (0, 0, 255), button_rect, 3)
        self.screen.blit(text_surf, text_rect)
        
        return button_rect

    def draw_level_complete(self):
        self.screen.fill(BLACK)
        
        title = self.font_large.render("Victory!", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        self.draw_button("NEXT LEVEL", 300)
        
        menu_text = self.font_small.render("MAIN MENU", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(menu_text, menu_rect)

    def draw_hud(self, score, lives):
        y_poz = 20 
        
        score_surf = self.font_small.render(f"SCORE: {score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (30, y_poz))
        
        lives_surf = self.font_small.render(f"LIVES: {lives}", True, (255, 255, 0))
        self.screen.blit(lives_surf, (SCREEN_WIDTH - 200, y_poz))

    def draw_game_over(self, score):
        self.screen.fill(BLACK)
        over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        
        score_text = self.font_small.render(f"FINAL SCORE: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        
        self.screen.blit(over_text, over_rect)
        self.screen.blit(score_text, score_rect)
    
    def draw_pause(self):        
        self.screen.fill(BLACK)

        title = self.font_large.render("PAUSED", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        resume_rect = self.draw_button("RESUME", 300)
        menu_rect = self.draw_button("MAIN MENU", 400)
        
        return resume_rect, menu_rect
