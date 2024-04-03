import turtle

turtle.shape('turtle')
turtle.tracer(0)
for i in range(1,3600):
  turtle.forward(((i/90)+1)/10)
  turtle.left(1)
turtle.update()
turtle.update()

