"""
pause.py

Place for PauseView class.
It's possible to pause a game in game and campaign views by pressing ESC button.
Current state of the game is passed as argument to instance of PauseView object.
"""

import arcade


class PauseView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.window.fps_counter.on_draw_start()
        arcade.start_render()
        arcade.draw_text("Pause Screen", self.window.width/2, self.window.height/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("You can pause the game in game and campaign screens.", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        self.window.fps_counter.on_draw_finish()
