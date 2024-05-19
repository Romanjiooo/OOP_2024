import math
import time
from tkinter import *
from random import choice, randint

root = Tk()
root.geometry('800x600')
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

class Ball:
    def __init__(self, x=40, y=450, r=10, vx=0, vy=0, color='red'):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = color
        self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color)
        self.live = 30

    def move(self):
        if self.y <= 500:
            self.vy -= 1.2
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
            canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        else:
            if self.vx**2 + self.vy**2 > 10:
                self.vy = -self.vy / 2
                self.vx = self.vx / 2
                self.y = 499
            if self.live < 0:
                balls.remove(self)
                canv.delete(self.id)
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx / 2
            self.x = 779

    def hittest(self, obj):
        return (abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r))

class BouncyBall(Ball):
    def __init__(self, x=40, y=450):
        super().__init__(x, y, color='blue')
        self.bounces = 15

    def move(self):
        super().move()
        if self.vx == 0 and self.vy == 0:
            self.bounces -= 1

class Gun:
    def __init__(self, x=20, y=450):
        self.x = x
        self.y = y
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(self.x, self.y, self.x + 30, self.y - 30, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.x, self.y)
        self.an = math.atan2((event.y - new_ball.y), (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=None):
        if event:
            self.an = math.atan2((event.y - self.y), (event.x - self.x))
        color = 'orange' if self.f2_on else 'black'
        canv.itemconfig(self.id, fill=color)
        canv.coords(self.id, self.x, self.y, self.x + max(self.f2_power, 20) * math.cos(self.an), self.y + max(self.f2_power, 20) * math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def move_left(self, event):
        if self.x > 0:
            self.x -= 10
            canv.move(self.id, -10, 0)

    def move_right(self, event):
        if self.x < 780:
            self.x += 10
            canv.move(self.id, 10, 0)

class Target:
    def __init__(self):
        self.points = 0
        self.id = canv.create_oval(0, 0, 0, 0)
        self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        self.new_target()
        self.live = 1

    def new_target(self):
        x = self.x = randint(50, 780)
        y = self.y = randint(50, 500)
        r = self.r = randint(20, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)

    def move(self):
        direction = choice([[5, 0], [-5, 0], [0, 5], [0, -5], [3, 3], [-3, -3]])
        self.x += direction[0]
        self.y += direction[1]
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

balls = []
guns = [Gun(), Gun(x=750, y=450)]
targets = [Target(), Target()]
screen1 = canv.create_text(400, 300, text='', font='28')
bullet = 0

def new_game(event=''):
    global balls, bullet
    for target in targets:
        target.new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', guns[0].fire2_start)
    canv.bind('<ButtonRelease-1>', guns[0].fire2_end)
    canv.bind('<Motion>', guns[0].targetting)
    root.bind('<Left>', guns[0].move_left)
    root.bind('<Right>', guns[0].move_right)
    while any(target.live for target in targets) or balls:
        for target in targets:
            if target.live:
                target.move()
        canv.update()
        for ball in balls:
            ball.move()
            for target in targets:
                if ball.hittest(target) and target.live:
                    target.live = 0
                    target.hit()
                    canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        time.sleep(0.03)
        for gun in guns:
            gun.targetting()
            gun.power_up()
    canv.itemconfig(screen1, text='')
    root.after(750, new_game)

new_game()
root.mainloop()
