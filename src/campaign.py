"""
campaign.py

Place for CampaignView class.
"""

import arcade
from game import GameView


class CampaignView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.window.fps_counter.on_draw_start()
        arcade.start_render()
        arcade.draw_text("Campaign Screen", self.window.width/2, self.window.height/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Choose one from unlocked levels.", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        self.window.fps_counter.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)
