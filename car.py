import arcade as arc
import math
import trail as tr


WIDTH = 1440
HEIGHT = 900

top_speed = 200
friction = 1
grip = 1.5

#make grip a function of current speed, decreasing with increase of speed

max_turn = 2.25

accel_rate = .03
brake_rate = .05
pos_turn_rate = .02
neg_turn_rate = .05


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
        #self.grip = 1

        self.horizontal_input = 0
        self.vertical_input = 0

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
    
    # [basecase] 
    def processInput(self):
        if self.gas: #accel
            self.vertical_input += 0 if self.vertical_input >= 1 else accel_rate
        if not self.gas and self.vertical_input >= 0: # coasting
            self.vertical_input = 0 if self.vertical_input <= .1 else self.vertical_input - accel_rate
        if self.brake: #brake
            self.vertical_input -= 0 if self.vertical_input <= -1 else brake_rate
        if not self.brake and self.vertical_input < 0:
            self.vertical_input = 0 if self.vertical_input >= -.1 else self.vertical_input + accel_rate

        if self.left_turn:
            self.horizontal_input += 0 if self.horizontal_input >= 1 else pos_turn_rate
        if not self.left_turn and self.horizontal_input >= 0:
            self.horizontal_input = 0 if self.horizontal_input <= .1 else self.horizontal_input - neg_turn_rate
        if self.right_turn: 
            self.horizontal_input -= 0 if self.horizontal_input <= -1 else pos_turn_rate
        if not self.right_turn and self.horizontal_input < 0:
            self.horizontal_input = 0 if self.horizontal_input >= -.1 else self.horizontal_input + neg_turn_rate
        
    def on_update(self, delta_time):
        print("\n------")
        #print(self.speed)
        #print(self.get_adjusted_hit_box())
        '''if(self.speed < top_speed/4): # 175
            self.grip = 2.6
            print("1")
        else:
            self.grip = 2.3
            print("2.3")'''


        self.bound()
        self.processInput()

        self.speed = math.sqrt(self.move_force_y**2 + self.move_force_x**2)
        self.speed = self.speed

        self.move_force_x += (self.forward_x * top_speed * self.vertical_input * delta_time) if self.speed < top_speed else 0
        self.move_force_y += (self.forward_y * top_speed * self.vertical_input * delta_time) if self.speed < top_speed else 0

        self.change_angle = self.horizontal_input * self.speed * max_turn * delta_time * grip
        self.first_angle = self.angle
        self.angle += self.change_angle
        self.angle %= 360

        angle_rad = math.radians(self.angle)
        self.forward_x = math.sin(angle_rad)
        self.forward_y = math.cos(angle_rad)
        self.fx = self.forward_x
        self.fy = self.forward_y
        
        #self.move_force_y *= friction if not self.gas else 1
        #self.move_force_x *= friction if not self.gas else 1
        
        self.center_y += self.move_force_y * delta_time
        self.center_x -= self.move_force_x * delta_time
        
        self.move_force_x += (self.forward_x - self.move_force_x) * delta_time
        self.move_force_y += (self.forward_y - self.move_force_y) * delta_time
        
        #self.update_trail_car()

        #TrailHandler.render_trail()
        #print(self.gas, self.brake,self.left_turn, self.right_turn)

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

