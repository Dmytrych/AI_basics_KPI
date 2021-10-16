import models.move_direction
import os
import pygame
from appsettings import image_store_path

tile_model_directory = os.path.join(image_store_path, "tiles")
algorythms = [ 0, 1]

class PathFinder():
    painted_tile = pygame.image.load(os.path.join(tile_model_directory, "painted_tile.png"))

    def __init__(self, user_input):
        self.path = None
        self.user_input = user_input

    def find(self, start_tile, end_tile):
        print("path finder started")
        self.initialize_search(start_tile, end_tile)

        print(self.user_input.selected_algorythm)
        if(self.user_input.selected_algorythm == 0):
            self.visit_dfs(start_tile)

        if(self.user_input.selected_algorythm == 1):
            self.start_bfs(start_tile)
            print(self.path_directions)

        if self.path is None or len(self.path) == 0:
            return []

        self.paint_tiles()

        return self.path_directions

    def visit_dfs(self, tile):
        if(tile is self.end_tile):
            self.path_found = True
            return
        for neigbour_info in tile.neighbours:
            self.try_visit_tile_dfs(neigbour_info)

    def try_visit_tile_dfs(self, tile_info):
        if not self.path_found and tile_info.tile.is_empty and tile_info.tile not in self.walked_tiles:
            self.path.append(tile_info)
            self.path_directions.append(tile_info.side)
            self.walked_tiles.append(tile_info.tile)
            self.visit_dfs(tile_info.tile)
            if self.path_found:
                return
            self.path.pop()
            self.path_directions.pop()

    def start_bfs(self, start_tile):
        self.ancestors_table = {}
        self.visit_queue = []

        self.walked_tiles.append(start_tile)
        for neighbour_info in start_tile.neighbours:
            self.visit_queue.append(neighbour_info)
            self.ancestors_table[neighbour_info] = start_tile

        while len(self.visit_queue) != 0:
            current_tile_info = self.visit_queue.pop(0)
            reached_end = self.visit_bfs(current_tile_info)
            if reached_end:
                self.calculate_final_result_bfs(current_tile_info, start_tile)
                break

    def visit_bfs(self, tile_info):
        if(tile_info.tile is self.end_tile):
            return True

        for neighbour_info in tile_info.tile.neighbours:
            if neighbour_info.tile.is_empty and neighbour_info.tile not in self.walked_tiles:
                self.visit_queue.append(neighbour_info)
                self.walked_tiles.append(neighbour_info.tile)
                self.ancestors_table[neighbour_info] = tile_info
        return False

    def calculate_final_result_bfs(self, current_tile, start_tile):
        self.path.append(current_tile)
        previous_tile = self.ancestors_table[current_tile]
        if previous_tile is not None and previous_tile is not start_tile and previous_tile.tile is not start_tile:
            self.calculate_final_result_bfs(previous_tile, start_tile)

    def initialize_search(self, start_tile, end_tile):
        self.end_tile = end_tile
        self.walked_tiles = [start_tile]
        self.path_directions = []
        self.path_found = False
        self.clear_paint()
        self.path = []

    def paint_tiles(self):
        for tile_info in self.path:
            tile_info.tile.set_tile_image(PathFinder.painted_tile.convert_alpha())

    def clear_paint(self):
        if self.path is None or len(self.path) == 0:
            return
        
        for tile_info in self.path:
            tile_info.tile.update_sprite()

