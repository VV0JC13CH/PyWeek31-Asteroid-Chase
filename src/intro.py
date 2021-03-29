"""
intro.py

Place for IntroView class.
"""

import arcade
import assets
from game import GameView


class IntroView(arcade.View):
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
        arcade.draw_text("Click to start a game", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE_SMOKE, font_size=20, anchor_x="center")
        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)
