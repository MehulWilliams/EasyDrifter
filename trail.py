import arcade
import math
#import car

tire_size = 3
length = 30

class TrailRenderer():
   
   def __init__(self):
      self.t = [(i * (255/length)) for i in range(length)]
      self.t.reverse()
      self.l = []
      self.r = []

      self.tire = arcade.load_texture("images/tire.png")
      #self.car = Car

   def render_trail(self, other, main):
      #print((main.forward_x - main.move_force_x) * .166 * 1.5)
      #print((main.forward_y - main.move_force_y) * .166 * 1.5)

      print(math.radians(main.angle))
      print(math.atan2(main.forward_x - main.move_force_x,main.forward_y - main.move_force_y))

      #if other.speed > 300:
      self.update_trail(other)

      for i in range(len(self.l)):
         arcade.draw_scaled_texture_rectangle(self.l[i][0], self.l[i][1], self.tire, angle=self.l[i][2], alpha=self.t[i])
         arcade.draw_scaled_texture_rectangle(self.r[i][0], self.r[i][1], self.tire, angle=self.l[i][2], alpha=self.t[i])

   def update_trail(self, other):
      a = other.get_adjusted_hit_box()
      x = a[0]
      y = a[1]
      x.append(other.angle)
      y.append(other.angle)
      self.l.insert(0,x)
      self.r.insert(0,y)

      if len(self.l)  > length-1:
         del self.l[length-1]
      if len(self.r)  > length-1:
         del self.r[length-1]

      #print(self.l)

