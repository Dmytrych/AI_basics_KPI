import pygame
import os
from appsettings import image_store_path

tile_model_directory = os.path.join(image_store_path, "tiles")

class Tile(pygame.sprite.Sprite):
    wall_tile_sprite = pygame.image.load(os.path.join(tile_model_directory, "wallTile.png"))
    empty_tile_sprite = pygame.image.load(os.path.join(tile_model_directory, "emptyTile.png"))
    coin_tile_sprite = pygame.image.load(os.path.join(tile_model_directory, "coinTile.png"))

    def __init__(self, is_empty, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.is_empty = is_empty
        self.was_changed_empty = False
        self.was_walked = False
        if is_empty:
            self.image = pygame.transform.scale(Tile.coin_tile_sprite.convert_alpha(), (self.tile_size, self.tile_size))
        else:
            self.image = pygame.transform.scale(Tile.wall_tile_sprite.convert_alpha(), (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.init_neighbours()

    def update(self):
        if self.was_walked and not self.was_changed_empty:
            self.image = pygame.transform.scale(Tile.empty_tile_sprite.convert_alpha(), (self.tile_size, self.tile_size))
            self.was_changed_empty = True

    def init_neighbours(self):
        self.left_neighbor = None
        self.right_neighbor = None
        self.upper_neighbor = None
        self.bottom_neighbor = None
