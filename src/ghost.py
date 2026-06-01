import random
import pygame
import math

from src.settings import GHOST_SPAWN, SCALED_TILE, SCALED_SPRITE, COLS, ROWS, BLUE, WHITE

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

CENTER_EPSILON = 0.5
HALF_OFFSET = (SCALED_SPRITE - SCALED_TILE) // 2
RESPAWN_FREEZE_DURATION = 0.75


class Ghost:
    def __init__(self, grid_x, grid_y, name="ghost", sprite=None):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.spawn_x = grid_x
        self.spawn_y = grid_y

        self.pixel_x = float(grid_x * SCALED_TILE)
        self.pixel_y = float(grid_y * SCALED_TILE)

        self.name = name  # shranimo ime duhca za algoritme
        self.sprite = sprite
        self.frightened_sprite = pygame.transform.scale(
            pygame.image.load("assets/ghosts/blue_ghost.png").convert_alpha(),
            (SCALED_SPRITE, SCALED_SPRITE),
        )

        self.speed = SCALED_TILE * 3
        self.normal_speed = SCALED_TILE * 3
        self.frightened_speed = SCALED_TILE * 1.5

        self.is_frightened = False
        self.flash_white = False
        self.ignore_frightened = False
        self.respawn_freeze_timer = 0.0

        self.direction = random.choice(list(DIRECTION_VECTORS.keys()))
        
        self.current_target = (grid_x, grid_y)

    @classmethod
    def create_from_map(cls, game_map, sprite_loader):
        ghosts = []
        positions = game_map.get_all_positions(GHOST_SPAWN)

        sprite_names = ["blinky", "pinky", "inky", "clyde"]

        for i, (x, y) in enumerate(positions):
            sprite = None
            name = sprite_names[i % len(sprite_names)]
            
            if sprite_loader and hasattr(sprite_loader, "ghost_sprites"):
                name = sprite_names[i % len(sprite_names)]
                sprite = sprite_loader.ghost_sprites.get(name)
            
            ghosts.append(cls(x, y, name, sprite))

        return ghosts

    def reset_position(self):
        self.grid_x = self.spawn_x
        self.grid_y = self.spawn_y
        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)
        self.direction = random.choice(list(DIRECTION_VECTORS.keys()))
        self.is_frightened = False
        self.flash_white = False
        self.ignore_frightened = False
        self.respawn_freeze_timer = 0.0
        self.current_target = (self.spawn_x, self.spawn_y)

    def send_to_spawn(self):
        self.grid_x = self.spawn_x
        self.grid_y = self.spawn_y
        self.pixel_x = float(self.grid_x * SCALED_TILE)
        self.pixel_y = float(self.grid_y * SCALED_TILE)
        self.direction = random.choice(list(DIRECTION_VECTORS.keys()))
        self.is_frightened = False
        self.flash_white = False
        self.ignore_frightened = True
        self.respawn_freeze_timer = RESPAWN_FREEZE_DURATION
        self.current_target = (self.spawn_x, self.spawn_y)

    def allow_frightened_again(self):
        self.ignore_frightened = False

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

    def _choose_direction(self, game_map, player=None, all_ghosts=None):
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
        choices = [d for d in valid if d != reverse]

        if not choices:
            choices = valid

        if player:
            player_rect = player.get_rect()
            p_x = player_rect.centerx // SCALED_TILE
            p_y = player_rect.centery // SCALED_TILE

            # blinky direkt na igralca
            if self.name == "blinky":
                self.current_target = (p_x, p_y)

            # pinky 4 polja naprej od igralca 
            elif self.name == "pinky":
                p_dir = getattr(player, "direction", "left")
                p_dx, p_dy = DIRECTION_VECTORS.get(p_dir, (0, 0))
                self.current_target = (p_x + (p_dx * 4), p_y + (p_dy * 4))

            # inky vektor od blinky skozi player pivot
            elif self.name == "inky" and all_ghosts:
                blinky = next((g for g in all_ghosts if g.name == "blinky"), None)
                if blinky:
                    p_dir = getattr(player, "direction", "left")
                    p_dx, p_dy = DIRECTION_VECTORS.get(p_dir, (0, 0))
                    
                    pivot_x = p_x + (p_dx * 2)
                    pivot_y = p_y + (p_dy * 2)

                    vec_x = pivot_x - blinky.grid_x
                    vec_y = pivot_y - blinky.grid_y

                    tx = pivot_x + vec_x
                    ty = pivot_y + vec_y
                    
                    self.current_target = (max(0, min(COLS - 1, tx)), max(0, min(ROWS - 1, ty)))
                else:
                    self.current_target = (p_x, p_y)

            # clyde evklidska razdalja do Pac-Mana
            elif self.name == "clyde":
                distance = math.sqrt((self.grid_x - p_x) ** 2 + (self.grid_y - p_y) ** 2)
                if distance > 8:
                    self.current_target = (p_x, p_y)
                else:
                    self.current_target = (self.spawn_x, self.spawn_y)

        if player:
            tx, ty = self.current_target
            best_direction = choices[0]
            min_distance = float('inf')

            for direction in choices:
                next_x, next_y = self._next_tile(direction)
                distance = math.sqrt((next_x - tx) ** 2 + (next_y - ty) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction
        
            self.direction = best_direction
            
        else:
            if self.direction in valid and len(valid) == 1:
                return
            if self.direction in valid and len(choices) == 0:
                return

            if self.direction in choices and len(choices) > 1:
                choices = [d for d in choices if d != self.direction] or choices

            self.direction = random.choice(choices)

    def _choose_frightened_direction(self, game_map, player):
        if not player:
            self._choose_direction(game_map)
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
        choices = [d for d in valid if d != reverse]

        if not choices:
            choices = valid

        player_rect = player.get_rect()
        p_x = player_rect.centerx // SCALED_TILE
        p_y = player_rect.centery // SCALED_TILE

        # vsi stirje koti
        corners = [
            (0, 0),             # Zgoraj levo
            (COLS - 1, 0),      # Zgoraj desno
            (0, ROWS - 1),      # Spodaj levo
            (COLS - 1, ROWS - 1)# Spodaj desno
        ]

        # kot ki je najdlje od playera
        best_corner = corners[0]
        max_corner_dist = -1

        for cx, cy in corners:
            dist_to_player = math.sqrt((cx - p_x) ** 2 + (cy - p_y) ** 2)
            if dist_to_player > max_corner_dist:
                max_corner_dist = dist_to_player
                best_corner = (cx, cy)

        # nastavi kot kot tarco
        self.current_target = best_corner
        tx, ty = self.current_target

        # iskanje best path
        best_direction = choices[0]
        min_distance = float('inf')

        for direction in choices:
            next_x, next_y = self._next_tile(direction)
            distance = math.sqrt((next_x - tx) ** 2 + (next_y - ty) ** 2)
            if distance < min_distance:
                min_distance = distance
                best_direction = direction

        self.direction = best_direction

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

    def update(self, dt, game_map, player=None, frightened=False, flash=False, all_ghosts=None):
        active_frightened = frightened and not self.ignore_frightened

        self.is_frightened = active_frightened
        self.flash_white = flash if active_frightened else False
        self.speed = self.frightened_speed if active_frightened else self.normal_speed

        if self.respawn_freeze_timer > 0:
            self.respawn_freeze_timer = max(0.0, self.respawn_freeze_timer - dt)
            return

        remaining = self.speed * dt

        if self._at_tile_center():
            self._snap_to_center()
            if not self._can_move_from_tile(self.grid_x, self.grid_y, self.direction, game_map):
                if self.is_frightened:
                    self._choose_frightened_direction(game_map, player)
                else:
                    self._choose_direction(game_map, player, all_ghosts)

        while remaining > 0:
            if self._at_tile_center():
                self._snap_to_center()
                if not self._can_move_from_tile(self.grid_x, self.grid_y, self.direction, game_map):
                    if self.is_frightened:
                        self._choose_frightened_direction(game_map, player)
                    else:
                        self._choose_direction(game_map, player, all_ghosts)

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
                        if self.is_frightened:
                            self._choose_frightened_direction(game_map, player)
                        else:
                            self._choose_direction(game_map, player, all_ghosts)

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

        if self.is_frightened and self.frightened_sprite:
            frightened_sprite = self.frightened_sprite.copy()

            if self.flash_white:
                frightened_sprite.fill(WHITE, special_flags=pygame.BLEND_ADD)

            surface.blit(frightened_sprite, (draw_x, draw_y))
        elif self.is_frightened:
            pygame.draw.rect(
                surface,
                BLUE,
                (int(self.pixel_x), int(self.pixel_y), SCALED_TILE, SCALED_TILE),
            )
        elif self.sprite:
            surface.blit(self.sprite, (draw_x, draw_y))
        else:
            pygame.draw.rect(
                surface,
                (255, 0, 0),
                (int(self.pixel_x), int(self.pixel_y), SCALED_TILE, SCALED_TILE),
            )

    def draw_debug(self, surface):
        if not hasattr(self, "current_target"):
            return

        if self.is_frightened:
            color = (0, 0, 255)
        else:
            colors = {
                "blinky": (255, 0, 0),
                "pinky": (255, 182, 193),
                "inky": (0, 255, 255),
                "clyde": (255, 165, 0)
            }
            color = colors.get(self.name, (255, 255, 255))

        tx, ty = self.current_target

        pygame.draw.rect(
            surface,
            color,
            (tx * SCALED_TILE + 2, ty * SCALED_TILE + 2, SCALED_TILE - 4, SCALED_TILE - 4),
            2
        )

        start_pixel = (
            int(self.pixel_x) + SCALED_TILE // 2,
            int(self.pixel_y) + SCALED_TILE // 2
        )
        end_pixel = (
            tx * SCALED_TILE + SCALED_TILE // 2,
            ty * SCALED_TILE + SCALED_TILE // 2
        )
        pygame.draw.line(surface, color, start_pixel, end_pixel, 1)
