import pygame
from src.settings import SCALED_TILE, SCALED_SPRITE, PLAYER_SPAWN


class Player:
    def __init__(self, game_map, sprite_loader):
        self.sprites = sprite_loader.pacman_sprites
        self.direction = "right"
        self.next_direction = "right"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        spawn = game_map.get_spawn_position(PLAYER_SPAWN)
        if spawn:
            self.grid_x, self.grid_y = spawn
        else:
            self.grid_x, self.grid_y = 14, 26

        self.spawn_x = self.grid_x
        self.spawn_y = self.grid_y
        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)

        self.speed = SCALED_TILE * 4
        self.moving = False

    def handle_input(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = "down"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = "right"

    def update(self, dt, game_map):
        pass

    def reset_position(self):
        self.grid_x = self.spawn_x
        self.grid_y = self.spawn_y
        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)
        self.direction = "right"
        self.next_direction = "right"
        self.moving = False

    def get_rect(self):
        return pygame.Rect(
            int(self.pixel_x), int(self.pixel_y),
            SCALED_SPRITE, SCALED_SPRITE,
        )

    def draw(self, surface):
        frames = self.sprites.get(self.direction, self.sprites.get("right"))
        if frames:
            frame = frames[int(self.animation_frame) % len(frames)]
            offset = (SCALED_SPRITE - SCALED_TILE) // 2
            surface.blit(frame, (int(self.pixel_x) - offset, int(self.pixel_y) - offset))
