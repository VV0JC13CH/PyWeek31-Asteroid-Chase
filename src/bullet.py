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
import random

# --- Constants ---
settings = data.load_settings()


# How far the bullet travels before disappearing
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
BULLET_MAX_DISTANCE = SCREEN_WIDTH * 0.75

SOUND_VOL = int(settings['AUDIO']['SOUND_VOL'])

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
        self.death_to = 20
        assets.game_sfx['laser'][int(random.random()>0.5)].play(SOUND_VOL)
    
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.distance += fabs(self.change_x)
        if self.distance > BULLET_MAX_DISTANCE:
            self.remove_from_sprite_lists()

class Explosion(arcade.Sprite):
    """ Explosion """

    def __init__(self, bullet):
        super().__init__()
        if bullet.change_x < 0:
            self.center_x = bullet.center_x - 40
        else:
            self.center_x = bullet.center_x + 40
        self.center_y = bullet.center_y
        self.texture = assets.explode_textures[0]
        self.death_to = 18
    
    def update(self):
        if self.death_to >= 15:
            self.texture = assets.explode_textures[0]
        elif self.death_to >= 12:
            self.texture = assets.explode_textures[1]
        elif self.death_to >= 9:
            self.texture = assets.explode_textures[2]
        elif self.death_to >= 6:
            self.texture = assets.explode_textures[3]
        elif self.death_to >= 3:
            self.texture = assets.explode_textures[4]
        elif self.death_to >= 0:
            self.texture = assets.explode_textures[5]
        self.death_to -= 1
        if self.death_to == 0:
            self.remove_from_sprite_lists()
            
