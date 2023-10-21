import arcade as arc
import arcade.key
import arcade.color
from PIL import Image
import car

debug = True

WIDTH = car.WIDTH
HEIGHT = car.HEIGHT
SCALE = car.SCALE


class Game(arc.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, fullscreen=True)
        self.camera = None
        self.background = None
        self.player_list = None
        self.Car = None
        self.trail_car = None
        self.AtlasRegion = None
        self.bg = None
        self.init = None

        self.img = None
        self.backgroundTexture = None
        self.counter = 0
        

    def setup(self):
        arc.set_background_color(arc.color.BLACK)
        arc.enable_timings()
        self.camera = arcade.Camera(self.width, self.height)
        self.startimg = Image.open("tracks/track2.png")
        self.img = self.startimg
        self.backgroundTexture = arc.Texture('backg', self.img)
        self.player_list = arc.SpriteList()
        self.texture_list = arc.SpriteList()
        self.Car = car.Car("images/car.png", .22*SCALE)
        self.player_list.append(self.Car)
        

    def draw_input_graph(self):
        max = 100
        width = 30
        # outline:
        arc.draw_lrtb_rectangle_outline(150, 150+width, 300, 300-max*2, arc.color.RED)
        arc.draw_lrtb_rectangle_outline(65, 65+max*2, 100, 100-width, arc.color.GREEN)

        # fill:
        vert = self.Car.vertical_input
        horiz = self.Car.horizontal_input
        if (vert >= 0):
            arc.draw_lrtb_rectangle_filled(150, 150+width, 200+(max*vert), 200, arc.color.RED)
        else:
            arc.draw_lrtb_rectangle_filled(150, 150+width, 200, 200+(max*vert), arc.color.RED)
        if (horiz >= 0):
            arc.draw_lrtb_rectangle_filled(165-(max*horiz), 165, 100, 100-width, arc.color.GREEN)
        else:
            arc.draw_lrtb_rectangle_filled(165, 165-(max*horiz), 100, 100-width, arc.color.GREEN)
  
    def center_camera_to_player(self):
        screen_center_x = self.Car.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.Car.center_y - (self.camera.viewport_height / 2) + 30
        self.camera.move_to((screen_center_x, screen_center_y), .17)


    def on_draw(self):
        self.counter += 1
        self.camera.use()
        arc.start_render()
        arc.draw_lrwh_rectangle_textured(0, 0, WIDTH*SCALE, HEIGHT*SCALE, self.backgroundTexture)
        self.Car.TrailRenderer.render_trail()
        self.player_list.draw()
        arc.draw_text("fps: " + str(int(arc.get_fps())), WIDTH-650,
                      HEIGHT-30, arc.color.YELLOW, align="right", width=600)

        if debug:
            #self.draw_input_graph()
            arc.draw_text(str(round((self.Car.speed/SCALE),0)), self.Car.center_x+20, self.Car.center_y+20, arc.color.YELLOW, align="right", width=50)
            
            aim_x = self.Car.center_x - (self.Car.move_force_x)/2
            aim_y = self.Car.center_y + (self.Car.move_force_y)/2
            arc.draw_point(aim_x, aim_y, arc.color.LIGHT_BLUE, 5)

    def on_update(self, delta_time):
        self.player_list.on_update()
        self.center_camera_to_player()
        self.dt = delta_time
        print("\n"*3) 

    def on_key_press(self, symbol, modifiers):
        if symbol == arc.key.ESCAPE:
            arc.close_window()
        if symbol == arc.key.R:
            self.Car.reset()

        if symbol == arc.key.W or symbol == arc.key.UP:
            self.Car.gas = True
        if symbol == arc.key.S or symbol == arc.key.DOWN:
            self.Car.brake = True
        if symbol == arc.key.A or symbol == arc.key.LEFT:
            self.Car.left_turn = True
        if symbol == arc.key.D or symbol == arc.key.RIGHT:
            self.Car.right_turn = True
        if symbol == arcade.key.TAB:
            self.Car.handbrake = True
        if symbol == arc.key.SPACE:
            self.Car.speedboost = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.Car.gas = False
        if symbol == arcade.key.S or symbol == arc.key.DOWN:
            self.Car.brake = False
        if symbol == arcade.key.A or symbol == arc.key.LEFT:
            self.Car.left_turn = False
        if symbol == arcade.key.D or symbol == arc.key.RIGHT:
            self.Car.right_turn = False
        if symbol == arcade.key.TAB:
            self.Car.handbrake = False
        if symbol == arc.key.SPACE:
            self.Car.speedboost = False
        


if __name__ == "__main__":
    app = Game()
    app.set_update_rate(1/60)
    app.setup()
    arc.run()
