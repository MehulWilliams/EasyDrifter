import arcade as arc
import math
import trail as tr


WIDTH = 700
HEIGHT = 500

top_speed = 700
friction = .98
grip = 1.5
#make grip a function of current speed, decreasing with increase of speed

max_turn = 2.25

y_sensitivity = .03
x_sensitivity = .015


class Car(arc.Sprite): 
    def __init__(self, texture, scaling):
        super().__init__(texture, scaling, hit_box_algorithm=None)

        self.center_x = WIDTH/2
        self.center_y = HEIGHT/2

        self.move_force_x = 0
        self.move_force_y = 0
        self.forward_x = 0
        self.forward_y = 0
        
        self.speed = 0.0
        self.turn_speed = 0

        self.inp_x = 0
        self.inp_y = 0

        self.gas = False
        self.brake = False
        self.left_turn = False
        self.right_turn = False

        #self.trail_car = None
        self.trail_renderer = tr.TrailRenderer()

    def bound(self):
        if self.center_y > HEIGHT:
            self.center_y = 0
        if self.center_y < 0:
            self.center_y = HEIGHT
        if self.center_x > WIDTH:
            self.center_x = 0
        if self.center_x < 0:
            self.center_x = WIDTH

    def lerp(self, lower, upper, val):
        return lower + (upper - lower)*val
    
    def processInput(self):
        if self.gas:
            self.inp_y += 0 if self.inp_y >= 1 else y_sensitivity
        if not self.gas and self.inp_y >= 0:
            self.inp_y = 0 if self.inp_y <= .1 else self.inp_y - y_sensitivity
        if self.brake: 
            self.inp_y -= 0 if self.inp_y <= -1 else y_sensitivity
        if not self.brake and self.inp_y < 0:
            self.inp_y = 0 if self.inp_y >= -.1 else self.inp_y + y_sensitivity

        if self.left_turn:
            self.inp_x += 0 if self.inp_x >= 1 else x_sensitivity
        if not self.left_turn and self.inp_x >= 0:
            self.inp_x = 0 if self.inp_x <= .1 else self.inp_x - x_sensitivity
        if self.right_turn: 
            self.inp_x -= 0 if self.inp_x <= -1 else x_sensitivity
        if not self.right_turn and self.inp_x < 0:
            self.inp_x = 0 if self.inp_x >= -.1 else self.inp_x + x_sensitivity
        
    def on_update(self, delta_time):
        print("\n------")
        #print(self.speed)
        #print(self.get_adjusted_hit_box())

        self.bound()
        self.processInput()

        resultant = math.sqrt(self.move_force_y**2 + self.move_force_x**2)
        self.speed = resultant
        
        self.move_force_y += (self.forward_y * top_speed * self.inp_y * delta_time) if resultant < top_speed else 0
        self.move_force_x += (self.forward_x * top_speed * self.inp_y * delta_time) if resultant < top_speed else 0

        self.change_angle = self.inp_x * resultant * max_turn * delta_time
        self.angle += self.change_angle

        angle_rad = math.radians(self.angle)
        self.forward_x = math.sin(angle_rad)
        self.forward_y = math.cos(angle_rad)
        
        self.move_force_y *= friction if not self.gas else 1
        self.move_force_x *= friction if not self.gas else 1

        self.center_y += self.move_force_y * delta_time
        self.center_x -= self.move_force_x * delta_time
        
        self.move_force_x += (self.forward_x - self.move_force_x) * delta_time * grip
        self.move_force_y += (self.forward_y - self.move_force_y) * delta_time * grip
        
        #self.update_trail_car()

        #TrailHandler.render_trail()
        print(self.gas, self.brake,self.left_turn, self.right_turn)

    def update_trail_car(self, other):
        other.center_x = self.center_x
        other.center_y = self.center_y
        other.angle = self.angle

    def drawTrail(self, other):
        #print("here: ", other)
        self.trail_renderer.render_trail(other, self)
    
    #def draw(self):
    #    print("here")
    #    self.trail.render_trail()

