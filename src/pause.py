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
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shift_pressed = False
        self.space_pressed = False
        self.escape_pressed = False
        self.keyboard_int = 8
        self.keyboard_image = assets.keyboard_hints_paths[7]

    def on_show_view(self):
        self.window.cursor.change_state(state='idle')

    def on_update(self, delta_time: float):
        if self.window.current_view_name == 'pause_view_after_game':
            self.button_back_game.detect_mouse(self.window.cursor)
        if self.window.current_view_name == 'pause_view_after_campaign':
            self.button_back_camp.detect_mouse(self.window.cursor)
        self.button_back_menu.detect_mouse(self.window.cursor)
        if self.shift_pressed:
            self.keyboard_int = 1
        elif self.escape_pressed:
            self.keyboard_int = 2
        elif self.left_pressed:
            self.keyboard_int = 3
        elif self.down_pressed:
            self.keyboard_int = 4
        elif self.right_pressed:
            self.keyboard_int = 5
        elif self.up_pressed:
            self.keyboard_int = 6
        elif self.space_pressed:
            self.keyboard_int = 7
        else:
            self.keyboard_int = 8
        self.keyboard_image = assets.keyboard_hints_paths[self.keyboard_int-1]

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_menu)
        arcade.draw_lrwh_rectangle_textured(self.window.width/2-500, self.window.height/2-200,
                                            500*2, 200*2,
                                            self.keyboard_image)

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

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True
        elif key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.LSHIFT:
            self.shift_pressed = True
        elif key == arcade.key.ESCAPE:
            self.escape_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.LSHIFT:
            self.shift_pressed = False
        elif key == arcade.key.ESCAPE:
            self.escape_pressed = False
