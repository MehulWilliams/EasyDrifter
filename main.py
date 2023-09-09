import arcade as arc
import arcade.key
import arcade.color
import car
import numpy as np

debug = True

WIDTH = car.WIDTH
HEIGHT = car.HEIGHT

class Game(arc.Window):
    def __init__(self):
        super().__init__(fullscreen=True)
        self.tile_map = None
        self.scene = None
        self.physics_engine = None
        self.camera = None
        self.background = None

    def setup(self):
        arc.set_background_color(arc.color.WHEAT)
        arc.enable_timings()
        self.player_list = arc.SpriteList()
        self.player_car = car.Car("images/car.png", .2)
        self.trail_car = car.Car("images/car.png", .14) # .7x
        self.player_list.append(self.player_car)
        
        self.background = arc.load_texture("track4.png")

    def on_draw(self):
        arc.start_render()
        arc.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)

        self.player_car.drawTrail(self.trail_car)
        self.player_list.draw()

        if debug:
            arc.draw_point(100,100, arc.color.WHITE, .5)
            arc.draw_text("self.player_car.angle " + str(self.player_car.angle), WIDTH-230, HEIGHT-30, arc.color.RED, align="right", width=200)
            arc.draw_text("self.player_car.first_angle " + str(self.player_car.first_angle), WIDTH-230, HEIGHT-40, arc.color.RED, align="right", width=200)

            slip_x = self.player_car.center_x - (self.player_car.move_force_x)/3
            slip_y = self.player_car.center_y + (self.player_car.move_force_y)/3
            arc.draw_line(self.player_car.center_x, self.player_car.center_y, slip_x, slip_y, arc.color.RED, 3)

            slip_x = self.player_car.center_x - (self.player_car.fx * 200)/3
            slip_y = self.player_car.center_y + (self.player_car.fy * 200)/3
            arc.draw_line(self.player_car.center_x, self.player_car.center_y, slip_x, slip_y, arc.color.YELLOW, 3)



       


    def on_update(self, delta_time):
        self.player_list.on_update()
        self.player_car.update_trail_car(self.trail_car)
        #print(arcade.get_fps())
        print("\n\n\n\n\n\n")

    def on_key_press(self, symbol, modifiers):
        if symbol == arc.key.ESCAPE:
            arc.close_window()

        if symbol == arc.key.W or symbol == arc.key.UP:
            self.player_car.gas = True
        if symbol == arc.key.S or symbol == arc.key.DOWN:
            self.player_car.brake = True
        if symbol == arc.key.A or symbol == arc.key.LEFT:
            self.player_car.left_turn = True
        if symbol == arc.key.D or symbol == arc.key.RIGHT:
            self.player_car.right_turn = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player_car.gas = False
        if symbol == arcade.key.S or symbol == arc.key.DOWN:
            self.player_car.brake = False
        if symbol == arcade.key.A or symbol == arc.key.LEFT:
            self.player_car.left_turn = False
        if symbol == arcade.key.D or symbol == arc.key.RIGHT:
            self.player_car.right_turn = False
            
        

    #def on_mouse_motion(self, x, y, dx, dy):
    #    print("mouse")



if __name__ == "__main__":
    app = Game()
    app.setup()
    arc.run()