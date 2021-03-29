"""
cursor.py

Place for Cursor class.
"""

import arcade
import assets


class Cursor(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.idle = assets.cursor_idle
        self.hover = assets.cursor_hover
        self.no = assets.cursor_no
        self.current_state = 'idle'
        self.append(self.idle)

    def change_state(self, state):
        self.current_state = state
        if state == 'hover':
            self.sprite_list.clear()
            self.append(self.hover)
        elif state == 'no':
            self.sprite_list.clear()
            self.append(self.no)
        elif state == 'off':
            self.sprite_list.clear()
        else:
            self.sprite_list.clear()
            self.append(self.idle)

    def get_position(self, dx, dy):
        for sprite in self:
            sprite.center_x = dx
            sprite.center_y = dy