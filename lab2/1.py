import turtle
from random import *

turtle.shape('turtle')

turtle.tracer(0)

for i in range(1,1000):
    s = randint(1,360)
    turtle.right(s)
    a = randint(1,100)
    turtle.forward(a)

turtle.update()

turtle.getscreen()._root.mainloop()