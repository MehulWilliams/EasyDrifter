import arcade as arc
import arcade.key
import arcade.color
from PIL import Image
import car
import ncar

debug = True

WIDTH = car.WIDTH
HEIGHT = car.HEIGHT


class Game(arc.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, fullscreen=False)
        self.camera = None
        self.background = None
        self.player_list = None
        self.Car = None
        self.trail_car = None
        self.startingline = None
        self.dt = None
        self.AtlasRegion = None
        self.bg = None
        self.init = None

        self.img = None
        self.backgroundTexture = None
        self.counter = 0
        

    def setup(self):
        arc.set_background_color(arc.color.WHEAT)
        arc.enable_timings()
        self.camera = arcade.Camera(self.width, self.height)
        #self.TextureAtlas = arc.TextureAtlas((2560, 1600))
        self.startimg = Image.open("tracks/track16s.png")
        self.img = self.startimg
        self.backgroundTexture = arc.Texture('backg', self.img)
        self.initTexture = arc.Texture.create_empty('init', (3500, 3500))
        #self.TextureAtlas.add(self.backgroundTexture)
        self.init = arcade.Sprite(center_x=0, center_y=0, texture=self.initTexture)
        #self.bg = arcade.Sprite(center_x=0, center_y=0, texture=self.backgroundTexture)

        # Create the spritelist and add the sprite
        #spritelist = arcade.SpriteList()
        # Adding the sprite will also add the texture to the atlas
        #spritelist.append(sprite)
        #self.backgroundTexture = arc.Texture('backg', self.img.rotate(45))
        #self.background = arc.load_texture("tracks/track16.png", width=720, height=450)
        self.player_list = arc.SpriteList()
        self.texture_list = arc.SpriteList()
        self.Car = ncar.Car("images/car.png", .16)
        #self.StockCar = ncar.StockCar("images/car.png", .16)
        #self.trail_car = car.Car("images/car.png",  .112)  # .7x
        #self.player_list.append(self.init)
        #self.player_list.append(self.bg)
        self.player_list.append(self.init)
        self.player_list.append(self.Car)
        self.startingline = arc.create_polygon([(800, 840), (800, 720), (803, 840), (803, 720)], arc.color.WHITE)
        self.dt = 0
        

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
        screen_center_y = self.Car.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        #if screen_center_x < 0:
        #    screen_center_x = 0
        #if screen_center_y < 0:
        #    screen_center_y = 0
        #player_centered = screen_center_x, screen_center_y

        self.camera.move_to((screen_center_x, screen_center_y))


    def on_draw(self):
        self.counter += 1
        self.camera.use()
        arc.start_render()

        #arc.cleanup_texture_cache()
        #self.img = self.startimg.rotate(int(self.Car.nangle), center=(self.Car.center_x, self.Car.center_y))
        #newTexture = arc.Texture(f"new{self.counter}", self.startimg.rotate(int(self.Car.nangle), center=(self.Car.center_x, self.Car.center_y)))
        #newTexture.draw_scaled(self.Car.center_x, self.Car.center_y)
        

        
        #with self.player_list.atlas.render_into(self.initTexture) as framebuffer:
            # Clear the allocated region in the atlas (if you need it)
            #framebuffer.clear()
            # From here on we can draw using any arcade draw functionality
            #self.img = self.startimg.rotate(int(self.Car.nangle), center=(self.Car.center_x, self.Car.center_y))
            #self.bg.texture.image = self.img
            #self.player_list.atlas.update_texture_image(self.backgroundTexture)
            #newTexture = arc.Texture.draw_scaled()
            #self.texture_list.atlas.clear()
            #framebuffer.clear()
            #self.backgroundTexture = arc.Texture(f"new{self.counter}", self.startimg.rotate(int(self.Car.nangle), center=(self.Car.center_x, self.Car.center_y)))
            #self.backgroundTexture.draw_scaled(self.Car.center_x, self.Car.center_y)
            
        self.texture_list.atlas.add(arc.Texture(f"new{self.counter}", self.startimg.rotate(int(self.Car.nangle), center=(self.Car.center_x, self.Car.center_y))))
        self.texture_list.draw()
            #arc.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.backgroundTexture)
            
            #newTexture.draw_scaled(self.Car.center_x, self.Car.center_y)
            #arc.draw_scaled_texture_rectangle(self.Car.center_x, self.Car.center_y, self.backgroundTexture)
        #save = self.img.rotate(int(self.Car.nangle), center=(self.Car.center_x, self.Car.center_y))
        #self.backgroundTexture = arc.Texture('backg', self.background)
        #self.background = arc.load_texture("tracks/track16.png")
        #print(self.Car.nangle)
        #self.img = self.startimg.rotate(45)
        #self.img = self.img.crop((0, 0, WIDTH, HEIGHT))
        #self.backgroundTexture.image = self.img
        #self.TextureAtlas.update_texture_image(self.backgroundTexture)
        #self.TextureAtlas.update_texture_image()
        #self.backgroundTexture = arc.Texture(f'backg{self.counter}', self.img)
        
        #arc.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.TextureAtlas.clear)
        
        #self.background = arc.Texture(f"backg{self.counter}", self.img.crop((self.Car.center_x-500, self.Car.center_y-300, self.Car.center_x+500, self.Car.center_y+300)))
        #arc.draw_scaled_texture_rectangle(self.Car.center_x, self.Car.center_y, self.player_list.atlas., angle=self.Car.nangle)

        #self.Car.drawTrail(self.trail_car)
        self.Car.TrailRenderer.render_trail()
        #self.StockCar.TrailRenderer.render_trail()
        self.player_list.draw()
       # self.texture_list.draw()

        arc.draw_text("fps: " + str(int(arc.get_fps())), WIDTH-650,
                      HEIGHT-30, arc.color.YELLOW, align="right", width=600)

        if debug:
            #arc.draw_text("self.Car.speed " + str(round(self.Car.speed//10, 0)*10),
            #              WIDTH-650, HEIGHT-50, arc.color.YELLOW, align="right", width=600)
            arc.draw_text(str(round(self.Car.speed//10*10,0)), self.Car.center_x+20, self.Car.center_y+20, arc.color.YELLOW, align="right", width=50)
            
            self.startingline.draw()
            #print(arc.are_polygons_intersecting(()))
            magnitude = self.Car.speed
            aim_x = self.Car.center_x - (self.Car.fx + self.Car.move_force_x) * magnitude
            aim_y = self.Car.center_y + (self.Car.fy + self.Car.move_force_y) * magnitude
            arc.draw_point(aim_x, aim_y, arc.color.BLUE, 5)

            aim_x = self.Car.center_x - (self.Car.fx) * magnitude
            aim_y = self.Car.center_y + (self.Car.fy) * magnitude
            arc.draw_point(aim_x, aim_y, arc.color.RED, 5)
            '''
            aim_x = self.StockCar.center_x - (self.StockCar.move_force_x)
            aim_y = self.StockCar.center_y + (self.StockCar.move_force_y)
            arc.draw_point(aim_x, aim_y, arc.color.GREEN, 4)

            aim_x = self.StockCar.center_x - (self.StockCar.fx)*self.StockCar.speed
            aim_y = self.StockCar.center_y + (self.StockCar.fy)*self.StockCar.speed
            arc.draw_point(aim_x, aim_y, arc.color.GREEN, 4)
            '''
            #for i in self.Car.radar_list:
            #    arc.draw_point(i[1], i[2], arc.color.YELLOW, 5)

            self.draw_input_graph()

    def on_update(self, delta_time):
        self.player_list.on_update()
        self.center_camera_to_player()
        self.dt = delta_time
        print("\n\n\n")

    def on_key_press(self, symbol, modifiers):
        if symbol == arc.key.ESCAPE:
            arc.close_window()
        if symbol == arc.key.R:
            self.Car.reset()

        if symbol == arc.key.W or symbol == arc.key.UP:
            self.Car.gas = True
            self.StockCar.gas = True
        if symbol == arc.key.S or symbol == arc.key.DOWN:
            self.Car.brake = True
            self.StockCar.brake = True
        if symbol == arc.key.A or symbol == arc.key.LEFT:
            self.Car.left_turn = True
            self.StockCar.left_turn = True
        if symbol == arc.key.D or symbol == arc.key.RIGHT:
            self.Car.right_turn = True
            self.StockCar.right_turn = True
        if symbol == arcade.key.TAB:
            self.Car.handbrake = True
            self.StockCar.handbrake = True
        if symbol == arc.key.SPACE:
            self.Car.speedboost = True
            self.StockCar.speedboost = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.Car.gas = False
            self.StockCar.gas = False
        if symbol == arcade.key.S or symbol == arc.key.DOWN:
            self.Car.brake = False
            self.StockCar.brake = False
        if symbol == arcade.key.A or symbol == arc.key.LEFT:
            self.Car.left_turn = False
            self.StockCar.left_turn = False
        if symbol == arcade.key.D or symbol == arc.key.RIGHT:
            self.Car.right_turn = False
            self.StockCar.right_turn = False
        if symbol == arcade.key.TAB:
            self.Car.handbrake = False
            
        if symbol == arc.key.SPACE:
            self.Car.speedboost = False
        


if __name__ == "__main__":
    app = Game()
    app.set_update_rate(1/60)
    app.setup()
    arc.run()
