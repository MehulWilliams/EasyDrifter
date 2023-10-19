import arcade as arc
import math

WIDTH = 1440
HEIGHT = 900

OFF_ROAD = (0, 0, 0)

super_top_speed = 140
super_grip = .5

turn_speed = 250

super_accel_rate = .03
brake_rate = .025
coast_rate = .01

pos_turn_rate = .05
neg_turn_rate = .08

    
class Car(arc.Sprite): 
    def __init__(self, texture, scaling):
        super().__init__(texture, scaling, hit_box_algorithm=None)

        self.center_x = WIDTH/2
        self.center_y = 800

        self.move_force_x = 0
        self.move_force_y = 0
        self.adjusted_x = 0
        self.adjusted_y = 0
        self.fx = 0
        self.fy = 0
        self.change_x = 0
        self.change_y = 0
        self.angle = 270
        self.radar_poll = 0
        self.radar_rays = 4
        self.radar_list = [(0,0,0)] * self.radar_rays
     
        self.top_speed = super_top_speed
        self.speed = 0.0

        self.horizontal_input = 0
        self.vertical_input = 0

        self.grip = super_grip
        self.accel_rate = super_accel_rate

        self.gas = False
        self.brake = False
        self.handbrake = False
        self.speedboost = False
        self.left_turn = False
        self.right_turn = False

        self.handbraking = False
        self.boosting = False

        self.TrailRenderer = Trail(self, texture)
        self.on_track = ()
        

    def reset(self):
        self.center_x = WIDTH/2
        self.center_y = 800

        self.move_force_x = 0
        self.move_force_y = 0
        self.fx = 0
        self.fy = 0
        self.angle = 270

        self.speed = 0.0

    def bound(self):
        if self.center_y > HEIGHT:
            self.center_y = 0
        if self.center_y < 0:
            self.center_y = HEIGHT
        if self.center_x > WIDTH:
            self.center_x = 0
        if self.center_x < 0:
            self.center_x = WIDTH

    def handle_speed_physics(self):
        return
    
    def adjust_top_speed(self, multiplier):
        self.boosting = True
        self.top_speed = super_top_speed * multiplier

    def reset_top_speed(self):
        self.boosting = False
        self.top_speed = super_top_speed
    
    def adjust_grip(self, multiplier):
        self.grip = super_grip * multiplier
        self.top_speed = super_top_speed * multiplier

    def reset_grip(self):
        self.grip = super_grip
        self.top_speed = super_top_speed

    # format: [controller input] -/+= 0 if [controller input] >/<= [deadzone] else [nudge value]
    def processInput(self):
        if self.speedboost: #boost
            if not self.boosting:
                self.adjust_top_speed(1.7)
        else:
            self.reset_top_speed()
        if self.gas: #accel
            self.vertical_input += 0 if self.vertical_input >= 1 else self.accel_rate
        if not self.gas and self.vertical_input >= 0: # coasting
            self.vertical_input = 0 if self.vertical_input <= .1 else self.vertical_input - coast_rate
        if self.brake: #brake
            self.adjust_grip(1.5)
            self.vertical_input -= 0 if self.vertical_input <= -1 else brake_rate
        if not self.brake and self.vertical_input < 0:
            self.reset_grip()
            self.vertical_input = 0 if self.vertical_input >= -.1 else self.vertical_input + coast_rate
        
        if self.handbrake: #slide
            #self.vertical_input = .2
            self.adjust_grip(.7)
        else: 
            self.reset_grip()
        
        if self.left_turn:
            #if self.horizontal_input < 0:
            #    self.horizontal_input = 0
            self.horizontal_input += 0 if self.horizontal_input >= 1 else pos_turn_rate
        if not self.left_turn and self.horizontal_input >= 0:
            self.horizontal_input = 0 if self.horizontal_input <= .1 else self.horizontal_input - neg_turn_rate
        if self.right_turn: 
            #if self.horizontal_input > 0:
            #    self.horizontal_input = 0
            self.horizontal_input -= 0 if self.horizontal_input <= -1 else pos_turn_rate
        if not self.right_turn and self.horizontal_input < 0:
            self.horizontal_input = 0 if self.horizontal_input >= -.1 else self.horizontal_input + neg_turn_rate

        self.handle_speed_physics()
        
    # polling_rate = n, where radar polls once every n frames
    def update_radar_list(self, angle_rad, polling_rate=5, FOV=2.094396): #fov in radians
        print(angle_rad)
        angle = angle_rad - (FOV/2)
        #angle = angle_rad - 1.047198
        radar_range = 40

        radar_steps = 5  #how many points to sample along ray.
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
                
                while(j <= max_dist):
                    stepped_x = self.center_x - (_x * j)
                    stepped_y = self.center_y + (_y * j)
                    if (i == 1):
                        print(self.center_x, stepped_x, self.center_y, stepped_y)
                    #self.on_track = True if arc.get_pixel(self.center_x - self.fx*12, self.center_y + self.fy*12, 3) == OFF_ROAD else False
                    if (arc.get_pixel(stepped_x, stepped_y) == OFF_ROAD):
                        dist = arc.get_distance(self.center_x, self.center_y, stepped_x, stepped_y)
                        self.radar_list[i] = (dist, stepped_x, stepped_y)
                        j += max_dist
                    j += single_step
                
                #self.radar_list[i] = (max_dist, self.center_x - _x*radar_range, self.center_y + _y*radar_range)
                

                angle += (FOV/(self.radar_rays-1))  
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
        
    #def limitspeed(self):
        #if self.

    def limitspeed(self):
        if self.speed > self.top_speed:
            self.speed = self.top_speed
    '''
    def on_update(self, delta_time):
        print("\n------")

        self.bound()
        self.processInput()
        
        #self.on_track = True if arc.get_pixel(self.center_x - self.fx*12, self.center_y + self.fy*12, 3) == OFF_ROAD else False
        
        #if (arc.get_pixel(self.center_x - self.fx*12, self.center_y + self.fy*12, 3) == OFF_ROAD) :
        #    self.on_track = True 
            #self.reset()
            #print("resetting")
    
        

        modifiers = self.top_speed * self.vertical_input * delta_time
        self.move_force_x += (self.fx * modifiers)
        self.move_force_y += (self.fy * modifiers)
        #print("move_force_x: ", self.move_force_x, self.fx*5 - self.move_force_x * delta_time)


        self.change_angle = self.horizontal_input * turn_speed * delta_time
        self.angle += self.change_angle
        self.angle %= 360

        self.fx = math.sin(self.radians)
        self.fy = math.cos(self.radians)
        print(self.fx, self.fy)
        #self.update_radar_list(angle_rad)


        
        self.center_x -= self.move_force_x * delta_time
        self.center_y += self.move_force_y * delta_time
        #arc.get_distance()

        print(self.fx, self.fy)
        print(self.move_force_x, self.move_force_y)
        print(self.fx - self.move_force_x, self.fy - self.move_force_y)
        self.move_force_x += ((self.fx - self.move_force_x)) * delta_time
        self.move_force_y += ((self.fy - self.move_force_y)) * delta_time

        self.speed = math.sqrt(self.move_force_y**2 + self.move_force_x**2)




        #self.limitspeed()
        #self.velocity

        self.TrailRenderer.update_trail()
    '''
     
    def on_update(self, delta_time):
        print("\n------")

        self.bound()
        self.processInput()
        
        #self.on_track = True if arc.get_pixel(self.center_x - self.fx*12, self.center_y + self.fy*12, 3) == OFF_ROAD else False
        
        #if (arc.get_pixel(self.center_x - self.fx*12, self.center_y + self.fy*12, 3) == OFF_ROAD) :
        #    self.on_track = True 
            #self.reset()
            #print("resetting")
    
        

        modifiers = self.top_speed * self.vertical_input * delta_time
        self.move_force_x += (self.fx * modifiers)
        self.move_force_y += (self.fy * modifiers)
        #print("move_force_x: ", self.move_force_x, self.fx*5 - self.move_force_x * delta_time)


        self.change_angle = self.horizontal_input * turn_speed * delta_time
        self.angle += self.change_angle
        self.angle %= 360

        self.fx = math.sin(self.radians)
        self.fy = math.cos(self.radians)
        #self.update_radar_list(angle_rad)


        
        self.center_x -= self.move_force_x * delta_time
        self.center_y += self.move_force_y * delta_time
        #arc.get_distance()

        print(self.fx, self.fy)
        print(self.move_force_x, self.move_force_y)
        print((self.fx - self.move_force_x) * delta_time, (self.fy - self.move_force_y) * delta_time)
        self.change_x = ((self.fx - self.move_force_x) * delta_time) if abs(self.change_x) > 5 else 0
        self.change_y = ((self.fy - self.move_force_y) * delta_time) if abs(self.change_y) > 5 else 0
        self.move_force_x += ((self.fx - self.move_force_x)) * delta_time
        self.move_force_y += ((self.fy - self.move_force_y)) * delta_time
        if abs(self.move_force_x) < 0.01:
            self.move_force_x = 0
        if abs(self.move_force_y) < 0.01:
            self.move_force_y = 0

        self.speed = math.sqrt(self.move_force_y**2 + self.move_force_x**2)




        #self.limitspeed()
        #self.velocity

        self.TrailRenderer.update_trail()

    ''' 
    def update_trail_car(self, trail_car):
        trail_car.center_x = self.center_x
        trail_car.center_y = self.center_y
        trail_car.angle = self.angle
        self.TrailRenderer.update_trail(trail_car)

    def drawTrail(self):
        #return
        self.TrailRenderer.render_trail()
    '''


