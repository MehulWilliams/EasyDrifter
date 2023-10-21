import arcade as arc
import math

WIDTH = 2880
HEIGHT = 1800
SCALE = 7

OFF_ROAD = (0, 0, 0)

super_top_speed = 75 * SCALE # pixels/sec
super_grip = 3

turn_speed = 180 # degrees/sec
drift_speed = 50

super_accel_rate = .007
brake_rate = .03
coast_rate = .007

pos_turn_rate = .08
neg_turn_rate = .2

    
class Car(arc.Sprite): 
    def __init__(self, texture, scaling):
        super().__init__(texture, scaling, hit_box_algorithm=None)

        self.center_x = WIDTH/2
        self.center_y = 300

        self._internal_mf_x = 0
        self._internal_mf_y = 0

        self.move_force_x = 0
        self.move_force_y = 0
        self.adjusted_x = 0
        self.adjusted_y = 0
        self.fx = 0
        self.fy = 0
        self.dx = 0
        self.dy = 0
        self.change_x = 0
        self.change_y = 0
        self.angle = 90
        self.radar_poll = 0
        self.radar_rays = 4
        self.radar_list = [(0,0,0)] * self.radar_rays

        self.nangle = 0
        self.drift_angle = 0
     
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
    

    def bound(self):
        if self.center_y > HEIGHT * SCALE:
            self.center_y = 0
        if self.center_y < 0:
            self.center_y = HEIGHT * SCALE
        if self.center_x > WIDTH * SCALE:
            self.center_x = 0
        if self.center_x < 0:
            self.center_x = WIDTH * SCALE

    
    # format: [controller input] -/+= 0 if [controller input] >/<= [deadzone] else [nudge value]
    # vertical and horizontal input is between [-1,1],[-1,1], like a joystick
    def processInput_o(self):
        if self.gas: #accel
            self.vertical_input += 0 if self.vertical_input >= 1 else self.accel_rate
        if not self.gas and self.vertical_input >= 0: # coasting
            self.vertical_input = 0 if self.vertical_input <= .1 else self.vertical_input - coast_rate
        if self.brake: #brake
            self.vertical_input -= 0 if self.vertical_input <= -1 else brake_rate
        if not self.brake and self.vertical_input < 0:
            self.vertical_input = 0 if self.vertical_input >= -.1 else self.vertical_input + coast_rate
        
        if self.left_turn:
            self.horizontal_input += 0 if self.horizontal_input >= 1 else pos_turn_rate
        if not self.left_turn and self.horizontal_input >= 0:
            self.horizontal_input = 0 if self.horizontal_input <= .1 else self.horizontal_input - neg_turn_rate
        if self.right_turn: 
            self.horizontal_input -= 0 if self.horizontal_input <= -1 else pos_turn_rate
        if not self.right_turn and self.horizontal_input < 0:
            self.horizontal_input = 0 if self.horizontal_input >= -.1 else self.horizontal_input + neg_turn_rate
        

    def processInput(self):
        if self.speedboost:
            if not self.boosting:
                self.top_speed = super_top_speed * 1.4
            self.boosting = True
        else:
            self.boosting = False
            self.top_speed = super_top_speed
        if self.gas and self.vertical_input <= 1:       #accel
            self.vertical_input += self.accel_rate
        if self.brake:                                  #brake
            if self.vertical_input >= -1:
                self.vertical_input -= brake_rate
        if not self.gas and self.vertical_input >= 0:   #coasting
            if self.vertical_input <= .15:
                self.vertical_input = 0 
            else:
                self.vertical_input -= coast_rate
        if not self.brake and self.vertical_input < 0:  #coasting from reverse
            if self.vertical_input >= -.15:
                self.vertical_input = 0 
            else:
                self.vertical_input += coast_rate
        
        if self.left_turn and self.horizontal_input <= 1:
            if self.horizontal_input < 0:
                self.horizontal_input = 0
            self.horizontal_input += pos_turn_rate
        if self.right_turn and self.horizontal_input >= -1: 
            if self.horizontal_input > 0:
                self.horizontal_input = 0
            self.horizontal_input -= pos_turn_rate
        if not self.left_turn and self.horizontal_input >= 0:
            if self.horizontal_input <= .35:
                self.horizontal_input = 0
            else:
                self.horizontal_input -= neg_turn_rate
        if not self.right_turn and self.horizontal_input < 0:
            if self.horizontal_input >= -.35:
                self.horizontal_input = 0
            else:
                self.horizontal_input += neg_turn_rate
    
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
        
    def move_force_deadzone(self):
        #print("self._internal_mf_  :", (self._internal_mf_x)//10*10, (self._internal_mf_y)//10*10)
        #print("self.move_force_    : ", (self.move_force_x)//10*10, (self.move_force_y)//10*10)
        #print("self.angle          :", self.angle//10*10)
        #print("self.drift_angle    :", self.drift_angle//10*10, "\n")
        #print("change  angle       :", (self.angle - self.drift_angle)//10*10)
        #print(self.horizontal_input)
        #print(self.speed)
        return
    def limitspeed(self):
        if self.speed > self.top_speed:
            self.speed = self.top_speed

    
    def on_update(self, delta_time):
        print("\n-----")
        self.bound()
        self.processInput()
        self.TrailRenderer.update_trail()

        self.change_angle = self.horizontal_input * turn_speed * delta_time
        self.angle += self.change_angle
        
        modifiers = self.top_speed * self.vertical_input
        self.fx = (math.sin(self.radians)) * modifiers
        self.fy = (math.cos(self.radians)) * modifiers

        self.center_x -= (self.fx) * delta_time
        self.center_y += (self.fy) * delta_time

        self.speed = math.sqrt(self.fx**2 + self.fy**2)
        #self.limitspeed()
        #self.drift_angle = 

        #print(self.fx, self.fy)
        #print(self.move_force_x, self.move_force_y)
        

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
        self.s = [[265.0089837885673, 1598.3220118315116], [266.1656637885673, 1596.6137218315116], [275.4725637885673, 1594.8276718315115], [277.17842378856733, 1595.9843518315115], [281.2097937885673, 1616.9844118315116], [280.2450837885673, 1618.4083918315116], [270.4619037885673, 1620.2867818315115], [269.0403537885673, 1619.3220718315115]]


    def update_trail(self):
        self.PositionSprite.angle = self.Car.angle
        self.PositionSprite.set_position(self.Car.position[0], self.Car.position[1])
        if(self.counter == self.spacing):
            a = self.PositionSprite.get_adjusted_hit_box()
            self.trail.insert(0, {'l': a[0], 'r': a[2], 'angle'
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
        super().__init__(texture, scaling*.9)
        #self.center_y += 10
 
    def on_update(self, delta_time):
        print("\n------")
        self.bound()
        self.processInput()
        
        self.speed = math.sqrt(self.move_force_y**2 + self.move_force_x**2)

        modifiers = self.top_speed * self.vertical_input * delta_time
        self.move_force_x += (self.fx * modifiers)
        self.move_force_y += (self.fy * modifiers)
        self._internal_mf_x = self.move_force_x
        self._internal_mf_y = self.move_force_y

        self.change_angle = self.horizontal_input * turn_speed * delta_time
        self.angle += self.change_angle
        self.angle %= 360
        self.drift_angle = math.degrees(math.atan2(self.move_force_y, -self.move_force_x))
        #self.drift_angle = math.degrees(math.atan2(x1*y2-y1*x2,x1*x2+y1*y2))

        self.fx = math.sin(self.radians)
        self.fy = math.cos(self.radians)
        
        self.center_x -= self.move_force_x * delta_time
        self.center_y += self.move_force_y * delta_time
        
        self.move_force_deadzone()
        self.move_force_x += ((self.fx - self.move_force_x) * delta_time)
        self.move_force_y += ((self.fy - self.move_force_y) * delta_time)

        #self.limitspeed()

        self.TrailRenderer.update_trail()



class ArcCar(Car):
    def __init__(self, texture, scaling):
        super().__init__(texture, scaling*.9)
        #self.center_y += 10
 
    def on_update(self, delta_time):
        print("\n------")
        self.bound()
        self.processInput()
        
        self.speed = math.sqrt(self.move_force_y**2 + self.move_force_x**2)

        self.move_force_x += (self.fx * delta_time)
        self.move_force_y += (self.fy * delta_time)
        self._internal_mf_x = self.move_force_x
        self._internal_mf_y = self.move_force_y

        self.change_angle = self.horizontal_input * turn_speed * delta_time
        self.angle += self.change_angle
        self.angle %= 360
        self.drift_angle = math.degrees(math.atan2(self.move_force_y, -self.move_force_x))

        self.fx = math.sin(self.radians) * self.top_speed * self.vertical_input
        self.fy = math.cos(self.radians) * self.top_speed * self.vertical_input
        
        self.center_x -= self.move_force_x * delta_time
        self.center_y += self.move_force_y * delta_time
        
        self.move_force_x += ((self.fx - self.move_force_x) * delta_time*self.grip)
        self.move_force_y += ((self.fy - self.move_force_y) * delta_time*self.grip)

        self.limitspeed()
        self.TrailRenderer.update_trail()

