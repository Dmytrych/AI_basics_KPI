import json
import pygame
import appsettings
import os
import math
from models.tiles.field_tile_model import Tile

field_model_directory = os.path.join(appsettings.application_root_path, "models\\game_field_model")

class Field(pygame.sprite.Sprite):
    def __init__(self, all_sprites, field_size):
        self.grid = []
        self.max_available_points = 0
        self.field_pixel_size = field_size
        self.load_grid(all_sprites)
        pygame.sprite.Sprite.__init__(self)

    def calculate_sizes(self, field_dim):
        biggest_field_dim = self.field_height if self.field_height >= self.field_width else self.field_width
        self.tile_size = math.floor(field_dim / biggest_field_dim)

    def load_grid(self, all_sprites):
        with open(os.path.join(field_model_directory, "field.json"), "r") as file:
            content = json.load(file)
            self.parse_file(content)
            self.calculate_sizes(self.field_pixel_size)
            self.grid = [[0] * self.field_width for i in range(self.field_height)]
            for y in range(self.field_height):
                for x in range(self.field_width):
                    self.grid[y][x] = self.create_tile(all_sprites, self.field_matrix[y][x] == 1, x, y)
                    all_sprites.add(self.grid[y][x])
                    if self.grid[y][x].is_empty:
                        self.max_available_points += 1
        self.set_grid_neighbours()

    def parse_file(self, parsed_json):
            self.field_matrix = parsed_json["field_structure"]
            self.field_width = parsed_json["field_width"]
            self.field_height = parsed_json["field_height"]
            self.player_spawn_x = parsed_json["player_spawn_x"]
            self.player_spawn_y = parsed_json["player_spawn_y"]

    def create_tile(self, all_sprites, is_empty, pos_x, pos_y):
        tile = Tile(is_empty, self.tile_size)
        tile.rect.x = pos_x * self.tile_size
        tile.rect.y = pos_y * self.tile_size
        all_sprites.add(tile)
        return tile
    
    def set_grid_neighbours(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.grid[y][x].left_neighbor = self.grid[y][x - 1]
                self.grid[y][x].upper_neighbor = self.grid[y - 1][x]
                self.grid[y][x - 1].right_neighbor = self.grid[y][x]
                self.grid[y - 1][x].bottom_neighbor = self.grid[y][x]
