import pygame
import os
import math
import random
import models.move_direction
from appsettings import window_size
from appsettings import image_store_path
from path_finder import PathFinder

pacman_model_directory = os.path.join(image_store_path, "red_ghost")
frames_between_tile_pass = 16
tile_switch_frame = 15

class RedGhost(pygame.sprite.Sprite):
    def __init__(self, spawn_tile, tile_size, player_model, player_input):
        self.previous_frame_path_calc_player_tile = None
        self.player_model = player_model
        self.animation_tick_counter = 0
        self.current_sprite_index = 0
        self.tile_size = tile_size
        self.right_animation_sprites = self.get_right_sprites()
        self.left_animation_sprites = self.get_left_sprites()
        self.up_down_animation_sprites = self.get_up_down_sprites()
        self.current_tile = spawn_tile
        self.movement_speed = math.floor(tile_size / frames_between_tile_pass)
        self.current_move_animation_frame = 0
        self.selected_move_direction = models.move_direction.left
        self.current_move_direction = models.move_direction.left
        self.stop = False
        self.path_finder = PathFinder(player_input)
        self.skips = 0

        pygame.sprite.Sprite.__init__(self)

        self.image = self.right_animation_sprites[self.current_sprite_index]
        self.rect = self.image.get_rect()
        self.set_pos(spawn_tile.rect.x, spawn_tile.rect.y)

    def update(self):
        if(self.player_model.current_tile == self.current_tile):
            self.player_model.kill()

        self.recalculate_path()

        if self.path is None or len(self.path) == 0:
            return

        self.selected_move_direction = self.path[0].side

        self.animation_tick_counter += 1
        if self.animation_tick_counter % 3 == 0:
            self.set_next_animation_sprite()

        self.move()

    def move(self):
        if self.current_move_animation_frame == frames_between_tile_pass or self.stop:
            self.set_pos(self.current_tile.rect.x, self.current_tile.rect.y)
            self.try_turn_in_direction(self.selected_move_direction)
            self.current_move_animation_frame = 0

        if not self.stop:
            self.current_move_animation_frame += 1
            self.move_in_direction()

    def recalculate_path(self):
        if self.previous_frame_path_calc_player_tile is not None and self.previous_frame_path_calc_player_tile is self.player_model.current_tile and self.skips < 1:
            self.skips += 1
            return

        self.path = self.path_finder.find(self.current_tile, self.player_model.current_tile).copy()
        #[self.current_tile.neighbours[0]]
        self.previous_frame_path_calc_player_tile = self.player_model.current_tile

    def move_in_direction(self):
        self.move_sprite(self.current_move_direction)
        for neigbor_info in self.current_tile.neighbours:
            if neigbor_info.side is self.current_move_direction:
                self.try_switch_tile(neigbor_info.tile)

    def move_sprite(self, direction):
        if direction == models.move_direction.left:
            self.move_x(-self.movement_speed)
        elif direction == models.move_direction.right:
            self.move_x(self.movement_speed)
        elif direction == models.move_direction.up:
            self.move_y(-self.movement_speed)
        else:
            self.move_y(self.movement_speed)

    def try_turn_in_direction(self, direction):
        for neigbor_info in self.current_tile.neighbours:
            if neigbor_info.side == direction and neigbor_info.tile.is_empty:
                self.choose_direction(direction)
                return True
        return False

    def choose_direction(self, direction):
        self.current_move_direction = direction

    def try_switch_tile(self, neghbour_tile):
        if self.current_move_animation_frame == tile_switch_frame:
            self.current_tile = neghbour_tile
            self.path.pop(0)
            print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    
    def move_x(self, distance):
        self.rect.x += distance

    def move_y(self, distance):
        self.rect.y += distance

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_next_animation_sprite(self):
        self.current_sprite_index = 0 if self.current_sprite_index == 2 else (self.current_sprite_index + 1)
        self.image = self.right_animation_sprites[self.current_sprite_index]

    def get_left_sprites(self):
        return [pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "1.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "2.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "1.png")).convert_alpha(), (self.tile_size, self.tile_size))]

    def get_right_sprites(self):
        return [pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "1.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "2.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "1.png")).convert_alpha(), (self.tile_size, self.tile_size))]

    def get_up_down_sprites(self):
        return [pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "1.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "2.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "1.png")).convert_alpha(), (self.tile_size, self.tile_size))]