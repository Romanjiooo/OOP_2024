import pygame
from pygame.draw import *

# Константы
FPS = 30
WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400
HARE_COLOR = (200, 200, 200)
HARE_POSITION_X, HARE_POSITION_Y = 200, 200
HARE_WIDTH, HARE_HEIGHT = 200, 400

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def draw_hare(surface, x, y, width, height, color):
    # Функция для рисования зайца
    draw_body_parts(surface, x, y, width, height, color)

def draw_body_parts(surface, x, y, width, height, color):
    # Отдельные функции для рисования частей тела зайца
    body_width, body_height = width // 2, height // 2
    head_size = height // 4
    ear_height = height // 3
    leg_height = height // 16
    # Рисование тела
    draw_ellipse(surface, x, y + body_height // 2, body_width, body_height, color)
    # Рисование головы
    draw_circle(surface, x, y - head_size // 2, head_size // 2, color)
    # Рисование ушей
    ear_y = y - height // 2 + ear_height // 2

    for ear_x in (x - head_size // 4, x + head_size // 4):
        draw_ellipse(surface, ear_x, ear_y, width // 8, ear_height, color)

    # Рисование ног
    leg_y = y + height // 2 - leg_height // 2
    for leg_x in (x - width // 4, x + width // 4):
        draw_ellipse(surface, leg_x, leg_y, width // 4, leg_height, color)


def draw_ellipse(surface, x, y, width, height, color):
    # Универсальная функция для рисования эллипса
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_circle(surface, x, y, radius, color):
    # Универсальная функция для рисования круга
    circle(surface, color, (x, y), radius)

draw_hare(screen, HARE_POSITION_X, HARE_POSITION_Y, HARE_WIDTH, HARE_HEIGHT, HARE_COLOR)
pygame.display.update()

clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()