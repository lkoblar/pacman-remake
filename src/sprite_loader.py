import os
import pygame
from src.settings import ASSETS_DIR, SCALE, SPRITE_SIZE, TILE_SIZE, SCALED_TILE


class SpriteLoader:
    def __init__(self):
        self.pacman_sprites = {}
        self.ghost_sprites = {}
        self.tile_sprites = {}

    def load_image(self, path, size=None):
        image = pygame.image.load(path).convert_alpha()
        if size is None:
            w, h = image.get_size()
            size = (w * SCALE, h * SCALE)
        image = pygame.transform.scale(image, size)
        return image

    def load_pacman_sprites(self):
        directions = ["up", "down", "left", "right"]
        for direction in directions:
            frames = []
            for i in range(1, 4):
                path = os.path.join(ASSETS_DIR, "pacman", direction, f"{i}.png")
                frames.append(self.load_image(path))
            self.pacman_sprites[direction] = frames
        return self.pacman_sprites

    def load_ghost_sprites(self):
        ghost_names = ["blinky", "pinky", "inky", "clyde", "blue_ghost"]
        for name in ghost_names:
            path = os.path.join(ASSETS_DIR, "ghosts", f"{name}.png")
            self.ghost_sprites[name] = self.load_image(path)
        return self.ghost_sprites

    def load_tile_sprites(self):
        tile_files = {
            "wall": "wall.png",
            "dot": "dot.png",
            "super_dot": "super_dot.png",
            "apple": "apple.png",
            "strawberry": "strawberry.png",
        }
        tile_size_override = {"dot": SCALED_TILE, "super_dot": SCALED_TILE}
        for key, filename in tile_files.items():
            path = os.path.join(ASSETS_DIR, "other", filename)
            sz = tile_size_override.get(key)
            self.tile_sprites[key] = self.load_image(path, (sz, sz) if sz else None)
        return self.tile_sprites

    def load_all(self):
        self.load_pacman_sprites()
        self.load_ghost_sprites()
        self.load_tile_sprites()
        return self
