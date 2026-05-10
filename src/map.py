import pygame
from src.settings import (
    WALL,
    DOT,
    EMPTY,
    SUPER_DOT,
    GHOST_SPAWN,
    PLAYER_SPAWN,
    SCALED_TILE,
    COLS,
    ROWS,
    BLUE,
)

GRID_LINE_COLOR = (40, 40, 40)
OPEN_CENTER_COLOR = (255, 255, 255)
WALL_BORDER_COLOR = (0, 0, 180)


class Map:
    def __init__(self, level_path, sprite_loader=None):
        self.grid = []
        self.sprite_loader = sprite_loader
        self.show_debug = True
        self.load(level_path)

    def load(self, path):
        self.grid = []

        with open(path, "r") as f:
            for line in f:
                row = list(line.rstrip("\n"))
                while len(row) < COLS:
                    row.append(EMPTY)
                row = row[:COLS]
                self.grid.append(row)

        while len(self.grid) < ROWS:
            self.grid.append([EMPTY] * COLS)

        self.grid = self.grid[:ROWS]

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

    def render(self, surface):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                x = col_idx * SCALED_TILE
                y = row_idx * SCALED_TILE
                rect = pygame.Rect(x, y, SCALED_TILE, SCALED_TILE)

                if tile == WALL:
                    if self.sprite_loader and "wall" in self.sprite_loader.tile_sprites:
                        surface.blit(self.sprite_loader.tile_sprites["wall"], (x, y))
                    else:
                        pygame.draw.rect(surface, BLUE, rect)

                if self.show_debug:
                    pygame.draw.rect(surface, GRID_LINE_COLOR, rect, 1)

                    if tile == WALL:
                        pygame.draw.rect(surface, WALL_BORDER_COLOR, rect, 2)
                    else:
                        cx = x + SCALED_TILE // 2
                        cy = y + SCALED_TILE // 2
                        pygame.draw.circle(surface, OPEN_CENTER_COLOR, (cx, cy), 2)

    def count_dots(self):
        count = 0
        for row in self.grid:
            for tile in row:
                if tile in (DOT, SUPER_DOT):
                    count += 1
        return count
