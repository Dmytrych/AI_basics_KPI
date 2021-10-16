from math import sqrt
import models.move_direction
import os
import pygame
from appsettings import image_store_path

tile_model_directory = os.path.join(image_store_path, "tiles")
single_walk_cost = 1
default_tile_height = 76

class AStarPathFinder():
    painted_tile = pygame.image.load(os.path.join(tile_model_directory, "painted_tile.png"))

    def __init__(self):
        self.tile_path = None

    def find(self, start_tile, end_tile):
        # self.clear_paint()
        self.tile_path = []
        all_cells = []
        used_cells = []
        start_a_star_tile = AStarCell(start_tile)
        start_a_star_tile.init_start_tile(end_tile)
        self.update_neighbours(start_a_star_tile, all_cells, end_tile)
        print("A* path finder started")

        if(start_tile is end_tile):
            return []

        while(len(all_cells) != 0):
            best_cell = self.find_best_tile(all_cells)
            all_cells.remove(best_cell)
            used_cells.append(best_cell)
            self.update_neighbours(best_cell, all_cells, end_tile)
            end_cell = self.get_end_cell(all_cells)
            if end_cell is not None:
                path = self.get_path(end_cell)
                break

        if path is None or len(path) == 0:
            return []

        path.reverse()
        print(path)
        # self.paint_tiles()

        return path

    def get_path(self, cell):
        path = []
        current_cell = cell
        while (current_cell is not None and not current_cell.is_start_tile):
            path.append(current_cell.side)
            self.tile_path.append(current_cell.tile)
            current_cell = current_cell.prev_tile
        return path

    def get_end_cell(self, all_cells):
        for cell in all_cells:
            if cell.is_end_tile:
                return cell
        return None

    def update_neighbours(self, cell, all_cells, end_tile):
        for neigbour in cell.tile.neighbours:
            if neigbour.tile.is_empty:
                self.create_or_update_cell(neigbour.tile, cell, neigbour.side, end_tile, all_cells)

    def find_best_tile(self, all_cells):
        best_cell = all_cells[0]
        for cell in all_cells:
            if best_cell.total_cost > cell.total_cost and not cell.is_start_tile:
                best_cell = cell
        return best_cell

    def create_or_update_cell(self, tile, prev_tile, tile_side, end_tile, all_a_star_tiles):
        for a_star_tile in all_a_star_tiles:
            if a_star_tile.tile == tile:
                a_star_tile.update_costs(prev_tile, tile_side, end_tile)
                return
        new_tile = AStarCell(tile)
        new_tile.update_costs(prev_tile, tile_side, end_tile)
        all_a_star_tiles.append(new_tile)

    def paint_tiles(self):
        for tile_info in self.tile_path:
            tile_info.set_tile_image(AStarPathFinder.painted_tile.convert_alpha())

    def clear_paint(self):
        if self.tile_path is None or len(self.tile_path) == 0:
            return
        
        for tile_info in self.tile_path:
            tile_info.update_sprite()

class AStarCell():
    def __init__(self, tile):
        self.tile = tile
        self.g_cost = None
        self.prev_tile = None
        self.side = None
        self.total_cost = None
        self.is_start_tile = False
        self.is_end_tile = False

    def init_start_tile(self, end_tile):
        self.g_cost = 0
        self.update_h_cost(end_tile)
        self.update_total_cost()
        self.is_start_tile = True

    def update_costs(self, prev_tile, new_side, end_tile):
        if(self.tile is end_tile):
            self.is_end_tile = True

        new_g_cost = prev_tile.g_cost + single_walk_cost
        if(not self.is_start_tile and (self.g_cost == None or self.g_cost > new_g_cost)):
            self.g_cost = new_g_cost
            self.prev_tile = prev_tile
            self.side = new_side
            self.update_h_cost(end_tile)
            self.update_total_cost()

    def update_total_cost(self):
        self.total_cost = self.g_cost + self.h_cost

    def update_h_cost(self, end_tile):
        x_height = abs(self.tile.rect.x - end_tile.rect.x) / 38
        y_height = abs(self.tile.rect.y - end_tile.rect.y) / 38
        self.h_cost = sqrt(pow(x_height, 2) + pow(y_height, 2))

