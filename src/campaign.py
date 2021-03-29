"""
intro.py

Place for IntroView class.
"""

import arcade
import assets
import data
import pause
from button import Button
from developer import log

# --- Constants ---
param = data.load_parameters()

# Size of the first level (intro plays only before first level)
LEVEL_WIDTH = int(param['LEVEL']['DEFAULT_WIDTH'])
LEVEL_HEIGHT = int(param['LEVEL']['DEFAULT_HEIGHT'])


class CampaignView(arcade.View):
    def __init__(self):
        super().__init__()
        if self.window.pause_view is None:
            self.window.pause_view = pause.PauseView(self)

        self.button_skip = Button(x=self.window.width / 6 * 5,
                                  y=self.window.height * 1 / 8,
                                  width=250, height=50,
                                  texture_idle='skip_intro',
                                  texture_hover='skip_intro_hover'
                                  )

    def on_update(self, delta_time: float):
        self.button_skip.detect_mouse(self.window.cursor)

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()
        # In order to count FPS in proper way, add objects below:

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_menu)

        arcade.draw_text("Intro Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        self.button_skip.draw()
        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass
