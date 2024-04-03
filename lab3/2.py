import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((384, 257))


yellow = (252, 238, 33)
oboi_vverx = (254, 213, 162)
oboi_centr = (255, 220, 202)
oboi_center_niz = (254, 213, 148)
oboi_niz = (179, 134, 148)

orange = (179, 72, 55)
red = (177, 68, 53)
neworange = (255, 156, 50)

pointsss = [(0,120),(0,104),(22,100),(50,80),(65,65),(80,50),(95,65),(100,65),(145,95),(175,94),(180,100),(205,80),(222,86),(230,76),(245,75),(255,65),(265,54),(275,43),(280,40),(285,45),(305,65),(320,60),(345,74),(357,65),(385,80)]


mountain_points = [(0, 170), (0,125), (10,133),(65,161),(82,136),(110,150),(125,115),(156,122),(185,144),(220,136),(312,135),(330,115),(346,126),(354,113),(368,115),(384,90),(384,195)]
mountain_points1 = [(220,136),(224,130),(234,120),(246,110),(250,108),(252,106),(254,104),(260,105),(264,104),(268,106),(270,106),(274,108),(280,114),(290,124),(295,127), (300,130),(310,135),(315,135)]
mointain_points2 = [(220,136),(224,130),(234,120)]
pygame.draw.rect(screen, oboi_vverx, (0, 0, 388, 55))
pygame.draw.rect(screen, oboi_centr, (0,55, 388, 45))
pygame.draw.rect(screen, oboi_center_niz, (0, 100, 388, 65))
pygame.draw.polygon(screen, neworange, pointsss)

pygame.draw.polygon(screen, orange, mountain_points)
ellipse(screen, red,(10,100,65,132))
pygame.draw.polygon(screen, orange, mountain_points1)
pygame.draw.rect(screen, oboi_niz, (0, 165, 388, 95))

pygame.draw.circle(screen, yellow, (180, 55), 20)

'''
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
'''

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
