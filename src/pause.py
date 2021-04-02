"""
pause.py

Place for PauseView class.
It's possible to pause a game in game and campaign views by pressing ESC button.
Current state of the game is passed as argument to instance of PauseView object.
"""

import arcade
import assets


from button import Button
from developer import log


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.button_back_game = Button(x=self.window.width / 6 * 4, y=self.window.height * 5 / 6,
                                       width=500, height=100,
                                       texture_idle='back_game', texture_hover='back_game_hover')
        self.button_back_camp = Button(x=self.window.width / 6 * 4, y=self.window.height * 5 / 6,
                                       width=500, height=100,
                                       texture_idle='back_camp', texture_hover='back_camp_hover')
        self.button_back_menu = Button(x=self.window.width / 6 * 2, y=self.window.height * 1 / 6,
                                       width=500, height=100,
                                       texture_idle='back_menu', texture_hover='back_menu_hover')

    def on_show_view(self):
        self.window.cursor.change_state(state='idle')

    def on_update(self, delta_time: float):
        if self.window.current_view_name == 'pause_view_after_game':
            self.button_back_game.detect_mouse(self.window.cursor)
        if self.window.current_view_name == 'pause_view_after_campaign':
            self.button_back_camp.detect_mouse(self.window.cursor)
        self.button_back_menu.detect_mouse(self.window.cursor)

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_menu)
        if self.window.current_view_name == 'pause_view_after_game':
            self.button_back_game.draw()
        if self.window.current_view_name == 'pause_view_after_campaign':
            self.button_back_camp.draw()
        self.button_back_menu.draw()

        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_back_game.current_state == 'hover':
            self.window.show_view(self.game_view)
            log('Scene switched to ' + str(self.game_view))
        if self.button_back_camp.current_state == 'hover':
            log('Scene switched to ' + str(self.window.campaign_view))
            self.window.show_view(self.window.campaign_view)
        if self.button_back_menu.current_state == 'hover':
            self.window.show_view(self.window.start_view)
            log('Scene switched to ' + str(self.window.start_view))
