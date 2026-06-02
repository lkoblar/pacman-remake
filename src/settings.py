import os
from enum import Enum, auto

import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEVELS_DIR = os.path.join(BASE_DIR, "levels")

TILE_SIZE = 16
SCALE = 3
SCALED_TILE = TILE_SIZE * SCALE

COLS = 14
ROWS = 18
SCREEN_WIDTH = COLS * SCALED_TILE
SCREEN_HEIGHT = (ROWS * SCALED_TILE) + 50

SPRITE_SIZE = 16
SCALED_SPRITE = SPRITE_SIZE * SCALE

FPS = 60

BLACK = (0, 0, 0)
BLUE = (35, 61, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 49, 49)
CYAN = (92, 225, 230)
MAGENTA = (226, 169, 241)
ORANGE = (255, 145, 77)
GREEN = (80, 220, 100)
GRAY = (120, 120, 120)

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    LEVEL_COMPLETE = auto()
    LEVEL_SELECT = auto()
    LEVEL_DIFFICULTY = auto()
    MULTIPLAYER_MODE_SELECT = auto()
    MULTIPLAYER_DIFFICULTY = auto()
    COOP_CONFIG = auto()
    MULTIPLAYER_READY = auto()
    MULTIPLAYER_PLAYING = auto()
    MULTIPLAYER_PAUSED = auto()
    MULTIPLAYER_COUNTDOWN = auto()
    MULTIPLAYER_RESULT = auto()

WALL = "#"
DOT = "."
EMPTY = " "
SUPER_DOT = "O"
GHOST_SPAWN = "G"
PLAYER_SPAWN = "P"

PLAYER_LIVES = 3
TOTAL_LEVELS = 3
FRIGHTENED_DURATION = 7.0

FRIGHTENED_FLASH_TIME = 2.0

LIVES_SCORE_MULTIPLIERS = {5: 1.5, 4: 1.5, 3: 1.5, 2: 1.0, 1: 0.5}
TIME_BONUS_BASE = 30000
MAX_TIME_BONUS = 2000

CONTROLS_WASD = {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
CONTROLS_ARROWS = {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

P1_READY_KEY = pygame.K_SPACE
P2_READY_KEY = pygame.K_RETURN

MP_DIVIDER = 4
MP_SCREEN_WIDTH = SCREEN_WIDTH * 2 + MP_DIVIDER
MP_LEVEL = 1

MP_DIFFICULTIES = {
    "EASY":   {"lives": 5, "player_speed": 1.0,  "ghost_speed": 0.8},
    "NORMAL": {"lives": 3, "player_speed": 1.0,  "ghost_speed": 1.0},
    "HARD":   {"lives": 1, "player_speed": 1.15, "ghost_speed": 1.2},
}
MP_DEFAULT_DIFFICULTY = "NORMAL"

COOP_LEVEL = "coop1"
COOP_COLS = 21
COOP_ROWS = 19
COOP_SCREEN_WIDTH = COOP_COLS * SCALED_TILE
COOP_SCREEN_HEIGHT = COOP_ROWS * SCALED_TILE + 50
COOP_LIVES = 3
COOP_P1_TINT = None
COOP_P2_TINT = (0, 230, 0)

COOP_LIVES_OPTIONS = (1, 3, 5)
COOP_LIVES_MODES = ("separate", "shared")
COOP_DIFFICULTIES = {
    "EASY":   {"ghost_speed": 0.8},
    "NORMAL": {"ghost_speed": 1.0},
    "HARD":   {"ghost_speed": 1.2},
}
COOP_DEFAULT_DIFFICULTY = "NORMAL"
COOP_DEFAULT_LIVES = 3
COOP_DEFAULT_LIVES_MODE = "separate"

DIFFICULTY_PRESETS = {
    "Easy":   {"ghost_speed_mult": 2.0, "frightened_duration": 10.0, "respawn_freeze": 1.5},
    "Normal": {"ghost_speed_mult": 3.0, "frightened_duration": 7.0,  "respawn_freeze": 0.75},
    "Hard":   {"ghost_speed_mult": 4.0, "frightened_duration": 4.0,  "respawn_freeze": 0.3},
}

SP_DIFFICULTIES = {
    "EASY":   {"preset": "Easy",   "lives": 5},
    "NORMAL": {"preset": "Normal", "lives": 3},
    "HARD":   {"preset": "Hard",   "lives": 1},
}
SP_DEFAULT_DIFFICULTY = "NORMAL"
