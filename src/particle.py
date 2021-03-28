"""
particle.py

Place for Particle class.
"""

import arcade


class Particle(arcade.SpriteSolidColor):
    """ Particle from explosion """
    def update(self):
        """ Move the particle, and fade out """
        # Move
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Fade
        self.alpha -= 5
        if self.alpha <= 0:
            self.remove_from_sprite_lists()