"""
pause.py

Place for PauseView class.
It's possible to pause a game in game and campaign views by pressing ESC button.
Current state of the game is passed as argument to instance of PauseView object.
"""

import arcade
import assets

from button import Button


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        self.button_back_game = Button(x=self.window.width / 6 * 4, y=self.window.height * 5 / 6,
                                       width=500, height=100,
                                       texture_idle='back_game', texture_hover='back_game_hover')
        self.button_back_menu = Button(x=self.window.width / 6 * 2, y=self.window.height * 1 / 6,
                                       width=500, height=100,
                                       texture_idle='back_menu', texture_hover='back_menu_hover')

    def on_update(self, delta_time: float):
        self.button_back_game.detect_mouse(self.window.cursor)
        self.button_back_menu.detect_mouse(self.window.cursor)

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_menu)
        self.button_back_game.draw()
        self.button_back_menu.draw()

        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_back_game.current_state == 'hover':
            self.window.show_view(self.game_view)
        if self.button_back_menu.current_state == 'hover':
            self.window.show_view(self.window.start_view)
