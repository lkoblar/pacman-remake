import pygame
from src.settings import (
    WALL, DOT, EMPTY, SUPER_DOT, GHOST_SPAWN, PLAYER_SPAWN,
    SCALED_TILE, COLS, ROWS, BLUE,
)

GRID_LINE_COLOR = (40, 40, 40)
CENTER_DOT_COLOR = (255, 255, 255)
WALL_DEBUG_COLOR = (0, 255, 255)
GHOST_SPAWN_DEBUG_COLOR = (255, 0, 255)
PLAYER_SPAWN_DEBUG_COLOR = (255, 255, 0)
LABEL_COLOR = (180, 180, 180)


class Map:
    def __init__(self, level_path, sprite_loader=None, debug=False):
        self.grid = []
        self.cols = COLS
        self.rows = ROWS
        self.sprite_loader = sprite_loader
        self.debug = debug
        self.debug_font = None
        self.load(level_path)

    def load(self, path):
        self.grid = []
        with open(path, "r") as f:
            lines = [line.rstrip("\n") for line in f]

        while lines and lines[-1].strip() == "":
            lines.pop()

        if not lines:
            lines = [""]

        self.rows = len(lines)
        self.cols = max(len(line) for line in lines)

        for line in lines:
            row = list(line)
            while len(row) < self.cols:
                row.append(EMPTY)
            self.grid.append(row)

    def toggle_debug(self):
        self.debug = not self.debug

    def set_debug(self, enabled):
        self.debug = bool(enabled)

    def get_tile(self, col, row):
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row]):
            return self.grid[row][col]
        return WALL

    def is_wall(self, col, row):
        return self.get_tile(col, row) == WALL

    def set_tile(self, col, row, value):
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row]):
            self.grid[row][col] = value

    def get_spawn_position(self, tile_type):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                if tile == tile_type:
                    return (col_idx, row_idx)
        return None

    def get_all_positions(self, tile_type):
        positions = []
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                if tile == tile_type:
                    positions.append((col_idx, row_idx))
        return positions

    def _ensure_debug_font(self):
        if self.debug_font is None:
            self.debug_font = pygame.font.SysFont(None, max(14, SCALED_TILE // 3))

    def _draw_debug_overlay(self, surface):
        self._ensure_debug_font()

        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                x = col_idx * SCALED_TILE
                y = row_idx * SCALED_TILE
                rect = pygame.Rect(x, y, SCALED_TILE, SCALED_TILE)

                pygame.draw.rect(surface, GRID_LINE_COLOR, rect, 1)

                cx = x + SCALED_TILE // 2
                cy = y + SCALED_TILE // 2

                if tile == WALL:
                    pygame.draw.rect(surface, WALL_DEBUG_COLOR, rect, 2)
                else:
                    pygame.draw.circle(surface, CENTER_DOT_COLOR, (cx, cy), max(2, SCALED_TILE // 16))

                if tile == GHOST_SPAWN:
                    pygame.draw.circle(
                        surface,
                        GHOST_SPAWN_DEBUG_COLOR,
                        (cx, cy),
                        max(6, SCALED_TILE // 8),
                        2,
                    )
                elif tile == PLAYER_SPAWN:
                    pygame.draw.circle(
                        surface,
                        PLAYER_SPAWN_DEBUG_COLOR,
                        (cx, cy),
                        max(6, SCALED_TILE // 8),
                        2,
                    )

                label_text = tile if tile != EMPTY else "·"
                label = self.debug_font.render(label_text, True, LABEL_COLOR)
                surface.blit(label, (x + 2, y + 2))

    def render(self, surface):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                x = col_idx * SCALED_TILE
                y = row_idx * SCALED_TILE

                if tile == WALL:
                    if self.sprite_loader and "wall" in self.sprite_loader.tile_sprites:
                        wall_sprite = self.sprite_loader.tile_sprites["wall"]
                        if wall_sprite.get_width() != SCALED_TILE or wall_sprite.get_height() != SCALED_TILE:
                            wall_sprite = pygame.transform.scale(wall_sprite, (SCALED_TILE, SCALED_TILE))
                        surface.blit(wall_sprite, (x, y))
                    else:
                        pygame.draw.rect(surface, BLUE, (x, y, SCALED_TILE, SCALED_TILE))

        if self.debug:
            self._draw_debug_overlay(surface)

    def count_dots(self):
        count = 0
        for row in self.grid:
            for tile in row:
                if tile in (DOT, SUPER_DOT):
                    count += 1
        return count
