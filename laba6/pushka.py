import math
import time
from tkinter import *
from random import *
root=Tk()
fr=Frame(root)
root.geometry('800x600')
canv=Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)

class ball():
 def init(self,x=40,y=450):
  self.x=x
  self.y=y
  self.r=10
  self.vx=0
  self.vy=0
  self.color='red'
  self.id=canv.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.color)
  self.live=30
 def set_coords(self):
  canv.coords(self.id,self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r)
 def move(self):
  if self.y<=500:
   self.vy-=1.2
   self.y-=self.vy
   self.x+=self.vx
   self.vx*=0.99
   self.set_coords()
  else:
   if self.vx**2+self.vy**2>10:
    self.vy=-self.vy/2
    self.vx=self.vx/2
    self.y=499
   if self.live<0:
    balls.pop(balls.index(self))
    canv.delete(self.id)
   else:
    self.live-=1
  if self.x>780:
   self.vx=-self.vx/2
   self.x=779
 def hittest(self,ob):
  if abs(ob.x-self.x)<=(self.r+ob.r)and abs(ob.y-self.y)<=(self.r+ob.r):
   return True
  else:
   return False
"""
Класс gun описывает пушку. 
"""
class gun():
 def init(self):
  self.f2_power=10
  self.f2_on=0
  self.an=1
  self.id=canv.create_line(20,450,50,420,width=7)
 def fire2_start(self,event):
  self.f2_on=1
 def fire2_end(self,event):
  global balls,bullet
  bullet+=1
  new_ball=ball()
  new_ball.r+=5
  self.an=math.atan((event.y-new_ball.y)/(event.x-new_ball.x))
  new_ball.vx=self.f2_power*math.cos(self.an)
  new_ball.vy=-self.f2_power*math.sin(self.an)
  balls+=[new_ball]
  self.f2_on=0
  self.f2_power=10
 def targetting(self,event=0):
  if event:
   self.an=math.atan((event.y-450)/(event.x-20))
  if self.f2_on:
   canv.itemconfig(self.id,fill='orange')
  else:
   canv.itemconfig(self.id,fill='black')
  canv.coords(self.id,20,450,20+max(self.f2_power,20)*math.cos(self.an),450+max(self.f2_power,20)*math.sin(self.an))
 def power_up(self):
  if self.f2_on:
   if self.f2_power<100:
    self.f2_power+=1
   canv.itemconfig(self.id,fill='orange')
  else:
   canv.itemconfig(self.id,fill='black')
"""
Класс target описывает цель. 
"""
class target():
  def init(self):
    self.points=0
    self.id=canv.create_oval(0,0,0,0)
    self.id_points=canv.create_text(30,30,text=self.points,font='28')
    self.new_target()
    self.live=1
  def new_target(self):
    x=self.x=randint(50, 780)
    y=self.y=randint(50, 500)
    r=self.r=round(2,50)
    color=self.color='red'
    canv.coords(self.id,x-r,y-r,x+r,y+r)
    canv.itemconfig(self.id,fill=color)
  def hit(self,points=1):
    canv.coords(self.id,-10,-10,-10,-10)
    self.points+=points
    canv.itemconfig(self.id_points,text=self.points)
  def rand_mv(self):
    a = [[5,0], [-5,0], [0,5], [0,-5]]
    dir = a[randint(0, 3)]
    self.x += dir[0]
    self.y += dir[1]
    x, y, r = self.x, self.y, self.r
    canv.coords(self.id,x-r,y-r,x+r,y+r)

t1=target()
t2=target()
screen1=canv.create_text(400,300,text='',font='28')
g1=gun()
bullet=0
balls=[]

def new_game(event=''):
  global gun,t1,t2,screen1,balls,bullet
  t1.new_target()
  t2.new_target()
  bullet=0
  balls=[]
  canv.bind('<Button-1>',g1.fire2_start)
  canv.bind('<ButtonRelease-1>',g1.fire2_end)
  canv.bind('<Motion>',g1.targetting)
  t1.live=1
  t2.live=1
  while t1.live or t2.live or balls:
    if (t1.live):
      t1.rand_mv()
    if (t2.live):
      t2.rand_mv()
    canv.update()

    for b in balls:
      b.move()
      if b.hittest(t1) and t1.live:
        t1.live=0
        t1.hit()
        # canv.bind('<Button-1>','')
        # canv.bind('<ButtonRelease-1>','')
        canv.itemconfig(screen1,text='Вы уничтожили одну из целей за '+str(bullet)+' выстрелов')
      if b.hittest(t2) and t2.live:
        t2.live=0
        t2.hit()
        # canv.bind('<Button-1>','')
        # canv.bind('<ButtonRelease-1>','')
        canv.itemconfig(screen1,text='Вы уничтожили одну из целей за '+str(bullet)+' выстрелов')
        # print(t1.live, t2.live)
        if not t1.live and not t2.live:
            canv.bind('<Button-1>', '')
            canv.bind('<ButtonRelease-1>', '')
            canv.itemconfig(screen1, text='Вы уничтожили все цели за ' + str(bullet) + ' выстрелов')

        # canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()

      canv.itemconfig(screen1, text='')
      canv.delete(gun)
      root.after(750, new_game)

    new_game()