"""
bullet.py

Place for Bullet class
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data
import assets

from math import fabs

# --- Constants ---
settings = data.load_settings()


# How far the bullet travels before disappearing
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
BULLET_MAX_DISTANCE = SCREEN_WIDTH * 0.75


class Bullet(arcade.Sprite):
    """ Bullet """

    def __init__(self, player_sprite):
        super().__init__()
        self.distance = 0
        self.center_x = player_sprite.center_x
        self.center_y = player_sprite.center_y
        self.change_x = max(12, abs(player_sprite.change_x) + 10)
        if player_sprite.face_right:
            self.texture = assets.bullet_textures[0]
        else:
            self.texture = assets.bullet_textures[1]
            self.change_x *= -1

    def update(self):
        """ Move the particle, and fade out """
        # Move
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.distance += fabs(self.change_x)
        if self.distance > BULLET_MAX_DISTANCE:
            self.remove_from_sprite_lists()