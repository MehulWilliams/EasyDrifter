import arcade as arc
import arcade.key
import arcade.color
import car

WIDTH = car.WIDTH
HEIGHT = car.HEIGHT

class Game(arc.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "game")

    def setup(self):
        arc.set_background_color(arc.color.WHEAT)
        arcade.enable_timings()
        self.player_list = arc.SpriteList()
        self.player_car = car.Car("images/car.png", .5)
        self.trail_car = car.Car("images/car.png", .35)
        #self.player_car.trail_car = self.trail_car
        self.player_list.append(self.player_car)
        

    def on_draw(self):
        arc.start_render()        
        self.player_car.drawTrail(self.trail_car)
        self.player_list.draw()


    def on_update(self, delta_time):
        self.player_list.on_update()
        self.player_car.update_trail_car(self.trail_car)
        print(arcade.get_fps())
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