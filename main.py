from user_input import UserInput
import pygame
import models.move_direction
from appsettings import window_size
from models.game_field_model.field_model import Field
from models.pacman_model import Pacman
from models.red_ghost_model import RedGhost

FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
field = Field(all_sprites, window_size)
pacman = Pacman(field.grid[field.player_spawn_y][field.player_spawn_x], field.tile_size, input)
reg_ghost = RedGhost(field.grid[field.player_spawn_y][field.player_spawn_x + 3], field.tile_size, pacman)
all_sprites.add(pacman)
all_sprites.add(reg_ghost)

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

    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()