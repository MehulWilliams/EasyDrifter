import arcade
import math

tire_size = 4
length = 30
dist = 3

class TrailRenderer():
   
   def __init__(self):
      #self.trail = [ {'l': (2, 3), 'r': (3, 4), 'angle': 90, 'alpha': 255}, {'x': (2, 3), 'y': (3, 4), 'angle': 90, 'alpha': 255}, ... ]
      self.trail = []

      self.counter = 0

      self.tire = arcade.load_texture("images/tire.png")

   def render_trail(self, other, main):
      for i in self.trail:
         arcade.draw_scaled_texture_rectangle(i['l'][0], i['l'][1], self.tire, .5, i['angle'], i['alpha'])
         arcade.draw_scaled_texture_rectangle(i['r'][0], i['r'][1], self.tire, .5, i['angle'], i['alpha'])

   def update_trail(self, other):
      if(self.counter == dist):
         a = other.get_adjusted_hit_box()
         self.trail.insert(0, {'l': a[0], 'r': a[1], 'angle': other.angle, 'alpha':  255})
         self.counter = 0
      self.counter += 1
      for i in self.trail:
         i['alpha'] -= 15 if i['alpha'] > 0 else 0
      if len(self.trail) > length-1:
         del self.trail[length-1]
