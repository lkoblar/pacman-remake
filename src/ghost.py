import pygame
from src.settings import SCALED_TILE, SCALED_SPRITE, GHOST_SPAWN


class Ghost:
    GHOST_NAMES = ["blinky", "pinky", "inky", "clyde"]

    def __init__(self, grid_x, grid_y, sprite, name):
        self.name = name
        self.sprite = sprite
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.spawn_x = grid_x
        self.spawn_y = grid_y
        self.pixel_x = float(grid_x * SCALED_TILE)
        self.pixel_y = float(grid_y * SCALED_TILE)
        self.direction = "up"
        self.speed = SCALED_TILE * 3
        self.vulnerable = False

    @classmethod
    def create_from_map(cls, game_map, sprite_loader):
        ghosts = []
        spawn_positions = game_map.get_all_positions(GHOST_SPAWN)

        for i, (gx, gy) in enumerate(spawn_positions):
            if i < len(cls.GHOST_NAMES):
                name = cls.GHOST_NAMES[i]
            else:
                name = cls.GHOST_NAMES[i % len(cls.GHOST_NAMES)]

            sprite = sprite_loader.ghost_sprites.get(name)
            ghost = cls(gx, gy, sprite, name)
            ghosts.append(ghost)

        return ghosts

    def update(self, dt, game_map, player):
        pass

    def check_collision(self, player):
        if player is None:
            return False
        ghost_rect = self.get_rect()
        player_rect = player.get_rect()
        return ghost_rect.colliderect(player_rect)

    def reset_position(self):
        self.grid_x = self.spawn_x
        self.grid_y = self.spawn_y
        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)
        self.vulnerable = False

    def get_rect(self):
        return pygame.Rect(
            int(self.pixel_x), int(self.pixel_y),
            SCALED_SPRITE, SCALED_SPRITE,
        )

    def draw(self, surface):
        if self.sprite:
            offset = (SCALED_SPRITE - SCALED_TILE) // 2
            surface.blit(self.sprite, (int(self.pixel_x) - offset, int(self.pixel_y) - offset))
