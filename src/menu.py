"""
menu.py

Place for MenuView class.
"""

import arcade
import assets
import campaign
import intro
from settings import SettingsView
from button import Button
from developer import log


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.logo_counter = 0
        self.logo_switch = False
        self.window.current_view_name = 'menu_view'
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

    def on_show_view(self):
        self.window.cursor.change_state(state='idle')

    def on_update(self, delta_time: float):
        self.button_play.detect_mouse(self.window.cursor)
        self.button_settings.detect_mouse(self.window.cursor)
        self.button_exit.detect_mouse(self.window.cursor)
        if self.logo_counter < delta_time*25:
            self.logo_counter += delta_time
            self.logo_switch = True
        elif self.logo_counter < delta_time*50:
            self.logo_counter += delta_time
            self.logo_switch = False
        else:
            self.logo_counter = 0

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()
        # In order to count FPS in proper way, add objects below:

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_menu)
        if self.logo_switch:
            arcade.draw_lrwh_rectangle_textured(self.window.width/2-250, self.window.height*3.5/6,
                                                500, 200,
                                                assets.logo_1)
        else:
            arcade.draw_lrwh_rectangle_textured(self.window.width/2-250, self.window.height*3.5/6,
                                                500, 200,
                                                assets.logo_2)

        self.button_play.draw()
        self.button_settings.draw()
        self.button_exit.draw()

        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_play.current_state == 'hover':
            if self.window.levels_unlocked == 0:
                self.window.levels_unlocked = 1
                self.window.intro_view = intro.IntroView()
                self.window.scenes.append(self.window.intro_view)
                self.window.show_view(self.window.intro_view)
            else:
                log('Scene switched to ' + str(self.window.campaign_view))
                self.window.show_view(self.window.campaign_view)
        elif self.button_settings.current_state == 'hover':
            self.window.settings_view = SettingsView(self)
            self.window.scenes.append(self.window.settings_view)
            self.window.show_view(self.window.settings_view)
        elif self.button_exit.current_state == 'hover':
            self.window.close()
