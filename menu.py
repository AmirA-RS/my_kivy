from kivy.core.window import Window
from ctypes import pointer
from kivy.app import App
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse, Quad, Triangle
from kivy.graphics.context_instructions import Color
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, Clock
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from platform import platform
from kivy.metrics import dp
class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)
