import random
import pygame

from src.settings import GHOST_SPAWN, SCALED_TILE, SCALED_SPRITE


class Ghost:
    def __init__(self, grid_x, grid_y, sprite=None):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.spawn_x = grid_x
        self.spawn_y = grid_y

        self.pixel_x = grid_x * SCALED_TILE
        self.pixel_y = grid_y * SCALED_TILE

        self.sprite = sprite
        self.speed = 2
        self.direction = random.choice(["up", "down", "left", "right"])

    @classmethod
    def create_from_map(cls, game_map, sprite_loader):
        ghosts = []
        positions = game_map.get_all_positions(GHOST_SPAWN)

        sprite_names = ["blinky", "pinky", "inky", "clyde"]

        for i, (x, y) in enumerate(positions):
            sprite = None
            if sprite_loader and hasattr(sprite_loader, "ghost_sprites"):
                name = sprite_names[i % len(sprite_names)]
                sprite = sprite_loader.ghost_sprites.get(name)
            ghosts.append(cls(x, y, sprite))

        return ghosts

    def reset_position(self):
        self.grid_x = self.spawn_x
        self.grid_y = self.spawn_y
        self.pixel_x = self.grid_x * SCALED_TILE
        self.pixel_y = self.grid_y * SCALED_TILE
        self.direction = random.choice(["up", "down", "left", "right"])

    def update(self, dt, game_map, player=None):
        old_x = self.pixel_x
        old_y = self.pixel_y

        if self.direction == "up":
            self.pixel_y -= self.speed
        elif self.direction == "down":
            self.pixel_y += self.speed
        elif self.direction == "left":
            self.pixel_x -= self.speed
        elif self.direction == "right":
            self.pixel_x += self.speed

        new_grid_x = int(round(self.pixel_x / SCALED_TILE))
        new_grid_y = int(round(self.pixel_y / SCALED_TILE))

        if game_map.is_wall(new_grid_x, new_grid_y):
            self.pixel_x = old_x
            self.pixel_y = old_y
            self.direction = random.choice(["up", "down", "left", "right"])
        else:
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y

    def get_rect(self):
        return pygame.Rect(
            int(self.pixel_x),
            int(self.pixel_y),
            SCALED_SPRITE,
            SCALED_SPRITE,
        )

    def check_collision(self, player):
        return self.get_rect().colliderect(player.get_rect())

    def draw(self, surface):
        offset = (SCALED_SPRITE - SCALED_TILE) // 2

        if self.sprite:
            surface.blit(self.sprite, (int(self.pixel_x) - offset, int(self.pixel_y) - offset))
        else:
            pygame.draw.rect(
                surface,
                (255, 0, 0),
                (int(self.pixel_x), int(self.pixel_y), SCALED_TILE, SCALED_TILE),
            )