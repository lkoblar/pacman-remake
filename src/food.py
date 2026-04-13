import pygame
from src.settings import SCALED_TILE, DOT, SUPER_DOT, WHITE, YELLOW


class Dot:
    def __init__(self, grid_x, grid_y, sprite=None):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.collected = False
        self.sprite = sprite
        self.points = 10

    def get_rect(self):
        return pygame.Rect(
            self.grid_x * SCALED_TILE,
            self.grid_y * SCALED_TILE,
            SCALED_TILE, SCALED_TILE,
        )

    def draw(self, surface):
        if self.collected:
            return
        x = self.grid_x * SCALED_TILE + SCALED_TILE // 2
        y = self.grid_y * SCALED_TILE + SCALED_TILE // 2
        if self.sprite:
            surface.blit(self.sprite, (x, y))
        else:
            center = (x + SCALED_TILE // 2, y + SCALED_TILE // 2)
            pygame.draw.circle(surface, WHITE, center, SCALED_TILE // 6)


class SuperDot(Dot):
    def __init__(self, grid_x, grid_y, sprite=None):
        super().__init__(grid_x, grid_y, sprite)
        self.points = 50

    def draw(self, surface):
        if self.collected:
            return
        x = self.grid_x * SCALED_TILE + SCALED_TILE // 2
        y = self.grid_y * SCALED_TILE + SCALED_TILE // 2
        if self.sprite:
            surface.blit(self.sprite, (x, y))
        else:
            center = (x + SCALED_TILE // 2, y + SCALED_TILE // 2)
            pygame.draw.circle(surface, YELLOW, center, SCALED_TILE // 3)


class FoodManager:
    def __init__(self, game_map, sprite_loader):
        self.dots = []
        self._generate_from_map(game_map, sprite_loader)

    def _generate_from_map(self, game_map, sprite_loader):
        dot_sprite = sprite_loader.tile_sprites.get("dot")
        super_dot_sprite = sprite_loader.tile_sprites.get("super_dot")

        for row_idx, row in enumerate(game_map.grid):
            for col_idx, tile in enumerate(row):
                if tile == DOT:
                    self.dots.append(Dot(col_idx, row_idx, dot_sprite))
                elif tile == SUPER_DOT:
                    self.dots.append(SuperDot(col_idx, row_idx, super_dot_sprite))

    def check_collisions(self, player):
        points = 0
        player_rect = player.get_rect()
        for dot in self.dots:
            if not dot.collected and dot.get_rect().colliderect(player_rect):
                dot.collected = True
                points += dot.points
        return points

    def all_collected(self):
        return all(dot.collected for dot in self.dots)

    def render(self, surface):
        for dot in self.dots:
            dot.draw(surface)
