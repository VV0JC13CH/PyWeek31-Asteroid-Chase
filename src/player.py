"""
player.py

Place for Player class.
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

# Control the physics of how the player moves
MAX_HORIZONTAL_MOVEMENT_SPEED = int(param['PLAYER']['MAX_HORIZONTAL_MOVEMENT_SPEED'])
MAX_VERTICAL_MOVEMENT_SPEED = int(param['PLAYER']['MAX_VERTICAL_MOVEMENT_SPEED'])
HORIZONTAL_ACCELERATION = float(param['PLAYER']['HORIZONTAL_ACCELERATION'])
VERTICAL_ACCELERATION = float(param['PLAYER']['VERTICAL_ACCELERATION'])
MOVEMENT_DRAG = float(param['PLAYER']['MOVEMENT_DRAG'])
HEALTH = float(param['PLAYER']['HEALTH'])

SOUND_VOL = int(settings['AUDIO']['SOUND_VOL'])

class Player(arcade.Sprite):
    """ Player ship """
    def __init__(self, level_width, level_height, particle_sprite_list=[], space=None, x=0, y=0):
        """ Set up player """
        super().__init__()
        self.face_right = True
        self.level_width = level_width
        self.level_height = level_height
        self.particle_sprite_list = particle_sprite_list
        self.space = space
        
        radius = 40
        mass = 2.0
        self.health = HEALTH
        
        vs_body = [(-50,-25),(-50,0),(-20,25),(20,25),(50,0),(50,-25)]
        inertia = pymunk.moment_for_poly(mass, vs_body)
        self.body = pymunk.Body(mass, inertia)
        self.body.position = pymunk.Vec2d(x, y)
        self.body.velocity = pymunk.Vec2d(0, 0)
        self.shape = pymunk.Poly(self.body, vs_body)
        self.shape.elasticity = 0.5
        self.shape.friction = 0.9
        self.shape.collision_type = 1
        
        self.space = space
        if self.space is not None:
            self.space.add(self.body, self.shape)
        
        self.flash_ani = 0
        self.damage_to = 0
        
        self.controlled = False
        
        self.siren_ani = 0
        self.texture = assets.police_textures[0][0]
        self.scale = 1.0
    
    def accelerate_up(self):
        if self.health == 0:
            return
        """ Accelerate player up """
        self.controlled = True
        if self.body.velocity[1] < MAX_VERTICAL_MOVEMENT_SPEED:
            self.body.apply_impulse_at_world_point((0,VERTICAL_ACCELERATION),(self.center_x,self.center_y))

    def accelerate_down(self):
        if self.health == 0:
            return
        """ Accelerate player down """
        self.controlled = True
        if self.body.velocity[1] > -MAX_VERTICAL_MOVEMENT_SPEED:
            self.body.apply_impulse_at_world_point((0,-VERTICAL_ACCELERATION),(self.center_x,self.center_y))

    def accelerate_right(self):
        if self.health == 0:
            return
        """ Accelerate player right """
        self.controlled = True
        self.face_right = True
        if self.body.velocity[0] < MAX_HORIZONTAL_MOVEMENT_SPEED:
            self.body.apply_impulse_at_world_point((HORIZONTAL_ACCELERATION,0),(self.center_x,self.center_y))

    def accelerate_left(self):
        if self.health == 0:
            return
        """ Accelerate player left """
        self.controlled = True
        self.face_right = False
        if self.body.velocity[0] > -MAX_HORIZONTAL_MOVEMENT_SPEED:
            self.body.apply_impulse_at_world_point((-HORIZONTAL_ACCELERATION,0),(self.center_x,self.center_y))
    
    def playerasteroidcollision_func(self, arbiter, space, data):
        a,b = arbiter.shapes
        rel_vx = a.body.velocity[0]-b.body.velocity[0]
        rel_vy = a.body.velocity[1]-b.body.velocity[1]
        rel_velocity = math.sqrt(rel_vx*rel_vx+rel_vy*rel_vy)
        position = arbiter.contact_point_set.points[0].point_a
        hit = False
        if self.flash_ani <= 0 and rel_velocity > 150:
            assets.game_sfx['crashbig'].play(SOUND_VOL)
            self.hit(damage=1)
            hit = True
        elif self.flash_ani <= 0 and rel_velocity > 50: # sparks on contact with asteroid
            assets.game_sfx['crashsmall'][int(random.random()>0.5)].play(SOUND_VOL)
            self.hit(damage=0)
            hit = True
        if hit:
            for i in range(10):
                particle = Particle(4, 4, arcade.color.YELLOW)
                while particle.change_y == 0 and particle.change_x == 0:
                    particle.change_y = random.randrange(-2, 3)
                    particle.change_x = random.randrange(-2, 3)
                particle.center_x = position[0]
                particle.center_y = position[1]
                self.particle_sprite_list.append(particle)
    
    def hit(self, damage=1):
        if self.flash_ani > 0:
            return
        self.health -= damage
        self.flash_ani = 10
        if self.health == 0:
            pass # TODO: handle player death
            #self.space.remove(self.shape, self.body)
            #self.remove_from_sprite_lists()
    
    def update(self):
        
        # Drag
        drag = (-MOVEMENT_DRAG*self.body.velocity[0],-MOVEMENT_DRAG*self.body.velocity[1])
        self.body.apply_impulse_at_world_point(drag,(self.center_x,self.center_y))
        
        # Attitude control (PD controller, only runs while key input control applied)
        if self.controlled:
            #gain_ang = 500.0
            #gain_angdot = 100.0
            gain_ang = 100.0
            gain_angdot = 20.0
            #angle_diff = self.body.angle
            angle_diff = ((self.body.angle + math.pi) % (2*math.pi))-math.pi
            righting = gain_ang*angle_diff + gain_angdot*self.body.angular_velocity
            self.body.apply_impulse_at_world_point((0.0,righting),(self.center_x-10, self.center_y))
            self.body.apply_impulse_at_world_point((0.0,-righting),(self.center_x+10, self.center_y))
        
        # Update sprite/animations
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
        if self.flash_ani > 0:
            self.flash_ani -= 1
        
        # update textures
        self.siren_ani += 1
        if self.siren_ani > 10:
            self.siren_ani = 0
        if self.siren_ani < 5:
            siren_ani_fram = 0
        else:
            siren_ani_fram = 1
        if flash == 1:
            siren_ani_fram = 2 # flash from hit
        if self.face_right:
            heading_ind = 0
        else:
            heading_ind = 1
        self.texture = assets.police_textures[siren_ani_fram][heading_ind]
        
        # reset control tracking
        self.controlled = False
        
