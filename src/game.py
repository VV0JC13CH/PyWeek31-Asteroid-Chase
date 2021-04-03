"""
game.py

Place for GameView class.
"""

# --- Import external modules ---
import arcade
import pymunk
from arcade.gl import geometry
import random
# --- Import internal classes ---
from developer import log
import pause
import data
import minimap
from player import Player
from particle import Particle
from bullet import Bullet, Explosion
from scroll_background import ScrollBackground
from structures import Structure
from asteroid import Asteroid, AsteroidManager
from badguys import BadGuy, FloatingBomb, WallofDeath
import campaign
import assets


# --- Constants ---
param = data.load_parameters()
settings = data.load_settings()

# --- Mini-map related ---
# Size of the minimap
MINIMAP_HEIGHT = int(param['MAP']['HEIGHT'])

# How far away from the edges do we get before scrolling?
TOP_VIEWPORT_MARGIN = int(param['VIEWPORT']['MARGIN_TOP'])
DEFAULT_BOTTOM_VIEWPORT = int(param['VIEWPORT']['DEFAULT_BOTTOM_VIEWPORT'])


# Collision Types (for pymunk)
COLLTYPE_POLICECAR = 1
COLLTYPE_ASTEROID = 2
COLLTYPE_STRUCTURE = 3
COLLTYPE_BOMB = 3


