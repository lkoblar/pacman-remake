import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, BLACK, RED


class UI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 36)
        self.hud_font = pygame.font.Font(None, 28)

    def _draw_text_centered(self, text, font, color, y):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(surface, rect)

    def draw_menu(self):
        self._draw_text_centered("PAC-MAN", self.title_font, YELLOW, SCREEN_HEIGHT // 3)
        self._draw_text_centered("Press ENTER to Play", self.menu_font, WHITE, SCREEN_HEIGHT // 2)
        self._draw_text_centered("Press ESC to Quit", self.menu_font, WHITE, SCREEN_HEIGHT // 2 + 50)
        self._draw_text_centered("WASD / Arrow Keys to Move", self.menu_font, WHITE, SCREEN_HEIGHT // 2 + 120)

    def draw_hud(self, score, lives):
        score_text = self.hud_font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        lives_text = self.hud_font.render(f"Lives: {lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        self._draw_text_centered("PAUSED", self.title_font, YELLOW, SCREEN_HEIGHT // 2 - 30)
        self._draw_text_centered("Press ESC to Resume", self.menu_font, WHITE, SCREEN_HEIGHT // 2 + 30)

    def draw_game_over(self, score):
        self._draw_text_centered("GAME OVER", self.title_font, RED, SCREEN_HEIGHT // 3)
        self._draw_text_centered(f"Final Score: {score}", self.menu_font, WHITE, SCREEN_HEIGHT // 2)
        self._draw_text_centered("Press ENTER to Retry", self.menu_font, WHITE, SCREEN_HEIGHT // 2 + 50)
        self._draw_text_centered("Press ESC for Menu", self.menu_font, WHITE, SCREEN_HEIGHT // 2 + 100)

    def draw_level_complete(self, level):
        self._draw_text_centered("LEVEL COMPLETE!", self.title_font, YELLOW, SCREEN_HEIGHT // 3)
        self._draw_text_centered(f"Level {level} Cleared", self.menu_font, WHITE, SCREEN_HEIGHT // 2)
        self._draw_text_centered("Press ENTER for Next Level", self.menu_font, WHITE, SCREEN_HEIGHT // 2 + 50)
        self._draw_text_centered("Press ESC for Menu", self.menu_font, WHITE, SCREEN_HEIGHT // 2 + 100)