class Trail():
    def __init__(self, car, texture, ):
        #self.trail = [ {'l': (2, 3), 'r': (3, 4), 'angle': 90, 'alpha': 255}, {'x': (2, 3), 'y': (3, 4), 'angle': 90, 'alpha': 255}, ... ]
        self.trail = []
        self.counter = 0
        self.tire_size = 4
        self.sections = 7
        self.spacing = 7
        self.alpha_step = 255/self.sections
        self.tire = arc.load_texture("images/tire.png")
        self.Car = car
        self.PositionSprite = arc.Sprite(texture, self.Car.scale*.75)


    def update_trail(self):
        self.PositionSprite.angle = self.Car.angle
        self.PositionSprite.set_position(self.Car.position[0], self.Car.position[1])
        if(self.counter == self.spacing):
            a = self.PositionSprite.get_adjusted_hit_box()
            print(a)
            self.trail.insert(0, {'l': a[0], 'r': a[1], 'angle'
                                  : self.PositionSprite.angle, 'alpha':  255})
            self.counter = 0
            for i in self.trail:
                i['alpha'] -= self.alpha_step if i['alpha'] > 0 else 0
            if len(self.trail) > self.sections-1:
                del self.trail[self.sections-1]
        self.counter += 1

    def render_trail(self):
      for i in self.trail:
         arc.draw_scaled_texture_rectangle(i['l'][0], i['l'][1], self.tire, .5, i['angle'], i['alpha'])
         arc.draw_scaled_texture_rectangle(i['r'][0], i['r'][1], self.tire, .5, i['angle'], i['alpha'])




