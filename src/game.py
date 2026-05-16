import os
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK,
    GameState, LEVELS_DIR, PLAYER_LIVES,
)
from src.sprite_loader import SpriteLoader
from src.map import Map
from src.player import Player
from src.ghost import Ghost
from src.food import FoodManager
from src.ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Remake")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU

        self.sprite_loader = SpriteLoader()
        self.sprite_loader.load_all()

        self.ui = UI(self.screen)
        self.current_level = 1
        self.score = 0
        self.lives = PLAYER_LIVES

        self.game_map = None
        self.player = None
        self.ghosts = []
        self.food_manager = None
        
        self.buttons = {}

    def load_level(self, level_num):
        level_path = os.path.join(LEVELS_DIR, f"level{level_num}.txt")
        if not os.path.exists(level_path):
            level_path = os.path.join(LEVELS_DIR, "level1.txt")

        self.game_map = Map(level_path, self.sprite_loader)
        self.player = Player(self.game_map, self.sprite_loader)
        self.ghosts = Ghost.create_from_map(self.game_map, self.sprite_loader)
        self.food_manager = FoodManager(self.game_map, self.sprite_loader)

    def start_game(self):
        self.score = 0
        self.lives = PLAYER_LIVES
        self.current_level = 1
        self.load_level(self.current_level)
        self.state = GameState.PLAYING

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.state == GameState.MENU:
                    if self.buttons.get("play") and self.buttons["play"].collidepoint(mouse_pos):
                        self.start_game()
                    elif self.buttons.get("exit") and self.buttons["exit"].collidepoint(mouse_pos):
                        self.running = False
                
                elif self.state == GameState.PAUSED:
                    if self.buttons.get("resume") and self.buttons["resume"].collidepoint(mouse_pos):
                        self.state = GameState.PLAYING
                    elif self.buttons.get("main_menu") and self.buttons["main_menu"].collidepoint(mouse_pos):
                        self.state = GameState.MENU

            if self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.PLAYING:
                self._handle_playing_events(event)
            elif self.state == GameState.PAUSED:
                self._handle_paused_events(event)
            elif self.state == GameState.GAME_OVER:
                self._handle_game_over_events(event)
            elif self.state == GameState.LEVEL_COMPLETE:
                self._handle_level_complete_events(event)

    def _handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def _handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.PAUSED

    def _handle_paused_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.PLAYING

    def _handle_game_over_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.buttons.get("restart") and self.buttons["restart"].collidepoint(mouse_pos):
                    self.start_game()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _handle_level_complete_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.current_level += 1
                self.load_level(self.current_level)
                self.state = GameState.PLAYING
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def update(self, dt):
        if self.state != GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()
        if self.player:
            self.player.handle_input(keys)
            self.player.update(dt, self.game_map)

        for ghost in self.ghosts:
            ghost.update(dt, self.game_map, self.player)

        if self.food_manager and self.player:
            points = self.food_manager.check_collisions(self.player)
            self.score += points

            if self.food_manager.all_collected():
                self.state = GameState.LEVEL_COMPLETE

        for ghost in self.ghosts:
            if ghost.check_collision(self.player):
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GameState.GAME_OVER
                else:
                    self.player.reset_position()
                    for g in self.ghosts:
                        g.reset_position()

    def render(self):
        self.screen.fill(BLACK)

        if self.state == GameState.MENU:
            play_rect, levels_rect, exit_rect = self.ui.draw_menu()
            self.buttons["play"] = play_rect
            self.buttons["levels"] = levels_rect
            self.buttons["exit"] = exit_rect

        elif self.state in (GameState.PLAYING, GameState.PAUSED, GameState.LEVEL_COMPLETE):
            if self.game_map:
                self.game_map.render(self.screen)
            if self.food_manager:
                self.food_manager.render(self.screen)

            for ghost in self.ghosts:
                ghost.draw(self.screen)
            if self.player:
                self.player.draw(self.screen)

            self.ui.draw_hud(self.score, self.lives)

            if self.state == GameState.PAUSED:
                resume_rect, menu_rect = self.ui.draw_pause()
                self.buttons["resume"] = resume_rect
                self.buttons["main_menu"] = menu_rect
            
            elif self.state == GameState.LEVEL_COMPLETE:
                self.ui.draw_level_complete(self.current_level)

        elif self.state == GameState.GAME_OVER:
            restart_rect = self.ui.draw_game_over(self.score)
            self.buttons["restart"] = restart_rect

        pygame.display.flip()