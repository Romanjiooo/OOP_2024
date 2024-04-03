def zvizdos(n):
    for i in range(n):
        turtle.forward(100)
        turtle.right(180 - 180/n)


import turtle
turtle.penup()
turtle.backward(100)
turtle.pendown()
zvizdos(5)
turtle.penup()
turtle.forward(250)
turtle.pendown()
zvizdos(11)