class StockCar(Car):
    def __init__(self, texture, scaling):
        super().__init__(texture, scaling)
 
    def on_update(self, delta_time):
        print("\n------")

        self.bound()
        self.processInput()
        
        #self.on_track = True if arc.get_pixel(self.center_x - self.fx*12, self.center_y + self.fy*12, 3) == OFF_ROAD else False
        
        #if (arc.get_pixel(self.center_x - self.fx*12, self.center_y + self.fy*12, 3) == OFF_ROAD) :
        #    self.on_track = True 
            #self.reset()
            #print("resetting")
    
        self.speed = math.sqrt(self.move_force_y**2 + self.move_force_x**2)

        modifiers = self.top_speed * self.vertical_input * delta_time
        self.move_force_x += (self.fx * modifiers)
        self.move_force_y += (self.fy * modifiers)

        self.change_angle = self.horizontal_input * turn_speed * delta_time
        self.angle += self.change_angle
        self.angle %= 360

        self.fx = math.sin(self.radians)
        self.fy = math.cos(self.radians)
        #self.update_radar_list(angle_rad)


        
        self.center_x -= self.move_force_x * delta_time
        self.center_y += self.move_force_y * delta_time
        #arc.get_distance()
        
        self.move_force_x += ((self.fx - self.move_force_x) * delta_time)
        self.move_force_y += ((self.fy - self.move_force_y) * delta_time)

        self.limitspeed()
        #self.velocity

        self.TrailRenderer.update_trail()
