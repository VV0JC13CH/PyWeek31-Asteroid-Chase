"""
assets.py

Let's gather all resources from gfx/sfx here, like sprites and sounds.
"""

import arcade

# we love Windows users:
from pathlib import Path


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


# Backgrounds
bg_menu = arcade.load_texture(path_to_string('gfx', 'bg_menu.png'))