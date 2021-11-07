import pygame
import os
from appsettings import image_store_path

tile_model_directory = os.path.join(image_store_path, "tiles")

class Tile(pygame.sprite.Sprite):
    wall_tile_sprite = pygame.image.load(os.path.join(tile_model_directory, "wallTile.png"))
    empty_tile_sprite = pygame.image.load(os.path.join(tile_model_directory, "emptyTile.png"))
    coin_tile_sprite = pygame.image.load(os.path.join(tile_model_directory, "coinTile.png"))

    def __init__(self, is_empty, tile_size, score_counter):
        pygame.sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.is_empty = is_empty
        self.was_changed_empty = False
        self.was_walked = False
        self.update_sprite()
        self.rect = self.image.get_rect()
        self.score_counter = score_counter
        self.init_neighbours()

    def update(self):
        if not self.was_changed_empty and self.was_walked:
            self.score_counter.picked()
            self.update_sprite()
            self.was_changed_empty = True

    def init_neighbours(self):
        self.neighbours = []

    def update_sprite(self):
        if self.is_empty:
            if self.was_walked:
                self.set_tile_image(Tile.empty_tile_sprite.convert_alpha())
                return
            self.set_tile_image(Tile.coin_tile_sprite.convert_alpha())
            return
        self.set_tile_image(Tile.wall_tile_sprite.convert_alpha())

    def set_tile_image(self, image):
        self.image = pygame.transform.scale(image, (self.tile_size, self.tile_size))

class FieldNeighbor():
    def __init__(self, tile, side):
        self.tile = tile
        self.side = side
