import random
import pygame

from src.settings import GHOST_SPAWN, SCALED_TILE, SCALED_SPRITE, COLS, ROWS

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

CENTER_EPSILON = 0.5
HALF_OFFSET = (SCALED_SPRITE - SCALED_TILE) // 2


class Ghost:
    def __init__(self, grid_x, grid_y, sprite=None):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.spawn_x = grid_x
        self.spawn_y = grid_y

        self.pixel_x = float(grid_x * SCALED_TILE)
        self.pixel_y = float(grid_y * SCALED_TILE)

        self.sprite = sprite
        self.speed = SCALED_TILE * 3
        self.direction = random.choice(list(DIRECTION_VECTORS.keys()))

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
        self.spawn_y = self.spawn_y
        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)
        self.direction = random.choice(list(DIRECTION_VECTORS.keys()))

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
        dx, dy = DIRECTION_VECTORS[direction]
        target_x = grid_x + dx
        target_y = grid_y + dy

        if target_x < 0 or target_x >= COLS or target_y < 0 or target_y >= ROWS:
            return True

        return not game_map.is_wall(target_x, target_y)

    def _next_tile(self, direction):
        dx, dy = DIRECTION_VECTORS[direction]
        return self.grid_x + dx, self.grid_y + dy

    def _valid_directions(self, game_map):
        valid = []
        for direction in DIRECTION_VECTORS:
            if self._can_move_from_tile(self.grid_x, self.grid_y, direction, game_map):
                valid.append(direction)
        return valid

    def _choose_direction(self, game_map):
        
        if self.grid_x < 0 or self.grid_x >= COLS or self.grid_y < 0 or self.grid_y >= ROWS:
            return

        valid = self._valid_directions(game_map)
        if not valid:
            return

        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        reverse = opposites[self.direction]

        non_reverse = [d for d in valid if d != reverse]

        if self.direction in valid and len(valid) == 1:
            return
        if self.direction in valid and len(non_reverse) == 0:
            return

        choices = non_reverse if non_reverse else valid
        if self.direction in choices and len(choices) > 1:
            choices = [d for d in choices if d != self.direction] or choices

        self.direction = random.choice(choices)

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

    def _wrap_tunnel(self):
        world_width = COLS * SCALED_TILE
        world_height = ROWS * SCALED_TILE

        if self.pixel_x < -SCALED_TILE // 2:
            self.pixel_x += world_width
            self.grid_x = COLS - 1
        elif self.pixel_x >= world_width - SCALED_TILE // 2:
            self.pixel_x -= world_width
            self.grid_x = 0

        if self.pixel_y < -SCALED_TILE // 2:
            self.pixel_y += world_height
            self.grid_y = ROWS - 1
        elif self.pixel_y >= world_height - SCALED_TILE // 2:
            self.pixel_y -= world_height
            self.grid_y = 0

    def update(self, dt, game_map, player=None):
        remaining = self.speed * dt

        if self._at_tile_center():
            self._snap_to_center()
            if not self._can_move_from_tile(self.grid_x, self.grid_y, self.direction, game_map):
                self._choose_direction(game_map)

        while remaining > 0:
            if self._at_tile_center():
                self._snap_to_center()
                if not self._can_move_from_tile(self.grid_x, self.grid_y, self.direction, game_map):
                    self._choose_direction(game_map)
                    if not self._can_move_from_tile(self.grid_x, self.grid_y, self.direction, game_map):
                        return

            distance_to_center = self._distance_to_next_center()
            if distance_to_center <= 0:
                distance_to_center = float(SCALED_TILE)

            step_distance = min(remaining, distance_to_center)
            self._step(step_distance)
            remaining -= step_distance

            if distance_to_center <= step_distance + CENTER_EPSILON:
                self.grid_x, self.grid_y = self._next_tile(self.direction)
                self._snap_to_center()

                if 0 <= self.grid_x < COLS and 0 <= self.grid_y < ROWS:
                    valid = self._valid_directions(game_map)
                    if len(valid) >= 3:
                        self._choose_direction(game_map)

        self._wrap_tunnel()

    def get_rect(self):
        return pygame.Rect(
            int(self.pixel_x),
            int(self.pixel_y),
            SCALED_TILE,
            SCALED_TILE,
        )

    def check_collision(self, player):
        return self.get_rect().colliderect(player.get_rect())

    def draw(self, surface):
        draw_x = int(self.pixel_x) - HALF_OFFSET
        draw_y = int(self.pixel_y) - HALF_OFFSET

        if self.sprite:
            surface.blit(self.sprite, (draw_x, draw_y))
        else:
            pygame.draw.rect(
                surface,
                (255, 0, 0),
                (int(self.pixel_x), int(self.pixel_y), SCALED_TILE, SCALED_TILE),
            )