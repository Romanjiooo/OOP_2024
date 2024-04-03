import turtle

def krug(n):
    turtle.circle(n)
n=100
s=6
turtle.shape('turtle')
turtle.tracer(0)
turtle.right(90)
for i in range(1,s+1):
    for n in range(1,10):
        krug(10*n+50)
        turtle.right(360/2)

turtle.update()
turtle.tracer(0)

