import pygame
import os
import math
import models.move_direction
from appsettings import window_size
from appsettings import image_store_path

pacman_model_directory = os.path.join(image_store_path, "pacman")
frames_between_tile_pass = 16
tile_switch_frame = 15

class Pacman(pygame.sprite.Sprite):
    def __init__(self, spawn_tile, tile_size, user_input_handler):
        self.killed = False
        spawn_tile.was_walked = True
        self.user_input = user_input_handler
        self.animation_tick_counter = 0
        self.current_sprite_index = 0
        self.tile_size = tile_size
        self.right_animation_sprites = self.get_right_sprites()
        self.left_animation_sprites = self.get_left_sprites()
        self.up_down_animation_sprites = self.get_up_down_sprites()
        self.current_tile = spawn_tile
        self.movement_speed = math.floor(tile_size / frames_between_tile_pass)
        self.current_move_animation_frame = 0
        self.selected_move_direction = user_input_handler.selected_direction
        self.current_move_direction = user_input_handler.selected_direction
        self.stop = False

        pygame.sprite.Sprite.__init__(self)

        self.image = self.right_animation_sprites[self.current_sprite_index]
        self.rect = self.image.get_rect()
        self.set_pos(spawn_tile.rect.x, spawn_tile.rect.y)

    def update(self):
        if not self.killed:
            self.selected_move_direction = self.user_input.selected_direction

            self.animation_tick_counter += 1
            if self.animation_tick_counter % 3 == 0:
                self.set_next_animation_sprite()

            self.move()

    def kill(self):
        self.killed = True
        self.image = self.get_killed_sprite()

    def move(self):
        if self.current_move_animation_frame == frames_between_tile_pass or self.stop:
            self.set_pos(self.current_tile.rect.x, self.current_tile.rect.y)
            if self.try_turn_in_direction(self.selected_move_direction) or self.try_turn_in_direction(self.current_move_direction):
                self.stop = False
            else:
                self.stop = True
            self.current_move_animation_frame = 0

        if not self.stop:
            self.current_move_animation_frame += 1
            self.move_in_direction()

    def move_in_direction(self):
        if self.current_move_direction == models.move_direction.left:
            self.move_x(-self.movement_speed)
            self.try_switch_tile(self.current_tile.left_neighbor)
        elif self.current_move_direction == models.move_direction.right:
            self.move_x(self.movement_speed)
            self.try_switch_tile(self.current_tile.right_neighbor)
        elif self.current_move_direction == models.move_direction.up:
            self.move_y(-self.movement_speed)
            self.try_switch_tile(self.current_tile.upper_neighbor)
        else:
            self.move_y(self.movement_speed)
            self.try_switch_tile(self.current_tile.bottom_neighbor)

    def try_turn_in_direction(self, direction):
        if direction == models.move_direction.left and self.current_tile.left_neighbor.is_empty:
            self.choose_direction(direction)
            return True
        elif direction == models.move_direction.right and self.current_tile.right_neighbor.is_empty:
            self.choose_direction(direction)
            return True
        elif direction == models.move_direction.up and self.current_tile.upper_neighbor.is_empty:
            self.choose_direction(direction)
            return True
        elif direction == models.move_direction.down and self.current_tile.bottom_neighbor.is_empty:
            self.choose_direction(direction)
            return True
        return False

    def choose_direction(self, direction):
        self.current_move_direction = direction

    def try_switch_tile(self, neghbour_tile):
        if self.current_move_animation_frame == tile_switch_frame:
            neghbour_tile.was_walked = True
            self.current_tile = neghbour_tile
    
    def move_x(self, distance):
        self.rect.x += distance

    def move_y(self, distance):
        self.rect.y += distance

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_next_animation_sprite(self):
        self.current_sprite_index = 0 if self.current_sprite_index == 2 else (self.current_sprite_index + 1)
        if self.current_move_direction == models.move_direction.right:
            self.image = self.right_animation_sprites[self.current_sprite_index]
        elif self.current_move_direction == models.move_direction.left:
            self.image = self.left_animation_sprites[self.current_sprite_index]
        else:
            self.image = self.up_down_animation_sprites[self.current_sprite_index]

    def get_left_sprites(self):
        return [pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanL.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanOpenL.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanUD.png")).convert_alpha(), (self.tile_size, self.tile_size))]

    def get_right_sprites(self):
        return [pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanR.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanOpenR.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanUD.png")).convert_alpha(), (self.tile_size, self.tile_size))]

    def get_up_down_sprites(self):
        return [pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanUpUD.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanUD.png")).convert_alpha(), (self.tile_size, self.tile_size)),
        pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "pacmanUpUD.png")).convert_alpha(), (self.tile_size, self.tile_size))]

    def get_killed_sprite(self):
        return pygame.transform.scale(pygame.image.load(os.path.join(pacman_model_directory, "banana.png")).convert_alpha(), (self.tile_size, self.tile_size))