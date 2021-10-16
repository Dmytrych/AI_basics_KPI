from user_input import UserInput
import pygame
import path_finder
import models.move_direction
from appsettings import window_size
from models.game_field_model.field_model import Field
from models.pacman_model import Pacman
from models.red_ghost_model import RedGhost
import random

FPS = 30
MAP_TILE_SIZE = 19
PLAYER_SPAWN_X = 10
PLAYER_SPAWN_Y = 10

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def generate_map(size, player_spawn_y, player_spawn_x):
    field = [[0] * size for i in range(size)]
    for y in range(len(field)):
        for x in range(len(field[y])):
            if (random.randint(0, 100) > 30):
                field[y][x] = 1
            else:
                field[y][x] = 0
    for i in range(4):
        field[player_spawn_y][player_spawn_x + i] = 1
    return field

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Цикл игры
running = True
input = UserInput()
field_matrix = generate_map(MAP_TILE_SIZE, PLAYER_SPAWN_Y, PLAYER_SPAWN_X)
field = Field(all_sprites, window_size, field_matrix, PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
pacman = Pacman(field.grid[field.player_spawn_y][field.player_spawn_x], field.tile_size, input)
reg_ghost = RedGhost(field.grid[field.player_spawn_y][field.player_spawn_x + 3], field.tile_size, pacman, input)
all_sprites.add(pacman)
all_sprites.add(reg_ghost)
algo_index = 0

while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                input.selected_direction = models.move_direction.right
            elif event.key == pygame.K_LEFT:
                input.selected_direction = models.move_direction.left
            elif event.key == pygame.K_UP:
                input.selected_direction = models.move_direction.up
            elif event.key == pygame.K_DOWN:
                input.selected_direction = models.move_direction.down
            elif event.key == pygame.K_SPACE:
                input.selected_algorythm = path_finder.algorythms[algo_index]
                print("Current algo changed")
                algo_index += 1

    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
