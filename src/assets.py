"""
assets.py

Let's gather all resources from gfx/sfx here, like sprites and sounds.
"""

import arcade
import data

# we love Windows users:
from pathlib import Path

# --- Constants ---
param = data.load_parameters()
BUTTON_WIDTH = int(param['UI']['BUTTON_SPRITE_SHEET_WIDTH'])
BUTTON_HEIGHT = int(param['UI']['BUTTON_SPRITE_SHEET_HEIGHT'])


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


# Backgrounds
bg_menu = arcade.load_texture(path_to_string('gfx', 'bg_menu.png'))

# Buttons
buttons_sprites = path_to_string('gfx', 'buttons.png')


class Button(arcade.Sprite):
    """ Simple graphical button """
    def __init__(self, button_col, button_row):
        """ Set up button """
        super().__init__(filename=buttons_sprites,
                         image_x=BUTTON_WIDTH*button_col,
                         image_y=BUTTON_HEIGHT*button_row,
                         image_width=BUTTON_WIDTH,
                         image_height=BUTTON_HEIGHT,
                         )


button_pause_idle = Button(button_col=0, button_row=0)
button_pause_hover = Button(button_col=1, button_row=0)
button_reset_idle = Button(button_col=0, button_row=1)
button_reset_hover = Button(button_col=1, button_row=1)
button_music_off_idle = Button(button_col=0, button_row=2)
button_music_off_hover = Button(button_col=1, button_row=2)
button_music_on_idle = Button(button_col=0, button_row=3)
button_music_on_hover = Button(button_col=1, button_row=3)
button_full_off_idle = Button(button_col=0, button_row=4)
button_full_off_hover = Button(button_col=1, button_row=4)
button_full_on_idle = Button(button_col=0, button_row=5)
button_full_on_hover = Button(button_col=1, button_row=5)
button_skip_intro_idle = Button(button_col=0, button_row=6)
button_skip_intro_hover = Button(button_col=1, button_row=6)
button_back_game_idle = Button(button_col=0, button_row=7)
button_back_game_hover = Button(button_col=1, button_row=7)
button_back_menu_idle = Button(button_col=0, button_row=8)
button_back_menu_hover = Button(button_col=1, button_row=8)
button_exit_idle = Button(button_col=0, button_row=9)
button_exit_hover = Button(button_col=1, button_row=9)
button_settings_idle = Button(button_col=0, button_row=10)
button_settings_hover = Button(button_col=1, button_row=10)
button_play_idle = Button(button_col=0, button_row=11)
button_play_hover = Button(button_col=1, button_row=11)
