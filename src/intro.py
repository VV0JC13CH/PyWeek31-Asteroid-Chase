"""
intro.py

Place for IntroView class.
"""

import arcade
import assets
import data
from game import GameView
from button import Button
from developer import log

# --- Constants ---
param = data.load_parameters()

# Size of the first level (intro plays only before first level)
LEVEL_WIDTH = int(param['LEVEL']['DEFAULT_WIDTH'])
LEVEL_HEIGHT = int(param['LEVEL']['DEFAULT_HEIGHT'])


class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.current_view_name = 'intro_view'
        self.button_skip = Button(x=self.window.width,
                                  y=self.window.height * 1 / 8,
                                  width=250, height=50,
                                  texture_idle='skip_intro',
                                  texture_hover='skip_intro_hover'
                                  )
        self.background_reached_max = False
        self.start_shaking_buildings = True
        self.time = 0

    def on_show_view(self):
        self.window.cursor.change_state(state='idle')

    def on_update(self, delta_time: float):
        self.button_skip.detect_mouse(self.window.cursor)
        if self.start_shaking_buildings:
            if self.time < 4 and not self.background_reached_max:
                self.time += 0.4
            elif 5 >= self.time > 0:
                self.background_reached_max = True
                self.time -= 0.4
            else:
                self.background_reached_max = False

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()
        # In order to count FPS in proper way, add objects below:

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, -self.window.height,
                                            self.window.width, self.window.height*2,
                                            assets.intro_bg_paths[int(self.time)])

        self.button_skip.draw()
        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_skip.current_state == 'hover':
            self.window.game_view = GameView(LEVEL_WIDTH, LEVEL_HEIGHT)
            self.window.scenes.append(self.window.game_view)
            log('View switched to ' + str(self.window.game_view))
            self.window.show_view(self.window.game_view)
