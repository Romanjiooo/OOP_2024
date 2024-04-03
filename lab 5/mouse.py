import pygame
from pygame.draw import *
from random import randint,choice

# Инициализация Pygame
pygame.init()

FPS = 60
WIDTH, HEIGHT = 1200,900
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# Цвета
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (10,255,0)
GREEN = (0,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,100)
BLACK = (0,0,29)
COLORS = [RED,BLUE,YELLOW,GREEN,MAGENTA,CYAN]

# Параметры шариков
NUM_BALLS = 10
balls = []

# Счетчик очков
score = 0

def new_ball():
    '''Создает новый шарик со случайными параметрами.'''
    x = randint(100,1100)
    y = randint(100,900)
    r = randint(10,100)
    color = choice(COLORS)
    dx,dy = randint(-5,5),randint(-5,5)
    return [x,y,r,color,dx,dy]

def draw_ball(ball):
    '''Рисует шарик на экране.'''
    circle(screen,ball[3],(ball[0],ball[1]),ball[2])

def move_ball(ball):
    '''Обновляет положение шарика и отражает его от стен.'''
    ball[0] += ball[4]
    ball[1] += ball[5]

    # Отражение от левой и правой стен
    if ball[0] <= ball[2] or ball[0] >= WIDTH - ball[2]:
        ball[4] = -ball[4]

    # Отражение от верхней и нижней стен
    if ball[1] <= ball[2] or ball[1] >= HEIGHT - ball[2]:
        ball[5] = -ball[5]

def check_click(event,ball):
    '''Проверяет, попал ли клик в шарик.'''
    distance = ((event.pos[0] - ball[0])**2 + (event.pos[1] - ball[1])**2)**0.5
    return distance < ball[2]

def check_click2(event,ball):
    '''Проверяет, не попал ли клик в шарик.'''
    distance = ((event.pos[0] - ball[0])**2 + (event.pos[1] - ball[1])**2)**0.5
    return distance > ball[2]

# Создаем начальные шарики
for _ in range(NUM_BALLS):
    balls.append(new_ball())

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            k = 0
            for ball in balls:
                if check_click(event,ball):
                    k=1
                    balls.remove(ball)
                    balls.append(new_ball())
            if k == 0:
                if score >0:
                    score -= 1
            else:
                score += 1
            print(score)



    screen.fill(BLACK)
    x, y = pygame.mouse.get_pos()
    clicker = pygame.font.Font(None, 64)
    click = clicker.render(str(score), True, (255, 255, 255))
    screen.blit(click, (x, y))
    for ball in balls:
        draw_ball(ball)
        move_ball(ball)
    pygame.display.update()

pygame.quit()