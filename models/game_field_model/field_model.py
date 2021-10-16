import pygame
import appsettings
import os
import math
from models.tiles.field_tile_model import Tile
from models.tiles.field_tile_model import FieldNeighbor
import models.move_direction

field_model_directory = os.path.join(appsettings.application_root_path, "models\\game_field_model")

class Field(pygame.sprite.Sprite):
    def __init__(self, all_sprites, field_size, field_matrix, player_spawn_x, player_spawn_y):
        self.grid = []
        self.max_available_points = 0
        self.field_matrix = field_matrix
        self.field_width = len(field_matrix[0])
        self.field_height = len(field_matrix)
        self.player_spawn_x = player_spawn_x
        self.player_spawn_y = player_spawn_y
        self.tile_size = math.floor(field_size / self.field_height)
        self.load_grid(all_sprites)
        pygame.sprite.Sprite.__init__(self)

    def load_grid(self, all_sprites):
        self.grid = [[0] * self.field_width for i in range(self.field_height)]
        for y in range(self.field_height):
            for x in range(self.field_width):
                self.grid[y][x] = self.create_tile(all_sprites, self.field_matrix[y][x] == 1, x, y)
                all_sprites.add(self.grid[y][x])
                if self.grid[y][x].is_empty:
                    self.max_available_points += 1
        self.set_grid_neighbours()

    def create_tile(self, all_sprites, is_empty, pos_x, pos_y):
        tile = Tile(is_empty, self.tile_size)
        tile.rect.x = pos_x * self.tile_size
        tile.rect.y = pos_y * self.tile_size
        all_sprites.add(tile)
        return tile
    
    def set_grid_neighbours(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.grid[y][x].neighbours.append(FieldNeighbor(self.grid[y][x - 1], models.move_direction.left))
                self.grid[y][x].neighbours.append(FieldNeighbor(self.grid[y - 1][x], models.move_direction.up))
                self.grid[y][x - 1].neighbours.append(FieldNeighbor(self.grid[y][x], models.move_direction.right))
                self.grid[y - 1][x].neighbours.append(FieldNeighbor(self.grid[y][x], models.move_direction.down))
