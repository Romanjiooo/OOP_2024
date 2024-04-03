import turtle

turtle.shape('turtle')
#turtle.tracer(0)
for i in range(3,13):
    for g in range(i):
      turtle.forward(20*i)
      turtle.left(360/i)
    turtle.penup()
    turtle.left(90)
    turtle.forward(-5*i-5)
    turtle.right(90)
    turtle.pendown()
  
#turtle.update()

'''
    def mng(n):
    turtle.left(180/n)
    for i in range(n):
        turtle.forward(n*5)
        turtle.left(360/n)
    turtle.right(180/n)
        


import turtle
import math
turtle.left(90)
for i in range(3, 13):
    a = i * 5
    turtle.penup()
    turtle.goto((a/(2*math.sin(math.pi/i))), 0)
    turtle.pendown()
    mng(i)
'''
