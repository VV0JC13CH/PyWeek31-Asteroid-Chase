"""
badguys.py

Place for BadGuys class.
"""

# --- Import external modules ---
import arcade
import pymunk
# --- Import internal classes ---
import data
import assets

import math
import random

from particle import Particle

# --- Constants ---
param = data.load_parameters()
settings = data.load_settings()

# Control the physics of how the bad guy moves
MAX_VERTICAL_MOVEMENT_SPEED = int(param['BADGUY1']['MAX_VERTICAL_MOVEMENT_SPEED'])

SOUND_VOL = int(settings['AUDIO']['SOUND_VOL'])

class BadGuy(arcade.Sprite):
    """ Bad Guy """
    def __init__(self, parent, level_width, level_height, x=0, y=0, type=0):
        """ Set up player """
        super().__init__()
        
        self.parent = parent
        self.face_right = True
        self.level_width = level_width
        self.level_height = level_height
        self.type = type
        
        self.center_x = x
        self.center_y = y
        self.angle = 0.0
        self.track_y = y
        
        self.flash_ani = 0
        self.damage_to = 0
        
        self.controlled = False
        
        self.frame_ani = 0
        self.texture = assets.bad_guys[self.type][0][0]
        self.scale = 1.0
        
        if type in [0,1]:
            self.maxhealth = int(param['BADGUY1']['HEALTH'])
        else:
            self.maxhealth = int(param['BADGUY1']['HEALTH'])
        self.health = self.maxhealth
    
    def hit(self, damage=1):
        self.track_y += 400*random.random()-200 # dodge vertically
        if self.flash_ani > 0:
            return
        if self.health <= 0:
            return
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.flash_ani = 10
        if self.health == 0:
            pass # TODO: handle bad guys shields down
    
    def update(self):
        
        # Update position
        if self.health == 0: # floating
            self.change_x -= 0.05
            if self.change_x < 0:
                self.change_x = 0
            self.angle += 1
            self.change_y = 0.0
        else: # still driving
            dist2p = self.center_x-self.parent.player_sprite.center_x
            if dist2p > 1200:
                vel_x = 50
            elif dist2p > 700:
                vel_x = 300
            elif dist2p > 400:
                vel_x = 400
            else:
                vel_x = 400+(400-dist2p)
        
            self.change_x = vel_x/60.0
            
            # track y position
            if math.fabs(self.track_y-self.center_y) < (MAX_VERTICAL_MOVEMENT_SPEED/60):
                self.change_y = 0.0
            else:
                self.change_y = (MAX_VERTICAL_MOVEMENT_SPEED/60)*(self.track_y-self.center_y)/math.fabs(self.track_y-self.center_y)
        
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        if self.change_x >= 0:
            self.face_right = True
        else:
            self.face_right = False
        
        # breakdown sparks
        if self.health == 0 and self.frame_ani == 0:
            for i in range(5):
                particle = Particle(4, 4, arcade.color.ORANGE)
                while particle.change_y == 0 and particle.change_x == 0:
                    particle.change_y = random.randrange(-2, 3)
                    particle.change_x = random.randrange(-2, 3)
                particle.center_x = self.center_x
                particle.center_y = self.center_y
                self.parent.particle_sprite_list.append(particle)
        
        # Update sprite/animations
        if self.flash_ani > 8:
            flash = 1
        elif self.flash_ani > 4:
            flash = 0
        elif self.flash_ani > 0:
            flash = 1
        else:
            flash = 0
        if self.flash_ani > 0:
            self.flash_ani -= 1
        
        # update textures
        self.frame_ani += 1
        if self.health == 0:
            repeat = 10
        else:
            repeat = 10
        if self.frame_ani > repeat:
            self.frame_ani = 0
        if self.frame_ani < (repeat/2) or self.health == 0:
            ani_fram = 0
        else:
            ani_fram = 1
        if flash == 1:
            ani_fram = 2 # flash from hit
        if self.face_right:
            heading_ind = 0
        else:
            heading_ind = 1
        self.texture = assets.bad_guys[self.type][ani_fram][heading_ind]
        
    def postdraw(self):
        if self.health > 0:
            meter_x = 100*(self.health/self.maxhealth)
            arcade.draw_text("Shield", self.center_x-40, self.center_y+80, arcade.color.WHITE, 18)
            arcade.draw_rectangle_filled(center_x=self.center_x-(50-meter_x/2), center_y=self.center_y+75,
                                      width=meter_x, height=10,
                                      color=arcade.color.ORANGE)
            arcade.draw_rectangle_outline(center_x=self.center_x, center_y=self.center_y+75,
                                      width=100, height=10,
                                      color=arcade.color.WHITE)
        else:
            arcade.draw_text("Disabled", self.center_x-50, self.center_y+75, arcade.color.WHITE, 18)

