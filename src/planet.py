"""
planet.py

Place for Planet class.
"""

import arcade
import assets
import timeit


class Planet(arcade.Sprite):
    def __init__(self, planet_id, center_x, center_y, speed=10, scale=1):
        super().__init__()
        self.planet_id = planet_id
        self.speed = speed
        self.asset = assets.planet_sprite_list[planet_id]
        self.current_frame = 0
        self.asset.texture = self.asset.textures[self.current_frame]
        self.center_x = center_x
        self.center_y = center_y
        self.asset.scale = scale
        self.list = arcade.SpriteList()
        self.time = timeit.default_timer()
        self.time_old = 0.0

    def on_draw(self):
        self.asset.center_x = self.center_x
        self.asset.center_y = self.center_y
        self.list.append(self.asset)
        self.list.draw()

    def update_rotation(self):
        self.time_old += self.time
        if (self.time_old - self.time)*0.0001 > self.speed:
            if self.current_frame < 34:
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.time_old = self.time
            self.asset.texture = self.asset.textures[self.current_frame]


