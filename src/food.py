import pygame
from src.settings import SCALED_TILE, DOT, SUPER_DOT, WHITE, YELLOW


class Dot(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, sprite=None):
        super().__init__()
        self.points = 10
        
        if sprite:
            self.image = sprite
        else:
            # ce ne najde asseta
            self.image = pygame.Surface((SCALED_TILE, SCALED_TILE), pygame.SRCALPHA)
            pygame.draw.circle(self.image, WHITE, (SCALED_TILE // 2, SCALED_TILE // 2), SCALED_TILE // 6)
        
        self.rect = self.image.get_rect()
        # damo tocke na screen
        self.rect.x = grid_x * SCALED_TILE
        self.rect.y = grid_y * SCALED_TILE


class SuperDot(Dot):
    def __init__(self, grid_x, grid_y, sprite=None):
        super().__init__(grid_x, grid_y, sprite)
        self.points = 50
        
        if not sprite:
            # ce ne najde asseta
            self.image = pygame.Surface((SCALED_TILE, SCALED_TILE), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (SCALED_TILE // 2, SCALED_TILE // 2), SCALED_TILE // 3)


class FoodManager:
    def __init__(self, game_map, sprite_loader):
        self.food_group = pygame.sprite.Group()
        self._generate_from_map(game_map, sprite_loader)

    def _generate_from_map(self, game_map, sprite_loader):
        dot_sprite = sprite_loader.tile_sprites.get("dot")
        super_dot_sprite = sprite_loader.tile_sprites.get("super_dot")

        for row_idx, row in enumerate(game_map.grid):
            for col_idx, tile in enumerate(row):
                if tile == DOT:
                    self.food_group.add(Dot(col_idx, row_idx, dot_sprite))
                elif tile == SUPER_DOT:
                    self.food_group.add(SuperDot(col_idx, row_idx, super_dot_sprite))

    def check_collisions(self, player):
        player.rect = player.get_rect()
        # spritecollide zbrise piko ce se je player dotakne (iz skupine)
        eaten_dots = pygame.sprite.spritecollide(player, self.food_group, True)

        # sestevamo tocke
        points = sum(dot.points for dot in eaten_dots)
        return points

    def all_collected(self):
        # preverja ce smo vse pojedli
        return len(self.food_group) == 0

    def render(self, surface):
        # narisemo vse ki so se v skupini
        self.food_group.draw(surface)
