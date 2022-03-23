from tkinter import N
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.metrics import dp
from platform import platform
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, Clock, ObjectProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse, Quad, Triangle
from kivy.app import App
from ctypes import pointer
from kivy.core.window import Window
import kivy
from kivy.lang import Builder
import math
import random
from kivy.core.audio import SoundLoader


Builder.load_file("menu.kv")


class GalexyApp(App):
    pass


class MainWidget(RelativeLayout):
    menu_text = StringProperty("G A L E X Y")
    button_text = StringProperty("START")
    menu_widget = ObjectProperty
    perspective_x = NumericProperty(0)
    perspective_y = NumericProperty(0)
    vertical_lines = []
    v_lines_number = 20
    v_lines_spacing = 0.2  # percetage in screen
    count_v = -1 * int(v_lines_number//2)
    horizontal_lines = []
    H_lines_number = 14
    H_lines_spacing = 0.2  # percetage in screen
    count_h = -1 * int(H_lines_number//2)
    offset = 0
    offset2 = 0
    dir_x = 0
    speed = 3.0/400
    speed2 = 9/900.0
    n_tiles = 15
    tiles = []
    tiles_coordinate = []
    current_y_loop = 0
    ship = None
    ship_width = .1
    ship_height = .05
    shilp_base_y = .01
    ship_cordinate = [(0, 0), (0, 0), (0, 0)]
    game_over = False
    start = False
    score = NumericProperty(0)
    begin = None
    galaxy = None
    gameover_impact = None
    gameover_voice = None
    music1 = None
    restart = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_audio()
        self.galaxy.play()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.fill_tiles()
        self.init_tiles()
        self.init_ship()
        self.generate_tiles_coordinate()
        Clock.schedule_interval(self.update, 1/60.0)
        self.galaxy

    def reset(self):
        self.game_over = False
        self.tiles_coordinate = []
        self.fill_tiles()
        self.generate_tiles_coordinate()
        self.offset = 0
        self.current_y_loop = 0
        self.offset2 = 0

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.is_desktop:
            if keycode[1] == 'left':
                self.dir_x = 10  # self.width/2 * self.H_lines_spacing
            elif keycode[1] == 'right':
                self.dir_x = -10  # -1 * self.width/2 * self.H_lines_spacing

    def _on_keyboard_up(self, keyboard, keycode):  # releasing r-l key
        pass

    def is_desktop(self):
        if platform is ("win", "linux", "macos"):
            return True
        else:
            return False

    def _on_parent(self, widget, parrent):
        pass

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        self.ship_cordinate[0] = (
            self.width/2 - self.ship_width * self.width/2, self.shilp_base_y * self.height)
        self.ship_cordinate[1] = (self.width/2, self.ship_height * self.height)
        self.ship_cordinate[2] = (
            self.width/2 + self.ship_width * self.width/2, self.shilp_base_y * self.height)
        x1, y1 = self.dimantion(
            (self.width/2 - self.ship_width * self.width/2, self.shilp_base_y * self.height))
        x2, y2 = self.dimantion((self.width/2, self.ship_height * self.height))
        x3, y3 = self.dimantion(
            (self.width/2 + self.ship_width * self.width/2, self.shilp_base_y * self.height))
        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def ship_in_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinate(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinate(ti_x+1, ti_y+1)
        xcenter = self.ship_cordinate[1][0]
        ycenter = self.ship_cordinate[1][1]
        if not(xmin <= xcenter <= xmax and ymin <= ycenter <= ymax):
            return False
        else:
            return True

    def check_ship(self):
        for i in range(len(self.tiles_coordinate)):
            ti_x, ti_y = self.tiles_coordinate[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.ship_in_tile(ti_x, ti_y):
                return True

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.n_tiles):
                self.tiles.append(Quad())

    def generate_tiles_coordinate(self):
        for i in range(len(self.tiles_coordinate)-1, -1, -1):
            if self.tiles_coordinate[i][1] < self.current_y_loop:
                del self.tiles_coordinate[i]
        last_y = 0
        last_x = 0
        if len(self.tiles_coordinate) > 0:
            last_y = self.tiles_coordinate[-1][1] + 1
            last_x = self.tiles_coordinate[-1][0]
        r = random.randint(-1, 1)
        for i in range(len(self.tiles_coordinate), self.n_tiles):
            if last_x + r > math.ceil(self.v_lines_number/4.0) or last_x + r < -1*math.ceil(self.v_lines_number/4.0):
                r = 0
            if r == 0:
                self.tiles_coordinate.append((last_x + r, last_y))
                last_y += 1
            elif r == 1:
                self.tiles_coordinate.append((last_x + r, last_y-1))
                self.tiles_coordinate.append((last_x + r, last_y))
                last_y += 1
            elif r == -1:
                self.tiles_coordinate.append((last_x + r, last_y-1))
                self.tiles_coordinate.append((last_x + r, last_y))
                last_y += 1

    def fill_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.n_tiles):
                self.tiles_coordinate.append((0, i))

    def update_tiles(self):
        for i in range(self.n_tiles):
            tile_x = self.tiles_coordinate[i][0]
            tile_y = self.tiles_coordinate[i][1]
            xmin, ymin = self.get_tile_coordinate(tile_x, tile_y)
            xmax, ymax = self.get_tile_coordinate(tile_x+1, tile_y+1)
            x1, y1 = self.dimantion((xmin, ymin))
            x2, y2 = self.dimantion((xmin, ymax))
            x3, y3 = self.dimantion((xmax, ymax))
            x4, y4 = self.dimantion((xmax, ymin))
            self.tiles[i].points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.v_lines_number):
                self.vertical_lines.append(Line(width=1))
            # for i in range(self.v_lines_number):
            #     self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        line_x = self.perspective_x + \
            (index-.5) * self.v_lines_spacing * self.width/2 + self.offset2
        return line_x

    def get_line_y_from_index(self, index):
        line_y = index * self.H_lines_spacing * self.height/2 - self.offset - 2
        return line_y

    def get_tile_coordinate(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_vertical_lines(self):
        num = self.count_v
        for i in range(self.v_lines_number):
            x_cordinate = self.width/2+num*self.width/2*self.v_lines_spacing + \
                self.width/2*self.v_lines_spacing * 0.5 + self.offset2
            first_cordinate = self.dimantion((x_cordinate, 0))
            second_cordinate = self.dimantion((x_cordinate, self.height))
            self.vertical_lines[i].points = [
                *first_cordinate, *second_cordinate]
            num += 1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(self.H_lines_number):
                self.horizontal_lines.append(Line(width=1))
            # for i in range(self.v_lines_number):
            #     self.vertical_lines.append(Line())

    def update_horizontal_lines(self):
        num = self.count_h
        minx = self.width/2+self.count_v*self.width/2*self.v_lines_spacing + \
            self.width/2*self.v_lines_spacing * 0.5 + self.offset2
        maxx = self.width/2-self.count_v*self.width/2*self.v_lines_spacing - \
            self.width/2*self.v_lines_spacing * 0.5 + self.offset2
        for i in range(self.H_lines_number):
            y_cordinate = self.height/2+num*self.height/2*self.H_lines_spacing - self.offset
            first_cordinate = self.dimantion((minx, y_cordinate))
            second_cordinate = self.dimantion((maxx, y_cordinate))
            self.horizontal_lines[i].points = [
                *first_cordinate, *second_cordinate]
            num += 1

    def dimantion(self, cordinate):
        # return cordinate
        return self.perspective_3D(cordinate)

    def perspective_3D(self, cordinate):
        alpha_y = self.perspective_y/self.height
        lin_y = alpha_y * cordinate[1]
        del_y = self.perspective_y - lin_y
        factor_x = del_y/self.perspective_y
        factor_x = pow(factor_x, 4)
        del_x = cordinate[0]-self.perspective_x
        res_x = self.perspective_x + factor_x * del_x
        res_y = self.perspective_y - factor_x * self.perspective_y
        return(res_x, res_y)

    def on_size(self, *args):
        self.perspective_x = self.width/2
        self.perspective_y = 3/4*self.height
        # self.update_vertical_lines()
        # self.update_horizontal_lines()

    def update(self, dt):
        if (not self.game_over) and self.start:
            speed = self.speed * self.height
            speed2 = self.speed2 * self.width
            self.update_tiles()
            self.offset += speed
            self.offset2 += self.dir_x * speed2
            if self.offset >= self.height/2 * self.H_lines_spacing:
                self.offset = 0
                self.current_y_loop += 1
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.generate_tiles_coordinate()
        self.update_ship()
        self.score = self.current_y_loop
        if (not self.check_ship()) and (not self.game_over):
            self.game_over = True
            self.start = False
            self.menu_widget.opacity = 1
            self.menu_text = "G A M E  O V E R"
            self.button_text = "RESTART"
            self.begin.stop()
            self.gameover_impact.play()
            self.gameover_voice.play()
            print("Game Over")
        self.dir_x = 0

    def on_touch_down(self, touch):
        if (not self.game_over) and (self.start):
            if touch.x < self.width/2:
                self.dir_x = 10  # self.width/2 * self.H_lines_spacing
            elif touch.x > self.width/2:
                self.dir_x = -10  # -1 * self.width/2 * self.H_lines_spacing
        return super(MainWidget, self).on_touch_down(touch)

    def on_menu_press(self):
        if self.game_over:
            self.restart.play()
        else:
            self.begin.play()
        self.reset()
        self.start = True
        self.menu_widget.opacity = 0
        self.music1.play()
    
    def init_audio(self):
        self.begin = SoundLoader.load("begin.wav")
        self.galaxy = SoundLoader.load("galaxy.wav")
        self.gameover_impact = SoundLoader.load("gameover_impact.wav")
        self.gameover_voice = SoundLoader.load("gameover_voice.wav")
        self.music1 = SoundLoader.load("music1.wav")
        self.restart = SoundLoader.load("restart.wav")
        self.begin.volume = 1
        self.galaxy.volume = .25
        self.gameover_impact.volume = .25
        self.gameover_voice.volume = .25
        self.music1.volume = .25
        self.restart.volume = .6





if __name__ == "__main__":
    application = GalexyApp()
    application.run()
