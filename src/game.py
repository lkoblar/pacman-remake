import os
import time
import pygame

from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BLACK,
    GameState,
    LEVELS_DIR,
    PLAYER_LIVES,
    FRIGHTENED_DURATION,
    TOTAL_LEVELS,
    FRIGHTENED_FLASH_TIME,
    LIVES_SCORE_MULTIPLIERS,
    TIME_BONUS_BASE,
    MAX_TIME_BONUS,
)
from src.sprite_loader import SpriteLoader
from src.map import Map
from src.player import Player
from src.ghost import Ghost
from src.food import FoodManager
from src.ui import UI
from src.audio import AudioManager


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

        self.frightened_timer = 0.0
        self.ghost_eat_score = 200
        self.eaten_ghosts = set()

        self.level_start_time = 0.0
        self.level_time_bonus = 0

        self.buttons = {}
        self.audio = AudioManager()

    @property
    def frightened_active(self):
        return self.frightened_timer > 0

    @property
    def score_multiplier(self):
        return LIVES_SCORE_MULTIPLIERS.get(self.lives, 0.5)

    def load_level(self, level_num):
        level_path = os.path.join(LEVELS_DIR, f"level{level_num}.txt")
        if not os.path.exists(level_path):
            level_path = os.path.join(LEVELS_DIR, "level1.txt")

        self.game_map = Map(level_path, self.sprite_loader)
        self.player = Player(self.game_map, self.sprite_loader)
        self.ghosts = Ghost.create_from_map(self.game_map, self.sprite_loader)
        self.food_manager = FoodManager(self.game_map, self.sprite_loader)
        self.frightened_timer = 0.0
        self.ghost_eat_score = 200
        self.eaten_ghosts.clear()
        self.level_start_time = time.time()
        self.level_time_bonus = 0

    def start_game(self):
        self.score = 0
        self.lives = PLAYER_LIVES
        self.current_level = 1
        self.load_level(self.current_level)
        self.state = GameState.PLAYING
        self.audio.play_music()

    def select_level(self, level_num):
        self.score = 0
        self.lives = PLAYER_LIVES
        self.current_level = level_num
        self.load_level(self.current_level)
        self.state = GameState.PLAYING
        self.audio.play_music()

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
                    elif self.buttons.get("gamemodes") and self.buttons["gamemodes"].collidepoint(mouse_pos):
                        self.state = GameState.GAMEMODES_SELECT
                    elif self.buttons.get("levels") and self.buttons["levels"].collidepoint(mouse_pos):
                        self.state = GameState.LEVEL_SELECT
                    elif self.buttons.get("exit") and self.buttons["exit"].collidepoint(mouse_pos):
                        self.running = False

                elif self.state == GameState.GAMEMODES_SELECT:
                    if self.buttons.get("one_life") and self.buttons["one_life"].collidepoint(mouse_pos):
                        self.lives = 1
                        self.start_game()
                    elif self.buttons.get("hard_mode") and self.buttons["hard_mode"].collidepoint(mouse_pos):
                        self.start_game()
                    elif self.buttons.get("battle_mode") and self.buttons["battle_mode"].collidepoint(mouse_pos):
                        self.start_game()
                    elif self.buttons.get("back") and self.buttons["back"].collidepoint(mouse_pos):
                        self.state = GameState.MENU

                elif self.state == GameState.LEVEL_SELECT:
                    if self.buttons.get("lvl1") and self.buttons["lvl1"].collidepoint(mouse_pos):
                        self.select_level(1)
                    elif self.buttons.get("lvl2") and self.buttons["lvl2"].collidepoint(mouse_pos):
                        self.select_level(2)
                    elif self.buttons.get("lvl3") and self.buttons["lvl3"].collidepoint(mouse_pos):
                        self.select_level(3)
                    elif self.buttons.get("back") and self.buttons["back"].collidepoint(mouse_pos):
                        self.state = GameState.MENU

                elif self.state == GameState.PAUSED:
                    if self.buttons.get("resume") and self.buttons["resume"].collidepoint(mouse_pos):
                        self.state = GameState.PLAYING
                        self.audio.play_music()
                    elif self.buttons.get("main_menu") and self.buttons["main_menu"].collidepoint(mouse_pos):
                        self.audio.stop_music()
                        self.state = GameState.MENU

            if self.state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.state == GameState.GAMEMODES_SELECT:
                self._handle_level_select_events(event)
            elif self.state == GameState.LEVEL_SELECT:
                self._handle_level_select_events(event)
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

    def _handle_level_select_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def _handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.audio.stop_music()
                self.state = GameState.PAUSED
            elif event.key == pygame.K_m:
                self.audio.toggle_mute()

    def _handle_paused_events(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.state = GameState.PLAYING
                self.audio.play_music()

            elif event.key == pygame.K_m:
                self.audio.toggle_mute()

    def _handle_game_over_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.buttons.get("restart") and self.buttons["restart"].collidepoint(mouse_pos):
                    self.score = 0
                    self.lives = PLAYER_LIVES
                    self.load_level(self.current_level)
                    self.state = GameState.PLAYING
                    self.audio.play_music()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.score = 0
                self.lives = PLAYER_LIVES
                self.load_level(self.current_level)
                self.state = GameState.PLAYING
                self.audio.play_music()
            elif event.key == pygame.K_ESCAPE:
                self.audio.stop_music()
                self.state = GameState.MENU

    def _handle_level_complete_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                if self.buttons.get("next_level") and self.buttons["next_level"].collidepoint(mouse_pos):
                    self.current_level += 1
                    self.lives = PLAYER_LIVES
                    self.load_level(self.current_level)
                    self.state = GameState.PLAYING

                if self.buttons.get("victory_menu") and self.buttons["victory_menu"].collidepoint(mouse_pos):
                    self.state = GameState.MENU

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_level < TOTAL_LEVELS:
                    self.current_level += 1
                    self.lives = PLAYER_LIVES
                    self.load_level(self.current_level)
                    self.state = GameState.PLAYING
                else:
                    self.state = GameState.MENU
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU

    def update(self, dt):
        if self.state != GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()
        if self.player:
            self.player.handle_input(keys)
            self.player.update(dt, self.game_map)

        flash = (
            self.frightened_active
            and self.frightened_timer <= FRIGHTENED_FLASH_TIME
            and int(self.frightened_timer * 6) % 2 == 0
        )

        for ghost in self.ghosts:
            ghost.update(
                dt,
                self.game_map,
                self.player,
                self.frightened_active,
                flash,
                self.ghosts
            )

        if self.food_manager and self.player:
            points, super_dots = self.food_manager.check_collisions(self.player)

            if points > 0:
                self.audio.play_sound("dot")

            self.score += int(points * self.score_multiplier)

            if super_dots > 0:
                self.frightened_timer = FRIGHTENED_DURATION
                self.ghost_eat_score = 200
                self.eaten_ghosts.clear()
                for ghost in self.ghosts:
                    ghost.allow_frightened_again()

            if self.food_manager.all_collected():
                elapsed = max(1.0, time.time() - self.level_start_time)
                self.level_time_bonus = min(MAX_TIME_BONUS, int(TIME_BONUS_BASE / elapsed))
                self.score += self.level_time_bonus
                self.state = GameState.LEVEL_COMPLETE

        if self.frightened_timer > 0:
            self.frightened_timer = max(0.0, self.frightened_timer - dt)

        for ghost in self.ghosts:
            if ghost.check_collision(self.player):
                if self.frightened_active and not ghost.ignore_frightened:
                    ghost_id = id(ghost)

                    if ghost_id not in self.eaten_ghosts:
                        self.score += int(self.ghost_eat_score * self.score_multiplier)
                        self.eaten_ghosts.add(ghost_id)
                        self.ghost_eat_score = min(self.ghost_eat_score * 2, 1600)
                        ghost.send_to_spawn()

                    continue

                if ghost.respawn_freeze_timer > 0:
                    continue

                self.lives -= 1

                if self.lives <= 0:
                    self.audio.play_sound("game_over")
                    self.audio.stop_music()
                    self.state = GameState.GAME_OVER
                else:
                    self.audio.play_sound("death")
                    self.player.reset_position()
                    for g in self.ghosts:
                        g.reset_position()

    def render(self):
        self.screen.fill(BLACK)

        if self.state == GameState.MENU:
            play_rect, gamemodes_rect, levels_rect, exit_rect = self.ui.draw_menu()
            self.buttons["play"] = play_rect
            self.buttons["gamemodes"] = gamemodes_rect
            self.buttons["levels"] = levels_rect
            self.buttons["exit"] = exit_rect

        elif self.state == GameState.GAMEMODES_SELECT:
            ol, hm, bm, b = self.ui.draw_gamemodes_menu()
            self.buttons["one_life"] = ol
            self.buttons["hard_mode"] = hm
            self.buttons["battle_mode"] = bm
            self.buttons["back"] = b

        elif self.state == GameState.LEVEL_SELECT:
            l1, l2, l3, b = self.ui.draw_levels_menu()
            self.buttons["lvl1"] = l1
            self.buttons["lvl2"] = l2
            self.buttons["lvl3"] = l3
            self.buttons["back"] = b

        elif self.state in (GameState.PLAYING, GameState.PAUSED):
            game_surface = self.screen.subsurface((0, 50, SCREEN_WIDTH, SCREEN_HEIGHT - 50))

            if self.game_map:
                self.game_map.render(game_surface)
            if self.food_manager:
                self.food_manager.render(game_surface)

            for ghost in self.ghosts:
                ghost.draw(game_surface)
#                ghost.draw_debug(self.screen)
            if self.player:
                self.player.draw(game_surface)

            self.ui.draw_hud(self.score, self.lives, self.score_multiplier)

            if self.state == GameState.PAUSED:
                resume_rect, menu_rect = self.ui.draw_pause()
                self.buttons["resume"] = resume_rect
                self.buttons["main_menu"] = menu_rect

        elif self.state == GameState.LEVEL_COMPLETE:
            next_rect, menu_rect = self.ui.draw_level_complete(self.current_level, self.score, self.level_time_bonus)
            self.buttons["next_level"] = next_rect
            self.buttons["victory_menu"] = menu_rect

        elif self.state == GameState.GAME_OVER:
            restart_rect = self.ui.draw_game_over(self.score)
            self.buttons["restart"] = restart_rect

        pygame.display.flip()