"""
menu.py

Place for MenuView class.
"""

import arcade
import assets
from intro import IntroView
from settings import SettingsView
from button import Button


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.button_play = Button(x=self.window.width/2,
                                  y=self.window.height*3/6,
                                  width=500, height=100,
                                  texture_idle='play',
                                  texture_hover='play_hover'
                                  )
        self.button_settings = Button(x=self.window.width / 2,
                                      y=self.window.height * 2 / 6,
                                      width=500, height=100,
                                      texture_idle='settings',
                                      texture_hover='settings_hover'
                                      )
        self.button_exit = Button(x=self.window.width / 2,
                                  y=self.window.height * 1 / 6,
                                  width=500, height=100,
                                  texture_idle='exit',
                                  texture_hover='exit_hover'
                                  )

    def on_update(self, delta_time: float):
        self.button_play.detect_mouse(self.window.cursor)
        self.button_settings.detect_mouse(self.window.cursor)
        self.button_exit.detect_mouse(self.window.cursor)

    def on_draw(self):
        self.window.fps_counter.on_draw_start()
        arcade.start_render()
        # In order to count FPS in proper way, add objects below:

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_menu)

        self.button_play.draw()
        self.button_settings.draw()
        self.button_exit.draw()

        self.window.fps_counter.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_play.current_state == 'hover':
            intro_view = IntroView()
            self.window.show_view(intro_view)
        elif self.button_settings.current_state == 'hover':
            settings_view = SettingsView()
            self.window.show_view(settings_view)
        elif self.button_exit.current_state == 'hover':
            self.window.close()
