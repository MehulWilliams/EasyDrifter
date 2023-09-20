import arcade as arc
import arcade.key
import arcade.color
import car

debug = True

WIDTH = car.WIDTH
HEIGHT = car.HEIGHT

class Game(arc.Window):
    def __init__(self):
        super().__init__(fullscreen=True)
        self.camera = None
        self.background = None
        self.player_list = None
        self.player_car = None
        self.trail_car = None

    def setup(self):
        arc.set_background_color(arc.color.WHEAT)
        arc.enable_timings()
        self.background = self.background = arc.load_texture("track7.png")
        self.player_list = arc.SpriteList()
        self.player_car = car.Car("images/car.png", .20)
        self.trail_car = car.Car("images/car.png",  .14) # .7x
        self.player_list.append(self.player_car)

    def on_draw(self):
        arc.start_render()
        arc.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)

        self.player_car.drawTrail(self.trail_car)
        self.player_list.draw()

        if debug:
            arc.draw_text("fps: " + str(int(arc.get_fps())), WIDTH-650, HEIGHT-30, arc.color.YELLOW, align="right", width=600)
            arc.draw_text("self.player_car.on_track " + str(self.player_car.on_track), WIDTH-650, HEIGHT-50, arc.color.YELLOW, align="right", width=600)
            arc.draw_text("self.player_car.grip " + str(self.player_car.grip), WIDTH-650, HEIGHT-70, arc.color.YELLOW, align="right", width=600)

            aim_x = self.player_car.center_x - (self.player_car.move_force_x)/3
            aim_y = self.player_car.center_y + (self.player_car.move_force_y)/3
            arc.draw_point(aim_x, aim_y, arc.color.RED, 5)

            #aim_x = self.player_car.center_x - (self.player_car.forward_x*13)
            #aim_y = self.player_car.center_y + (self.player_car.forward_y*13)
            #arc.draw_point(aim_x, aim_y, arc.color.GREEN, 5)

            for i in self.player_car.radar_list:
                arc.draw_point(i[1], i[2], arc.color.YELLOW, 5)
            

    def on_update(self, delta_time):
        self.player_list.on_update()
        self.player_car.update_trail_car(self.trail_car)
        print("\n\n\n\n\n\n")

    def on_key_press(self, symbol, modifiers):
        if symbol == arc.key.ESCAPE:
            arc.close_window()
        if symbol == arc.key.R:
            self.player_car.reset()

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

if __name__ == "__main__":
    app = Game()
    app.setup()
    arc.run()