"""
assets.py

Let's gather all resources from gfx/sfx here, like sprites and sounds.
"""

import arcade
from button import SimpleButton

# we love Windows users:
from pathlib import Path


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


# Backgrounds
bg_menu = arcade.load_texture(path_to_string('gfx', 'bg_menu.png'))

# Buttons
buttons_sprites = path_to_string('gfx', 'buttons.png')


button_pause_idle = SimpleButton(button_col=0, button_row=0)
button_pause_hover = SimpleButton(button_col=1, button_row=0)
button_reset_idle = SimpleButton(button_col=0, button_row=1)
button_reset_hover = SimpleButton(button_col=1, button_row=1)
button_music_off_idle = SimpleButton(button_col=0, button_row=2)
button_music_off_hover = SimpleButton(button_col=1, button_row=2)
button_music_on_idle = SimpleButton(button_col=0, button_row=3)
button_music_on_hover = SimpleButton(button_col=1, button_row=3)
button_full_off_idle = SimpleButton(button_col=0, button_row=4)
button_full_off_hover = SimpleButton(button_col=1, button_row=4)
button_full_on_idle = SimpleButton(button_col=0, button_row=5)
button_full_on_hover = SimpleButton(button_col=1, button_row=5)
button_skip_intro_idle = SimpleButton(button_col=0, button_row=6)
button_skip_intro_hover = SimpleButton(button_col=1, button_row=6)
button_back_game_idle = SimpleButton(button_col=0, button_row=7)
button_back_game_hover = SimpleButton(button_col=1, button_row=7)
button_back_menu_idle = SimpleButton(button_col=0, button_row=8)
button_back_menu_hover = SimpleButton(button_col=1, button_row=8)
button_exit_idle = SimpleButton(button_col=0, button_row=9)
button_exit_hover = SimpleButton(button_col=1, button_row=9)
button_settings_idle = SimpleButton(button_col=0, button_row=10)
button_settings_hover = SimpleButton(button_col=1, button_row=10)
button_play_idle = SimpleButton(button_col=0, button_row=11)
button_play_hover = SimpleButton(button_col=1, button_row=11)
button_dev_on_idle = SimpleButton(button_col=0, button_row=12)
button_dev_on_hover = SimpleButton(button_col=1, button_row=12)
button_dev_off_idle = SimpleButton(button_col=0, button_row=13)
button_dev_off_hover = SimpleButton(button_col=1, button_row=13)

button_textures = {"pause": button_pause_idle,
                   "pause_hover": button_pause_hover,
                   "reset": button_reset_idle,
                   "reset_hover": button_reset_hover,
                   "music_off": button_music_off_idle,
                   "music_off_hover": button_music_off_hover,
                   "music_on": button_music_on_idle,
                   "music_on_hover": button_music_on_hover,
                   "full_off": button_full_off_idle,
                   "full_off_hover": button_full_off_hover,
                   "full_on": button_full_on_idle,
                   "full_on_hover": button_full_on_hover,
                   "skip_intro": button_skip_intro_idle,
                   "skip_intro_hover": button_skip_intro_hover,
                   "back_game": button_back_game_idle,
                   "back_game_hover": button_back_game_hover,
                   "back_menu": button_back_menu_idle,
                   "back_menu_hover": button_back_menu_hover,
                   "exit": button_exit_idle,
                   "exit_hover": button_exit_hover,
                   "settings": button_settings_idle,
                   "settings_hover": button_settings_hover,
                   "play": button_play_idle,
                   "play_hover": button_play_hover
                   }

# Cursor
cursor_hover = arcade.Sprite(filename=path_to_string('gfx', 'cursor_hover.png'))
cursor_idle = arcade.Sprite(filename=path_to_string('gfx', 'cursor_idle.png'))
cursor_no = arcade.Sprite(filename=path_to_string('gfx', 'cursor_no.png'))

