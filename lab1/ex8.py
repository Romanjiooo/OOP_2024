import turtle

turtle.shape('turtle')
turtle.tracer(0)
for i in range(1,36):
  turtle.forward((i*20)+20)
  turtle.left(90)
turtle.update()
turtle.update()

