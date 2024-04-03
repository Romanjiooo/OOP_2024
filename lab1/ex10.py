import turtle

def krug(n):
    turtle.circle(n)
n=100
s=6
turtle.shape('turtle')
turtle.tracer(0)
for i in range(1,s+1):
    krug(n)
    turtle.right(360/s)

turtle.update()
turtle.tracer(0)

