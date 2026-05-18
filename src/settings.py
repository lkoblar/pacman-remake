import os
from enum import Enum, auto

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEVELS_DIR = os.path.join(BASE_DIR, "levels")

TILE_SIZE = 16
SCALE = 3
SCALED_TILE = TILE_SIZE * SCALE

COLS = 14
ROWS = 18
SCREEN_WIDTH = COLS * SCALED_TILE
SCREEN_HEIGHT = ROWS * SCALED_TILE

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

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    LEVEL_COMPLETE = auto()
    LEVEL_SELECT = auto()

WALL = "#"
DOT = "."
EMPTY = " "
SUPER_DOT = "O"
GHOST_SPAWN = "G"
PLAYER_SPAWN = "P"

PLAYER_LIVES = 3

FRIGHTENED_DURATION = 7.0