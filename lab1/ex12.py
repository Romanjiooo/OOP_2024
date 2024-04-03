import turtle
def big():
    for i in range(1,182):
        turtle.forward(3)
        turtle.right(1)
def mal():
    for i in range(1,181):
        turtle.forward(1)
        turtle.right(1)

turtle.shape('turtle')
turtle.tracer(0)
turtle.right(270)
for j in range(12):
    big()
    mal()
turtle.update()
turtle.update()
turtle.tracer(0)

