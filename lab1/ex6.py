import turtle

turtle.shape('turtle')
turtle.tracer(0)
n=12
for i in range(1,360):
    turtle.right(360/n)
    turtle.forward(100)
    turtle.stamp()
    turtle.backward(100)
turtle.update()
