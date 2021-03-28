"""
settings.py

Place for SettingsView class.
"""

import arcade


class SettingsView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.window.fps_counter.on_draw_start()
        arcade.start_render()
        arcade.draw_text("Settings Screen", self.window.width/2, self.window.height/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        self.window.fps_counter.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass
