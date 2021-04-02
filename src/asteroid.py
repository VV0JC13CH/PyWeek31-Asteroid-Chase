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
    
    def __init__(self, parent, density=50):
        self.parent = parent
        self.density = density
        self.space = self.parent.space
        self.sector_len = 1200
        #self.previous_sector = math.floor(self.parent.player_sprite.center_x/self.sector_len)
        self.previous_sector = -1
    
    def PopulateSector(self, sector):
        for i in range(self.density):
            x = sector*self.sector_len + random.randrange(self.sector_len)
            y = random.randrange(self.parent.level_height)
            vx = random.randrange(100)-50
            vy = random.randrange(100)-50
            type=['small','large'][int(random.random()>0.5)]
            if type == 'small' and random.random()>0.8:
                type = 'broken_sat'
            sprite = Asteroid(self.parent,self.space,x,y,vx,vy,type=type)
            self.parent.asteroid_sprite_list.append(sprite)
    
    def Update(self):
        
        current_sector = math.floor(self.parent.player_sprite.center_x/self.sector_len)
        if current_sector == self.previous_sector:
            return
        else:
            #print('moving: %d -> %d'%(self.previous_sector, current_sector))
            # remove asteroids outside of range
            c = 0
            for asteroid in self.parent.asteroid_sprite_list:
                prevsect_bound = (current_sector-1)*self.sector_len
                nextsect_bound = (current_sector+2)*self.sector_len
                if asteroid.center_x < prevsect_bound or asteroid.center_x > nextsect_bound:
                    self.space.remove(asteroid.shape, asteroid.body)
                    asteroid.remove_from_sprite_lists()
                    #print('x: ',asteroid.center_x)
                    c += 1
                else:
                    pass
                    #print('xkeep: ',asteroid.center_x)
            #print('removed: %d'%(c))
        
            # Populate asteroids in next sector
            if current_sector > self.previous_sector:
                approaching_sector = current_sector+1
            else:
                approaching_sector = current_sector-1
            n_sectors = math.floor(self.parent.level_width/self.sector_len)
            if approaching_sector >= 0 and approaching_sector < n_sectors: # inside level width
                self.PopulateSector(approaching_sector)
                #print('adding: %d'%(approaching_sector))
            
            if self.previous_sector == -1: # init level, so populate the current sector too
                self.PopulateSector(current_sector)
                #print('adding: %d'%(current_sector))
            
            # reset for next update
            self.previous_sector = current_sector
            #print('num: ',len(self.parent.asteroid_sprite_list))
            

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


