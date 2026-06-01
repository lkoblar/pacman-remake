import pygame
from src.settings import SCALED_TILE, SCALED_SPRITE, PLAYER_SPAWN, COLS, ROWS

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

CENTER_EPSILON = 0.5
HALF_OFFSET = (SCALED_SPRITE - SCALED_TILE) // 2


class Player:
    def __init__(self, game_map, sprite_loader):
        self.sprites = sprite_loader.pacman_sprites
        self.direction = "right"
        self.next_direction = "right"
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1

        spawn = game_map.get_spawn_position(PLAYER_SPAWN)
        if spawn:
            self.grid_x, self.grid_y = spawn
        else:
            self.grid_x, self.grid_y = 1, 1

        self.spawn_x = self.grid_x
        self.spawn_y = self.grid_y

        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)

        self.speed = SCALED_TILE * 4
        self.moving = False

    def handle_input(self, keys, controls=None):
        if controls is None:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.next_direction = "up"
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.next_direction = "down"
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.next_direction = "left"
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.next_direction = "right"
            return

        if keys[controls["up"]]:
            self.next_direction = "up"
        elif keys[controls["down"]]:
            self.next_direction = "down"
        elif keys[controls["left"]]:
            self.next_direction = "left"
        elif keys[controls["right"]]:
            self.next_direction = "right"

    def update(self, dt, game_map):
        self._move(dt, game_map)
        self._wrap_tunnel()
        self._update_animation(dt)

    def _at_tile_center(self):
        target_x = self.grid_x * SCALED_TILE
        target_y = self.grid_y * SCALED_TILE
        return (
            abs(self.pixel_x - target_x) <= CENTER_EPSILON
            and abs(self.pixel_y - target_y) <= CENTER_EPSILON
        )

    def _snap_to_center(self):
        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)

    def _can_move_from_tile(self, grid_x, grid_y, direction, game_map):
            if direction not in DIRECTION_VECTORS:
                return False
            dx, dy = DIRECTION_VECTORS[direction]
            
            target_x = grid_x + dx
            target_y = grid_y + dy
            if target_x < 0 or target_x >= COLS or target_y < 0 or target_y >= ROWS:
                return True
                
            return not game_map.is_wall(target_x, target_y)

    def _next_tile(self, direction):
        dx, dy = DIRECTION_VECTORS[direction]
        return self.grid_x + dx, self.grid_y + dy

    def _distance_to_next_center(self):
        dx, dy = DIRECTION_VECTORS[self.direction]
        if dx > 0:
            return ((self.grid_x + 1) * SCALED_TILE) - self.pixel_x
        if dx < 0:
            return self.pixel_x - ((self.grid_x - 1) * SCALED_TILE)
        if dy > 0:
            return ((self.grid_y + 1) * SCALED_TILE) - self.pixel_y
        if dy < 0:
            return self.pixel_y - ((self.grid_y - 1) * SCALED_TILE)
        return 0.0

    def _step(self, distance):
        dx, dy = DIRECTION_VECTORS[self.direction]
        self.pixel_x += dx * distance
        self.pixel_y += dy * distance

    def _move(self, dt, game_map):
        remaining = self.speed * dt
        self.moving = False

        if self._at_tile_center():
            self._snap_to_center()

        while remaining > 0:
            if self._at_tile_center():
                self._snap_to_center()

                if self._can_move_from_tile(self.grid_x, self.grid_y, self.next_direction, game_map):
                    self.direction = self.next_direction

                if not self._can_move_from_tile(self.grid_x, self.grid_y, self.direction, game_map):
                    self.moving = False
                    return

            distance_to_center = self._distance_to_next_center()
            if distance_to_center <= 0:
                distance_to_center = float(SCALED_TILE)

            step_distance = min(remaining, distance_to_center)
            self._step(step_distance)
            remaining -= step_distance
            self.moving = True

            if distance_to_center <= step_distance + CENTER_EPSILON:
                self.grid_x, self.grid_y = self._next_tile(self.direction)
                self._snap_to_center()

    def _wrap_tunnel(self):
            world_width = COLS * SCALED_TILE
            world_height = ROWS * SCALED_TILE

            # levo - desno teleportacija
            if self.pixel_x < -SCALED_TILE // 2:
                self.pixel_x += world_width
                self.grid_x = COLS - 1

            elif self.pixel_x >= world_width - SCALED_TILE // 2:
                self.pixel_x -= world_width
                self.grid_x = 0

            # zgoraj - spodaj teleportacija
            if self.pixel_y < -SCALED_TILE // 2:
                self.pixel_y += world_height
                self.grid_y = ROWS - 1

            elif self.pixel_y >= world_height - SCALED_TILE // 2:
                self.pixel_y -= world_height
                self.grid_y = 0

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
        self.animation_frame = 0
        self.animation_timer = 0.0

    def get_rect(self):
        return pygame.Rect(
            int(self.pixel_x),
            int(self.pixel_y),
            SCALED_TILE,
            SCALED_TILE,
        )

    def draw(self, surface):
        frames = self.sprites.get(self.direction, self.sprites.get("right"))
        if frames:
            frame = frames[int(self.animation_frame) % len(frames)]
            surface.blit(
                frame,
                (int(self.pixel_x) - HALF_OFFSET, int(self.pixel_y) - HALF_OFFSET),
            )
