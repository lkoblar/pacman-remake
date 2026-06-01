import os
import time
import math

from src.settings import (
    LEVELS_DIR,
    FRIGHTENED_DURATION,
    FRIGHTENED_FLASH_TIME,
    LIVES_SCORE_MULTIPLIERS,
    TIME_BONUS_BASE,
    MAX_TIME_BONUS,
    MP_DIFFICULTIES,
    MP_DEFAULT_DIFFICULTY,
    COOP_LIVES,
    COOP_P1_TINT,
    COOP_P2_TINT,
)
from src.map import Map
from src.player import Player
from src.ghost import Ghost
from src.food import FoodManager


class PlayerWorld:
    def __init__(self, level_num, sprite_loader, controls, label, difficulty=MP_DEFAULT_DIFFICULTY):
        self.sprite_loader = sprite_loader
        self.controls = controls
        self.label = label
        self.difficulty = difficulty

        level_path = os.path.join(LEVELS_DIR, f"level{level_num}.txt")
        if not os.path.exists(level_path):
            level_path = os.path.join(LEVELS_DIR, "level1.txt")

        self.game_map = Map(level_path, sprite_loader)
        self.player = Player(self.game_map, sprite_loader)
        self.ghosts = Ghost.create_from_map(self.game_map, sprite_loader)
        self.food_manager = FoodManager(self.game_map, sprite_loader)

        cfg = MP_DIFFICULTIES.get(difficulty, MP_DIFFICULTIES[MP_DEFAULT_DIFFICULTY])

        self.score = 0
        self.lives = cfg["lives"]

        self.player.speed *= cfg["player_speed"]
        for ghost in self.ghosts:
            ghost.normal_speed *= cfg["ghost_speed"]
            ghost.frightened_speed *= cfg["ghost_speed"]
            ghost.speed = ghost.normal_speed

        self.frightened_timer = 0.0
        self.ghost_eat_score = 200
        self.eaten_ghosts = set()

        self.level_start_time = time.time()
        self.time_bonus = 0

        self.finished = False
        self.finish_reason = None

    @property
    def frightened_active(self):
        return self.frightened_timer > 0

    @property
    def score_multiplier(self):
        return LIVES_SCORE_MULTIPLIERS.get(self.lives, 0.5)

    def update(self, dt, keys, audio):
        if self.finished:
            return

        self.player.handle_input(keys, self.controls)
        self.player.update(dt, self.game_map)

        flash = (
            self.frightened_active
            and self.frightened_timer <= FRIGHTENED_FLASH_TIME
            and int(self.frightened_timer * 6) % 2 == 0
        )

        for ghost in self.ghosts:
            ghost.update(
                dt,
                self.game_map,
                self.player,
                self.frightened_active,
                flash,
                self.ghosts,
            )

        points, super_dots = self.food_manager.check_collisions(self.player)

        if points > 0:
            audio.play_sound("dot")

        self.score += int(points * self.score_multiplier)

        if super_dots > 0:
            self.frightened_timer = FRIGHTENED_DURATION
            self.ghost_eat_score = 200
            self.eaten_ghosts.clear()
            for ghost in self.ghosts:
                ghost.allow_frightened_again()

        if self.food_manager.all_collected():
            elapsed = max(1.0, time.time() - self.level_start_time)
            self.time_bonus = min(MAX_TIME_BONUS, int(TIME_BONUS_BASE / elapsed))
            self.score += self.time_bonus
            self.finished = True
            self.finish_reason = "cleared"
            return

        if self.frightened_timer > 0:
            self.frightened_timer = max(0.0, self.frightened_timer - dt)

        for ghost in self.ghosts:
            if ghost.check_collision(self.player):
                if self.frightened_active and not ghost.ignore_frightened:
                    ghost_id = id(ghost)

                    if ghost_id not in self.eaten_ghosts:
                        self.score += int(self.ghost_eat_score * self.score_multiplier)
                        self.eaten_ghosts.add(ghost_id)
                        self.ghost_eat_score = min(self.ghost_eat_score * 2, 1600)
                        ghost.send_to_spawn()

                    continue

                if ghost.respawn_freeze_timer > 0:
                    continue

                self.lives -= 1

                if self.lives <= 0:
                    audio.play_sound("death")
                    self.finished = True
                    self.finish_reason = "dead"
                    return
                else:
                    audio.play_sound("death")
                    self.player.reset_position()
                    for g in self.ghosts:
                        g.reset_position()

    def render(self, surface):
        if self.game_map:
            self.game_map.render(surface)
        if self.food_manager:
            self.food_manager.render(surface)
        for ghost in self.ghosts:
            ghost.draw(surface)
        if self.player:
            self.player.draw(surface)


