"""
button.py

Place for Button class.
"""

import arcade
import assets
import data

# --- Constants ---
param = data.load_parameters()
BUTTON_WIDTH = int(param['UI']['BUTTON_SPRITE_SHEET_WIDTH'])
BUTTON_HEIGHT = int(param['UI']['BUTTON_SPRITE_SHEET_HEIGHT'])


class Button(arcade.SpriteList):
    def __init__(self, textures,
                 texture_idle,
                 texture_hover,
                 width=200,
                 height=200,
                 x=200,
                 y=200,
                 ):

        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.textures = textures

        self.idle = self.textures[texture_idle]
        self.hover = self.textures[texture_hover]

        self.all_sprites = [self.idle, self.hover]
        self.current_state = 'idle'
        self.append(self.idle)
        for sprite in self.all_sprites:
            sprite.center_x = self.x
            sprite.center_y = self.y
            sprite.width = self.width
            sprite.height = self.height

    def change_state(self, state):
        self.current_state = state
        if state == 'hover':
            self.sprite_list.clear()
            self.append(self.hover)
        else:
            self.sprite_list.clear()
            self.append(self.idle)

    def detect_mouse(self, mouse_instance):
        if arcade.check_for_collision_with_list(self[0], mouse_instance):
            self.change_state(state='hover')
        else:
            self.change_state(state='idle')


class SimpleButton(arcade.Sprite):
    """ Simple graphical button """
    def __init__(self, button_col, button_row):
        """ Set up button """
        super().__init__(filename=assets.buttons_sprites,
                         image_x=BUTTON_WIDTH*button_col,
                         image_y=BUTTON_HEIGHT*button_row,
                         image_width=BUTTON_WIDTH,
                         image_height=BUTTON_HEIGHT,
                         )
