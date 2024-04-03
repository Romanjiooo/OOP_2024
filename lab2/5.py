from random import randint
import turtle

radius = 10

window = turtle.Screen()
window.title("Идеальный газ в контейнере с учетом радиуса частицы")
window.bgcolor("white")

min_x, min_y = -200 + radius, -200 + radius
max_x, max_y = 200 - radius, 200 - radius

# Функция для рисования контейнера
def draw_container():
    turtle.penup()
    turtle.goto(-200, 200)
    turtle.pendown()
    for _ in range(2):
        turtle.forward(400)
        turtle.right(90)
        turtle.forward(400)
        turtle.right(90)
    turtle.penup()

draw_container()

num_particles = 10
steps = 1000
coordinates = [[0, 0] for _ in range(num_particles)]
speeds = [[randint(-10, 10), randint(-10, 10)] for _ in range(num_particles)]
particles = [turtle.Turtle(shape='circle') for _ in range(num_particles)]

# Инициализация частиц
for i, particle in enumerate(particles):
    particle.penup()
    coordinates[i] = [randint(min_x, max_x), randint(min_y, max_y)]
    particle.goto(coordinates[i])

# Основной цикл моделирования
for _ in range(steps):
    for i in range(num_particles):
        if coordinates[i][0] + speeds[i][0] > max_x or coordinates[i][0] + speeds[i][0] < -200 + radius:
            speeds[i][0] = -speeds[i][0]
        if coordinates[i][1] + speeds[i][1] > max_y or coordinates[i][1] + speeds[i][1] < -200 + radius:
            speeds[i][1] = -speeds[i][1]

        coordinates[i][0] += speeds[i][0]
        coordinates[i][1] += speeds[i][1]
        particles[i].goto(coordinates[i])

turtle.done()
