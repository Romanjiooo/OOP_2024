import math
import time
from tkinter import *
from random import *

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = 'red'
        self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color)
        self.live = 30

    def set_coords(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def move(self):
        if self.y <= 500:
            self.vy -= 1.2
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
            self.set_coords()
        else:
            if self.vx**2 + self.vy**2 > 10:
                self.vy = -self.vy / 2
                self.vx = self.vx / 2
                self.y = 499
            if self.live < 0:
                if self in balls:
                    balls.pop(balls.index(self))
                canv.delete(self.id)
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx / 2
            self.x = 779

    def hittest(self, ob):
        if isinstance(ob, Gun):
            ob_r = 10
        else:
            ob_r = ob.r
        if abs(ob.x - self.x) <= (self.r + ob_r) and abs(ob.y - self.y) <= (self.r + ob_r):
            return True
        else:
            return False

class HeavyBall(Ball):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy)
        self.r = 15
        self.color = 'blue'
        canv.itemconfig(self.id, fill=self.color)

class FastBall(Ball):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy)
        self.r = 8
        self.color = 'green'
        canv.itemconfig(self.id, fill=self.color)

    def move(self):
        if self.y <= 500:
            self.vy -= 1.5
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
            self.set_coords()
        else:
            if self.vx**2 + self.vy**2 > 10:
                self.vy = -self.vy / 2
                self.vx = self.vx / 2
                self.y = 499
            if self.live < 0:
                if self in balls:
                    balls.pop(balls.index(self))
                canv.delete(self.id)
            else:
                self.live -= 1
        if self.x > 780:
            self.vx = -self.vx / 2
            self.x = 779

class Gun:
    def __init__(self, x, y):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x = x
        self.y = y
        self.r = 10
        self.id = canv.create_line(self.x, self.y, self.x + 30, self.y - 30, width=7)
        self.ball_type = Ball
        self.balls = []
        self.vx = randint(-2, 2)
        self.vy = randint(-2, 2)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        new_ball = self.ball_type(self.x, self.y, 0, 0)
        new_ball.r += 5
        try:
            self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        except ZeroDivisionError:
            self.an = math.pi / 2 if event.y > new_ball.y else -math.pi / 2
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        self.balls.append(new_ball)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        if event:
            try:
                self.an = math.atan((event.y - self.y) / (event.x - self.x))
            except ZeroDivisionError:
                self.an = math.pi / 2 if event.y > self.y else -math.pi / 2
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x, self.y, self.x + max(self.f2_power, 20) * math.cos(self.an), self.y + max(self.f2_power, 20) * math.sin(self.an))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > 800:
            self.vx = -self.vx
        if self.y < 0 or self.y > 600:
            self.vy = -self.vy
        canv.coords(self.id, self.x, self.y, self.x + max(self.f2_power, 20) * math.cos(self.an), self.y + max(self.f2_power, 20) * math.sin(self.an))

    def change_ball_type(self, ball_type):
        self.ball_type = ball_type

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
        r = self.r = 20
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)

    def move(self):
        pass

class StaticTarget(Target):
    def move(self):
        pass

class MovingTarget(Target):
    def move(self):
        a = [[5, 0], [-5, 0], [0, 5], [0, -5]]
        dir = a[randint(0, 3)]
        self.x += dir[0]
        self.y += dir[1]
        x, y, r = self.x, self.y, self.r
        canv.coords(self.id, x - r, y - r, x + r, y + r)

class Bomb(Target):
    def __init__(self):
        super().__init__()
        self.x = randint(50, 780)
        self.y = 0
        self.vy = 5
        self.r = 15
        self.color = 'black'
        canv.itemconfig(self.id, fill=self.color)

    def move(self):
        self.y += self.vy
        if self.y > 600:
            self.new_target()
        x, y, r = self.x, self.y, self.r
        canv.coords(self.id, x - r, y - r, x + r, y + r)

t1 = StaticTarget()
t2 = MovingTarget()
b1 = Bomb()
b2 = Bomb()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = Gun(100, 450)
g2 = Gun(700, 450)
g3 = Gun(400, 300)
guns = [g1, g2, g3]
bullet = 0
balls = []

def new_game(event=''):
    global gun, t1, t2, b1, b2, screen1, balls, bullet
    t1.new_target()
    t2.new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', lambda event: [g.fire2_start(event) for g in guns])
    canv.bind('<ButtonRelease-1>', lambda event: [g.fire2_end(event) for g in guns])
    canv.bind('<Motion>', lambda event: [g.targetting(event) for g in guns])
    root.bind('<KeyPress-1>', lambda event: [g.change_ball_type(Ball) for g in guns])
    root.bind('<KeyPress-2>', lambda event: [g.change_ball_type(HeavyBall) for g in guns])
    root.bind('<KeyPress-3>', lambda event: [g.change_ball_type(FastBall) for g in guns])
    t1.live = 1
    t2.live = 1
    b1.live = 1
    b2.live = 1

    while t1.live or t2.live or b1.live or b2.live or any(g.balls for g in guns):
        if t1.live:
            t1.move()
        if t2.live:
            t2.move()
        b1.move()
        b2.move()
        for g in guns:
            g.move()
        canv.update()

        for g in guns:
            for b in g.balls:
                b.move()
                if b.hittest(t1) and t1.live:
                    t1.live = 0
                    t1.hit()
                    canv.itemconfig(screen1, text='Вы уничтожили одну из целей за ' + str(bullet) + ' выстрелов')
                if b.hittest(t2) and t2.live:
                    t2.live = 0
                    t2.hit()
                    canv.itemconfig(screen1, text='Вы уничтожили одну из целей за ' + str(bullet) + ' выстрелов')
                for other_gun in guns:
                    if other_gun != g:
                        if b.hittest(other_gun):
                            canv.itemconfig(screen1, text='Одна пушка попала в другую!')
                if b.hittest(b1) and b1.live:
                    b1.live = 0
                    b1.hit()
                    canv.itemconfig(screen1, text='Вы сбили бомбу!')
                if b.hittest(b2) and b2.live:
                    b2.live = 0
                    b2.hit()
                    canv.itemconfig(screen1, text='Вы сбили бомбу!')

        if not t1.live:
            t1.new_target()
            t1.live = 1
        if not t2.live:
            t2.new_target()
            t2.live = 1
        if not b1.live:
            b1 = Bomb()
        if not b2.live:
            b2 = Bomb()

        time.sleep(0.03)
        for g in guns:
            g.targetting()
            g.power_up()

    canv.itemconfig(screen1, text='')
    for g in guns:
        canv.delete(g.id)
    root.after(750, new_game)

new_game()
root.mainloop()
