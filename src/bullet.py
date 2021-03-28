"""
bullet.py

Place for Bullet class
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data

# --- Constants ---
settings = data.load_settings()


# How far the bullet travels before disappearing
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
BULLET_MAX_DISTANCE = SCREEN_WIDTH * 0.75


class Bullet(arcade.SpriteSolidColor):
    """ Bullet """

    def __init__(self, width, height, color):
        super().__init__(width, height, color)
        self.distance = 0

    def update(self):
        """ Move the particle, and fade out """
        # Move
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.distance += self.change_x
        if self.distance > BULLET_MAX_DISTANCE:
            self.remove_from_sprite_lists()