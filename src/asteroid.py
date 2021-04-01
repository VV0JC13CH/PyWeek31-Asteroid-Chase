"""
asteroid.py

Place for Asteroid class
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
settings = data.load_settings()
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])

SOUND_VOL = int(settings['AUDIO']['SOUND_VOL'])

# AsteroidManager: dynamically creates/deletes asteroids based on current player position
class AsteroidManager(object):
    def __init__(self):
        pass

class Asteroid(arcade.Sprite):
    """ Asteroid """

    def __init__(self, parent, space, x, y, vx, vy, type='small'):
        super().__init__()
        
        self.parent = parent
        self.center_x = x
        self.center_y = y
        self.type = type
        if self.type in ['small','broken_sat']:
            self.texture = assets.asteroid_textures[self.type][0]
            radius = 25
            mass = 1.0
            self.health = 3
        else:
            self.texture = assets.asteroid_textures['large'][0]
            radius = 50
            mass = 5.0
            self.health = 5
                
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = pymunk.Vec2d(x, y)
        self.body.velocity = pymunk.Vec2d(vx, vy)
        self.shape = shape = pymunk.Circle(self.body, radius, pymunk.Vec2d(0, 0))
        self.shape.elasticity = 0.99
        self.shape.friction = 0.9
        self.shape.collision_type = 2
        
        self.space = space
        self.space.add(self.body, self.shape)
        
        self.flash_ani = 0
        self.damage_to = 0
    
    def hit(self, bullet):
        if self.flash_ani > 0:
            return
        self.health -= 1
        self.flash_ani = 10
        
        if bullet.change_x > 0:
            self.body.apply_impulse_at_world_point((100,0),(bullet.center_x,bullet.center_y))
        else:
            self.body.apply_impulse_at_world_point((-100,0),(bullet.center_x,bullet.center_y))
        
        if self.health == 0:
            self.space.remove(self.shape, self.body)
            self.remove_from_sprite_lists()
            if self.type == 'large':
                assets.game_sfx['asteroid_break_big'].play()
                for i in range(3):
                    vx = random.randrange(-50, 50)
                    vy = random.randrange(-50, 50)
                    x = self.center_x+random.randrange(-10, 10)
                    y = self.center_y+random.randrange(-10, 10)
                    sprite = Asteroid(self.parent,self.space,x,y,vx,vy,type='small')
                    self.parent.asteroid_sprite_list.append(sprite)
            else:
                assets.game_sfx['asteroid_break_small'].play()
            for i in range(10):
                particle = Particle(4, 4, arcade.color.GRAY)
                while particle.change_y == 0 and particle.change_x == 0:
                    particle.change_y = random.randrange(-2, 3)
                    particle.change_x = random.randrange(-2, 3)
                particle.center_x = self.center_x
                particle.center_y = self.center_y
                self.parent.particle_sprite_list.append(particle)
    
    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.angle = math.degrees(self.shape.body.angle)
        if self.flash_ani > 8:
            flash = 1
        elif self.flash_ani > 4:
            flash = 0
        elif self.flash_ani > 0:
            flash = 1
        else:
            flash = 0
        self.texture = assets.asteroid_textures[self.type][flash]
        if self.flash_ani > 0:
            self.flash_ani -= 1