class GameView(arcade.View):
    """ Main game view. """

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__()
        self.window.current_view_name = 'game_view'
        
        # Variables that will hold sprite lists
        self.player_list = None
        self.star_sprite_list = None
        self.asteroid_sprite_list = None
        self.bullet_sprite_list = None
        self.particle_sprite_list = None
        self.structures_sprite_list = None
        self.badguys_sprite_list = None
        self.bomb_sprite_list = None

        self.left_pressed = None
        self.right_pressed = None
        self.up_pressed = None
        self.down_pressed = None
        self.lshift_pressed = None
        self.space_pressed = None
        self.enter_pressed = False
        
        # Set up the player info
        self.player_sprite = None
        self.basic_laser_in_use = False
    
    def setup(self, level, restart=False):
        
        self.current_level = level
        self.outcome = None
        self.hurry_msg = False
        self.hurry_msg_to = 0
        self.level_to = 180
        
        if not restart:
            if not self.window.music_manager.common_name_of_song == assets.leveldata[level].music:
                self.window.music_manager.play_song(assets.leveldata[level].music)
        
        # Set up level
        self.level_width = assets.leveldata[level].size[0]
        self.level_height = assets.leveldata[level].size[1]

        # pymunk
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, 0.0)
        self.static_lines = []
        
        # Create pymunk walls around level
        walls = [[0, 0, self.level_width, 0],[0, self.level_height, self.level_width, self.level_height],[0, 0, 0, self.level_height],[self.level_width, 0, self.level_width, self.level_height]]
        for wall in walls:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, (wall[0], wall[1]), (wall[2], wall[3]), 0.0)
            shape.elasticity = 0.99
            shape.friction = 10
            self.space.add(shape, body)
            self.static_lines.append(shape)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.lshift_pressed = False
        self.space_pressed = False
        self.enter_pressed = False

        self.view_bottom = 0
        self.view_left = 0

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()
        self.asteroid_sprite_list = arcade.SpriteList()
        self.bullet_sprite_list = arcade.SpriteList()
        self.particle_sprite_list = arcade.SpriteList()
        self.structures_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.badguys_sprite_list = arcade.SpriteList()
        self.bomb_sprite_list = arcade.SpriteList()

        # Set up the player
        startx = assets.leveldata[level].player_start[0]
        starty = assets.leveldata[level].player_start[1]
        self.player_sprite = Player(self.level_width, self.level_height, self.particle_sprite_list, self.space, startx, starty)
        self.player_list.append(self.player_sprite)

        # Weapons
        self.basic_laser_in_use = False
        
        # Add static structures
        structures = [] # TODO: fill this with static_structures taken from assets
        for id in assets.leveldata[level].static_structures:
            structures.append(assets.static_structure[id])
        for i in range(len(structures)):
            structure = structures[i]
            structure_sprite = Structure(self, self.space, structure.verts, "str_%d"%(i), type=structure.type)
            self.structures_sprite_list.append(structure_sprite)
        
        # Initialise Asteroid Manager
        self.asteroid_manager = AsteroidManager(self, density=assets.leveldata[level].asteroid_density)
        self.asteroid_manager.Update() # initial asteroid population
        
        """
        # Add in some bombs for testing
        sprite = FloatingBomb(self,self.space,1000,300,0,0)
        self.bomb_sprite_list.append(sprite)
        sprite = FloatingBomb(self,self.space,1500,400,0,0)
        self.bomb_sprite_list.append(sprite)
        """
        
        # Add Badguys
        for id in assets.leveldata[level].badguy_ids:
            x = assets.bad_guydata[id].start_pos[0]
            y = assets.bad_guydata[id].start_pos[1]
            type = assets.bad_guydata[id].type
            action_data = assets.bad_guydata[id].action_data
            bg_sprite = BadGuy(self, self.level_width, self.level_height, x=x, y=y, type=type, action_data=action_data)
            self.badguys_sprite_list.append(bg_sprite)
        
        if self.current_level == 'level5': #wall of death
            self.wallofdeath = WallofDeath(self, self.level_width, self.level_height)
        
        # scrolling background images
        self.background_list = ScrollBackground(self.window)
        
        # pymunk collision handlers
        self.collision_handlers = []
        self.collision_handlers.append(self.space.add_collision_handler(COLLTYPE_POLICECAR, COLLTYPE_ASTEROID))
        self.collision_handlers[-1].post_solve=self.player_sprite.playerasteroidcollision_func
        self.collision_handlers.append(self.space.add_collision_handler(COLLTYPE_POLICECAR, COLLTYPE_STRUCTURE))
        self.collision_handlers[-1].post_solve=self.player_sprite.playerasteroidcollision_func

    def on_show_view(self):
        self.window.cursor.change_state(state='off')
        self.window.current_view_name = 'game_view'

    def reset_viewport(self):
        """In order to fix views after quit from gameView"""
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Render the screen. """
        self.window.developer_tool.on_draw_start()
        # This command has to happen before we start drawing
        arcade.start_render()

        arcade.set_viewport(self.view_left,
                            self.window.width + self.view_left,
                            self.view_bottom,
                            self.window.height + self.view_bottom)
        
        self.background_list.draw()
        self.star_sprite_list.draw()
        self.structures_sprite_list.draw()
        self.asteroid_sprite_list.draw()
        self.badguys_sprite_list.draw()
        for badguy in self.badguys_sprite_list:
            badguy.postdraw2()
        self.bomb_sprite_list.draw()
        self.bullet_sprite_list.draw()
        self.particle_sprite_list.draw()
        self.player_list.draw()

        for badguy in self.badguys_sprite_list:
            badguy.postdraw()
        
        if self.current_level == 'level5':
            self.wallofdeath.draw()
        
        """
        # Draw walls (testing)
        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcade.color.WHITE, 2)
        """
        
        minimap.draw_minimap(self, MINIMAP_HEIGHT, self.level_width, self.level_height)

        self.window.developer_tool.on_draw_finish()

    def on_update(self, delta_time):
        
        # Update pymunk physics
        self.space.step(1 / 60.0)
        
        """ Movement and game logic """
        # Calculate speed based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.accelerate_up()
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.accelerate_down()

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.accelerate_left()
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.accelerate_right()

        # Call update to move the sprite
        self.player_list.update()
        self.bullet_sprite_list.update()
        self.asteroid_sprite_list.update()
        self.particle_sprite_list.update()
        self.badguys_sprite_list.update()
        if self.current_level == 'level5':
            self.wallofdeath.update()
        self.bomb_sprite_list.update()
        
        # check for asteroid updates needed
        self.asteroid_manager.Update()
        
        for bullet in self.bullet_sprite_list:
            if bullet.death_to < 20: # bullet currently acting as explosion
                continue
            badguys_hit_list = arcade.check_for_collision_with_list(bullet, self.badguys_sprite_list)
            if len(badguys_hit_list) > 0:
                explosion = Explosion(bullet)
                self.bullet_sprite_list.append(explosion)
                bullet.remove_from_sprite_lists()
            for badguy in badguys_hit_list:
                badguy.hit(damage=1)
        for bullet in self.bullet_sprite_list:
            if bullet.death_to < 20: # bullet currently acting as explosion
                continue
            asteroid_hit_list = arcade.check_for_collision_with_list(bullet, self.asteroid_sprite_list)
            if len(asteroid_hit_list) > 0:
                explosion = Explosion(bullet)
                self.bullet_sprite_list.append(explosion)
                bullet.remove_from_sprite_lists()
            for asteroid in asteroid_hit_list:
                asteroid.hit(bullet)
        for bullet in self.bullet_sprite_list:
            if bullet.death_to < 20: # bullet currently acting as explosion
                continue
            structures_hit_list = arcade.check_for_collision_with_list(bullet, self.structures_sprite_list)
            if len(structures_hit_list) > 0:
                explosion = Explosion(bullet)
                self.bullet_sprite_list.append(explosion)
                bullet.remove_from_sprite_lists()
        
        # Scroll left
        left_boundary = self.view_left + (self.window.width / 2 - 50)
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left

        # Scroll right
        right_boundary = self.view_left + self.window.width - (self.window.width / 2 - 50)
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary

        # Scroll up
        self.view_bottom = DEFAULT_BOTTOM_VIEWPORT
        top_boundary = self.view_bottom + self.window.height - TOP_VIEWPORT_MARGIN - MINIMAP_HEIGHT
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # Shoot out a bullet/laser
        if self.player_sprite.health > 0:
            if self.space_pressed and self.lshift_pressed and not self.basic_laser_in_use:
                if len(self.bullet_sprite_list) < 8 and not self.player_sprite.laser_disabled:
                    bullet = Bullet(self.player_sprite)
                    self.bullet_sprite_list.append(bullet)
                    self.player_sprite.overheat += 0.03

        # Update scrolling background
        self.background_list.update_scroll(self.view_left, self.view_bottom)

        # Check for level outcome
        if self.outcome == None:
            if self.player_sprite.health == 0:
                self.outcome = 'death'
            if any([bg.fraction > 0.8 for bg in self.badguys_sprite_list]) and not self.hurry_msg:
                self.hurry_msg = True
                self.hurry_msg_to = 90
                assets.game_sfx['getaway'].play()
            if any([bg.fraction > 1.0 for bg in self.badguys_sprite_list]):
                self.outcome = 'failure'
            if len(self.badguys_sprite_list) > 0:
                if all([(bg.health == 0) for bg in self.badguys_sprite_list]):
                    self.outcome = 'victory'
                    self.window.levels_unlocked = self.window.levels_unlocked + 1
            else:
                if self.player_sprite.center_x/self.level_width > 0.95:
                    self.outcome = 'victory'
                    assets.game_sfx['wallofdeath'].stop()
                    self.window.levels_unlocked = self.window.levels_unlocked + 1
        elif self.outcome == 'victory' and self.enter_pressed:
            """ Waiting for a player to press enter in order to go to campaign view"""
            self.reset_viewport()
            """ We are going to create campaign level from beginning"""
            self.window.campaign_view = campaign.CampaignView()
            self.window.scenes.append(self.window.campaign_view)
            log('Scene switched to ' + str(self.window.campaign_view))
            self.window.show_view(self.window.campaign_view)
        if not self.outcome == None:
            self.level_to -= 1
            if self.level_to == 0:
                if self.outcome in ['death','failure']:
                    self.window.gameview.setup(self.current_level,restart=True)
                    self.window.show_view(self.window.gameview)
                else:
                    pass
        
        if self.hurry_msg_to > 0:
            self.hurry_msg_to -= 1

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            self.reset_viewport()
            self.window.pause_view = pause.PauseView(self)
            log('Scene switched to ' + str(self.window.pause_view))
            self.window.current_view_name = 'pause_view_after_game'
            self.window.scenes.append(self.window.pause_view)
            self.window.show_view(self.window.pause_view)
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True
            if self.player_sprite.health > 0 and not self.player_sprite.laser_disabled:
                self.basic_laser_in_use = True
                bullet = Bullet(self.player_sprite)
                self.bullet_sprite_list.append(bullet)
                self.player_sprite.overheat += 0.05
                self.basic_laser_in_use = False
        elif key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.LSHIFT:
            self.lshift_pressed = True
        elif key == arcade.key.ENTER:
            self.enter_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.LSHIFT:
            self.lshift_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.ENTER:
            self.enter_pressed = False
