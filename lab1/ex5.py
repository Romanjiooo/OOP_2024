import turtle

turtle.shape('turtle')
turtle.tracer(0)
for i in range(1,11):
   for j in range(4):
      turtle.forward(50*i)
      turtle.right(90)
   turtle.penup()
   turtle.right(180)
   turtle.forward(25)
   turtle.right(90)
   turtle.forward(25)
   turtle.right(90)
   turtle.pendown()
