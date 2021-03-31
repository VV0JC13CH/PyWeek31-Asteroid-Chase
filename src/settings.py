"""
settings.py

Place for SettingsView class.
"""

import arcade
import assets
from button import Button


class SettingsView(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        full_resolution_mode_state = self.window.fullscreen
        developer_mode_state = self.window.developer_mode
        music_mode_state = self.window.music_enabled

        if full_resolution_mode_state:
            self.button_full_resolution = Button(x=self.window.width/2, y=self.window.height * 4 / 6,
                                                 width=500, height=100,
                                                 texture_idle='full_off', texture_hover='full_off_hover')
        else:
            self.button_full_resolution = Button(x=self.window.width / 2, y=self.window.height * 4 / 6,
                                                 width=500, height=100,
                                                 texture_idle='full_on', texture_hover='full_on_hover')
        if music_mode_state:
            self.button_music_enabled = Button(x=self.window.width / 2, y=self.window.height * 3 / 6,
                                               width=500, height=100,
                                               texture_idle='music_off', texture_hover='music_off_hover')
        else:
            self.button_music_enabled = Button(x=self.window.width / 2, y=self.window.height * 3 / 6,
                                               width=500, height=100,
                                               texture_idle='music_on', texture_hover='music_on_hover')
        if developer_mode_state:
            self.button_developer_mode = Button(x=self.window.width / 2, y=self.window.height * 2 / 6,
                                                width=500, height=100,
                                                texture_idle='dev_off', texture_hover='dev_off_hover')
        else:
            self.button_developer_mode = Button(x=self.window.width / 2, y=self.window.height * 2 / 6,
                                                width=500, height=100,
                                                texture_idle='dev_on', texture_hover='dev_on_hover')
        self.button_back_menu = Button(x=self.window.width / 2, y=self.window.height * 1 / 6, width=500, height=100,
                                       texture_idle='back_menu', texture_hover='back_menu_hover')

    def on_show_view(self):
        self.window.cursor.change_state(state='idle')

    def on_update(self, delta_time: float):
        self.button_full_resolution.detect_mouse(self.window.cursor)
        self.button_music_enabled.detect_mouse(self.window.cursor)
        self.button_developer_mode.detect_mouse(self.window.cursor)
        self.button_back_menu.detect_mouse(self.window.cursor)

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_menu)

        self.button_full_resolution.draw()
        self.button_music_enabled.draw()
        self.button_developer_mode.draw()
        self.button_back_menu.draw()

        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_full_resolution.current_state == 'hover':
            self.window.set_fullscreen(not self.window.fullscreen)
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)
            for button in assets.button_register:
                button.center_horizontally(self.window)
            if self.window.fullscreen:
                self.button_full_resolution.replace_textures('full_off', 'full_off_hover')
            else:
                self.button_full_resolution.replace_textures('full_on', 'full_on_hover')
        if self.button_music_enabled.current_state == 'hover':
            self.window.music_enabled = not self.window.music_enabled
            if self.window.music_enabled:
                self.button_music_enabled.replace_textures('music_off', 'music_off_hover')
                self.window.music_manager.play_song()
            else:
                self.button_music_enabled.replace_textures('music_on', 'music_on_hover')
                self.window.music_manager.stop_song()
        if self.button_developer_mode.current_state == 'hover':
            self.window.developer_mode = not self.window.developer_mode
            if self.window.developer_mode:
                self.button_developer_mode.replace_textures('dev_off', 'dev_off_hover')
            else:
                self.button_developer_mode.replace_textures('dev_on', 'dev_on_hover')
        if self.button_back_menu.current_state == 'hover':
            self.window.show_view(self.previous_view)