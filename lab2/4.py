import turtle

turtle.shape('turtle')
turtle.tracer(0)
x, y = 0, 0
vx, vy = 5, 80
a = -9.81
for t in range(60000):
    if y <= 0:
        vy = abs(vy)*0.8
    x += vx * 0.01
    y += vy * 0.01 + a * 0.01 ** 2 / 2
    vy += a * 0.01
    turtle.goto(x, y)
turtle.update()

turtle.getscreen()._root.mainloop()