class CoopWorld:
    def __init__(self, level_name, sprite_loader, control_specs):
        self.sprite_loader = sprite_loader

        level_path = os.path.join(LEVELS_DIR, f"{level_name}.txt")
        if not os.path.exists(level_path):
            level_path = os.path.join(LEVELS_DIR, "level1.txt")

        self.game_map = Map(level_path, sprite_loader)

        spawns = self.game_map.get_all_positions("P")
        tints = [COOP_P1_TINT, COOP_P2_TINT]
        self.players = []
        self.controls = []
        self.labels = []
        for i, (controls, label) in enumerate(control_specs):
            spawn = spawns[i] if i < len(spawns) else (spawns[-1] if spawns else None)
            tint = tints[i] if i < len(tints) else None
            player = Player(self.game_map, sprite_loader, spawn=spawn, tint=tint)
            self.players.append(player)
            self.controls.append(controls)
            self.labels.append(label)

        self.lives = [COOP_LIVES for _ in self.players]

        self.ghosts = Ghost.create_from_map(self.game_map, sprite_loader)
        self.food_manager = FoodManager(self.game_map, sprite_loader)

        self.score = 0
        self.frightened_timer = 0.0
        self.ghost_eat_score = 200
        self.eaten_ghosts = set()

        self.level_start_time = time.time()
        self.time_bonus = 0

        self.finished = False
        self.result = None

    @property
    def frightened_active(self):
        return self.frightened_timer > 0

    def _living_players(self):
        return [p for p in self.players if not p.dead]

    def _nearest_player(self, ghost):
        living = self._living_players()
        if not living:
            return None
        return min(
            living,
            key=lambda p: (ghost.grid_x - p.grid_x) ** 2 + (ghost.grid_y - p.grid_y) ** 2,
        )

    def update(self, dt, keys, audio):
        if self.finished:
            return

        for player, controls in zip(self.players, self.controls):
            if player.dead:
                continue
            player.handle_input(keys, controls)
            player.update(dt, self.game_map)

        flash = (
            self.frightened_active
            and self.frightened_timer <= FRIGHTENED_FLASH_TIME
            and int(self.frightened_timer * 6) % 2 == 0
        )

        for ghost in self.ghosts:
            target = self._nearest_player(ghost)
            ghost.update(
                dt,
                self.game_map,
                target,
                self.frightened_active,
                flash,
                self.ghosts,
            )

        total_points = 0
        super_dots = 0
        for player in self._living_players():
            points, supers = self.food_manager.check_collisions(player)
            total_points += points
            super_dots += supers

        if total_points > 0:
            audio.play_sound("dot")
            self.score += total_points

        if super_dots > 0:
            self.frightened_timer = FRIGHTENED_DURATION
            self.ghost_eat_score = 200
            self.eaten_ghosts.clear()
            for ghost in self.ghosts:
                ghost.allow_frightened_again()

        if self.food_manager.all_collected():
            elapsed = max(1.0, time.time() - self.level_start_time)
            self.time_bonus = min(MAX_TIME_BONUS, int(TIME_BONUS_BASE / elapsed))
            self.score += self.time_bonus
            self.finished = True
            self.result = "win"
            return

        if self.frightened_timer > 0:
            self.frightened_timer = max(0.0, self.frightened_timer - dt)

        for ghost in self.ghosts:
            for player in self._living_players():
                if not ghost.check_collision(player):
                    continue

                if self.frightened_active and not ghost.ignore_frightened:
                    ghost_id = id(ghost)
                    if ghost_id not in self.eaten_ghosts:
                        self.score += self.ghost_eat_score
                        self.eaten_ghosts.add(ghost_id)
                        self.ghost_eat_score = min(self.ghost_eat_score * 2, 1600)
                        ghost.send_to_spawn()
                    break

                if ghost.respawn_freeze_timer > 0:
                    continue

                idx = self.players.index(player)
                self.lives[idx] -= 1

                if self.lives[idx] <= 0:
                    audio.play_sound("death")
                    player.dead = True
                else:
                    audio.play_sound("death")
                    player.reset_position()
                    for g in self.ghosts:
                        g.reset_position()
                break

        if all(p.dead for p in self.players):
            self.finished = True
            self.result = "lose"

    def render(self, surface):
        if self.game_map:
            self.game_map.render(surface)
        if self.food_manager:
            self.food_manager.render(surface)
        for ghost in self.ghosts:
            ghost.draw(surface)
        for player in self.players:
            if not player.dead:
                player.draw(surface)
