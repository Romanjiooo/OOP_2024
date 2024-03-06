import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


yellow = (255, 255, 0)
red = (255, 0, 0)
gray = (128,128,128)
black = (0,0,0)

# (200, 200) - координаты центра круга
# 100 - радиус круга
pygame.draw.circle(screen, yellow, (200, 200), 100)
pygame.draw.circle(screen, (128,128,128), (200, 200), 100,2)
# (x, y, width, height) - координаты верхнего левого угла, ширина и высота прямоугольника
pygame.draw.rect(screen, black, (150, 250, 100, 25))
pygame.draw.circle(screen, red , (250, 170), 20)
pygame.draw.circle(screen, black , (250, 170), 10)
pygame.draw.circle(screen, black , (250, 170), 20,2)

pygame.draw.circle(screen, red , (180, 170), 40)
pygame.draw.circle(screen, black , (180, 170), 10)
pygame.draw.circle(screen, black , (180, 170), 40,2)

line(screen, gray, (235, 140), (350, 90), width=20) #праваая
line(screen, gray, (30, 50), (200, 115), width=20)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
