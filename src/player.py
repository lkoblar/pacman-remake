import pygame
from src.settings import SCALED_TILE, SCALED_SPRITE, PLAYER_SPAWN, COLS

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

CENTER_EPSILON = 0.5


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
        self._maybe_change_direction(game_map)
        self._move(dt, game_map)
        self._wrap_tunnel()
        self._update_grid_position()
        self._update_animation(dt)

    def _at_tile_center(self):
        return (
            abs(self.pixel_x - round(self.pixel_x / SCALED_TILE) * SCALED_TILE) < CENTER_EPSILON
            and abs(self.pixel_y - round(self.pixel_y / SCALED_TILE) * SCALED_TILE) < CENTER_EPSILON
        )

    def _snap_to_center(self):
        self.pixel_x = float(round(self.pixel_x / SCALED_TILE) * SCALED_TILE)
        self.pixel_y = float(round(self.pixel_y / SCALED_TILE) * SCALED_TILE)

    def _can_move(self, direction, game_map):
        if direction not in DIRECTION_VECTORS:
            return False
        dx, dy = DIRECTION_VECTORS[direction]
        col = int(round(self.pixel_x / SCALED_TILE)) + dx
        row = int(round(self.pixel_y / SCALED_TILE)) + dy
        return not game_map.is_wall(col, row)

    def _maybe_change_direction(self, game_map):
        if not self._at_tile_center():
            return
        if self.next_direction == self.direction:
            return
        if self._can_move(self.next_direction, game_map):
            self._snap_to_center()
            self.direction = self.next_direction

    def _distance_to_next_center(self):
        dx, dy = DIRECTION_VECTORS[self.direction]
        if dx > 0:
            next_center = (int(self.pixel_x // SCALED_TILE) + 1) * SCALED_TILE
            return next_center - self.pixel_x
        if dx < 0:
            next_center = (int((self.pixel_x - 1) // SCALED_TILE)) * SCALED_TILE
            return self.pixel_x - next_center
        if dy > 0:
            next_center = (int(self.pixel_y // SCALED_TILE) + 1) * SCALED_TILE
            return next_center - self.pixel_y
        if dy < 0:
            next_center = (int((self.pixel_y - 1) // SCALED_TILE)) * SCALED_TILE
            return self.pixel_y - next_center
        return 0.0

    def _step(self, distance):
        dx, dy = DIRECTION_VECTORS[self.direction]
        self.pixel_x += dx * distance
        self.pixel_y += dy * distance

    def _move(self, dt, game_map):
        if self._at_tile_center() and not self._can_move(self.direction, game_map):
            self._snap_to_center()
            self.moving = False
            return

        remaining = self.speed * dt
        self.moving = True

        while remaining > 0:
            if self._at_tile_center():
                self._maybe_change_direction(game_map)
                if not self._can_move(self.direction, game_map):
                    self._snap_to_center()
                    self.moving = False
                    return

            distance_to_center = self._distance_to_next_center()
            if distance_to_center <= 0:
                distance_to_center = float(SCALED_TILE)

            if remaining < distance_to_center:
                self._step(remaining)
                remaining = 0
            else:
                self._step(distance_to_center)
                remaining -= distance_to_center
                self._snap_to_center()

    def _wrap_tunnel(self):
        world_width = COLS * SCALED_TILE
        if self.pixel_x < -SCALED_TILE:
            self.pixel_x += world_width
        elif self.pixel_x >= world_width:
            self.pixel_x -= world_width

    def _update_grid_position(self):
        self.grid_x = int(round(self.pixel_x / SCALED_TILE))
        self.grid_y = int(round(self.pixel_y / SCALED_TILE))

    def _update_animation(self, dt):
        if not self.moving:
            return
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.animation_frame = (self.animation_frame + 1) % 4

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
