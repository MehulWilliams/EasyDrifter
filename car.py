import arcade as arc
import math
import trail as tr

WIDTH = 1440
HEIGHT = 900

OFF_ROAD = (0, 0, 0)

top_speed = 1000

max_turn = 1.5

accel_rate = .03
coast_rate = .015
brake_rate = .02

pos_turn_rate = .025
neg_turn_rate = .25


class Car(arc.Sprite): 
    #new env
    def __init__(self, texture, scaling):
        super().__init__(texture, scaling, hit_box_algorithm=None)

        self.center_x = WIDTH/2
        self.center_y = 800

        self.move_force_x = 0
        self.move_force_y = 0
        self.forward_x = 0
        self.forward_y = 0
        self.angle = 270
        self.radar_poll = 0
        self.radar_rays = 4
        self.radar_list = [(0,0,0)] * self.radar_rays
                           
        self.speed = 0.0
        self.turn_speed = 0

        self.horizontal_input = 0
        self.vertical_input = 0

        self.grip = 4

        self.gas = False
        self.brake = False
        self.left_turn = False
        self.right_turn = False

        self.trail_renderer = tr.TrailRenderer()
        self.on_track = ()

    def reset(self):
        self.center_x = WIDTH/2
        self.center_y = 800

        self.move_force_x = 0
        self.move_force_y = 0
        self.forward_x = 0
        self.forward_y = 0
        self.angle = 270

        self.speed = 0.0
        self.turn_speed = 0

    def bound(self):
        if self.center_y > HEIGHT:
            self.center_y = 0
        if self.center_y < 0:
            self.center_y = HEIGHT
        if self.center_x > WIDTH:
            self.center_x = 0
        if self.center_x < 0:
            self.center_x = WIDTH


    # format: [controller input] -/+= 0 if [controller input] >/<= [deadzone] else [nudge value]
    def processInput(self):
        if self.gas: #accel
            pos_turn_rate = .03
            self.grip = 4
            self.vertical_input += 0 if self.vertical_input >= 1 else accel_rate
        else:
            pos_turn_rate = .05
            self.grip = 5
        if not self.gas and self.vertical_input >= 0: # coasting
            self.vertical_input = 0 if self.vertical_input <= .1 else self.vertical_input - coast_rate
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
        
    # polling_rate = n, where radar polls once every n frames
    def update_radar_list(self, angle_rad, polling_rate=2, FOV=2.094396): #fov in radians
        
        angle = angle_rad - (FOV/2)
        #angle = angle_rad - 1.047198
        radar_range = 50

        radar_steps = 7  #how many points to sample along ray.
        if self.radar_poll == polling_rate-1:
            self.radar_poll = 0
            for i in range(len(self.radar_list)):
                _x = math.sin(angle)
                _y = math.cos(angle)
                #radar_range = max(_x*radar_scale, _y*radar_scale)
                
                self.radar_list[i] = (radar_range, self.center_x - _x*radar_range, self.center_y + _y*radar_range)
                
                max_dist = arc.get_distance(self.center_x, self.center_y, self.center_x - _x*radar_range, self.center_y + _y*radar_range)
                single_step = int(max_dist/radar_steps)
                j = single_step
                #print("max_dist:", max_dist, "j:", j)
                #j *= 2
                
                while(j <= max_dist):
                    stepped_x = self.center_x - (_x * j)
                    stepped_y = self.center_y + (_y * j)
                    if (i == 1):
                        print(self.center_x, stepped_x, self.center_y, stepped_y)
                    #self.on_track = True if arc.get_pixel(self.center_x - self.forward_x*12, self.center_y + self.forward_y*12, 3) == OFF_ROAD else False
                    if (arc.get_pixel(stepped_x, stepped_y) == OFF_ROAD):
                        dist = arc.get_distance(self.center_x, self.center_y, stepped_x, stepped_y)
                        self.radar_list[i] = (dist, stepped_x, stepped_y)
                        j += max_dist
                    j += single_step
                
                #self.radar_list[i] = (max_dist, self.center_x - _x*radar_range, self.center_y + _y*radar_range)
                

                angle += (FOV/(self.radar_rays-1))  
                #angle += 0.523599         #(0.523599 = 30 deg in rad)
        else :
            self.radar_poll += 1


        '''if self.radar_poll == polling_rate-1:
            self.radar_poll = 0
            for i in range(5):
                self.radar_list[i] = (self.center_x - math.sin(angle)*radar_range, self.center_y + math.cos(angle)*radar_range)
                angle += 0.523599        #(0.523599 = 30 deg in rad)
        else:
            self.radar_poll += 1
        '''
        
    def on_update(self, delta_time):
        print("\n------")

        self.bound()
        self.processInput()
        
        #self.on_track = True if arc.get_pixel(self.center_x - self.forward_x*12, self.center_y + self.forward_y*12, 3) == OFF_ROAD else False
        
        #if (arc.get_pixel(self.center_x - self.forward_x*12, self.center_y + self.forward_y*12, 3) == OFF_ROAD) :
        #    self.on_track = True 
            #self.reset()
            #print("resetting")
        
    
        self.speed = math.sqrt(self.move_force_y**2 + self.move_force_x**2)

        self.move_force_x += (self.forward_x * top_speed * self.vertical_input * delta_time) if self.speed < top_speed else 0
        self.move_force_y += (self.forward_y * top_speed * self.vertical_input * delta_time) if self.speed < top_speed else 0

        self.change_angle = self.horizontal_input * self.speed * max_turn * delta_time
        self.angle += self.change_angle
        self.angle %= 360

        angle_rad = math.radians(self.angle)
        self.forward_x = math.sin(angle_rad)
        self.forward_y = math.cos(angle_rad)

        self.update_radar_list(angle_rad)
        
        self.center_x -= self.move_force_x * delta_time
        self.center_y += self.move_force_y * delta_time
        
        self.move_force_x += (self.forward_x - self.move_force_x * self.grip) * delta_time
        self.move_force_y += (self.forward_y - self.move_force_y * self.grip) * delta_time


    def update_trail_car(self, trail_car):
        trail_car.center_x = self.center_x
        trail_car.center_y = self.center_y
        trail_car.angle = self.angle
        self.trail_renderer.update_trail(trail_car)

    def drawTrail(self, other):
        self.trail_renderer.render_trail(other, self)