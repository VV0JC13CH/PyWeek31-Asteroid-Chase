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
import data
import minimap
from pause import PauseView
from player import Player
from particle import Particle
from bullet import Bullet, Explosion
from scroll_background import ScrollBackground
from asteroid import Asteroid
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

MUSIC_VOL = int(settings['AUDIO']['MUSIC_VOL'])

# Collision Types (for pymunk)
COLLTYPE_POLICECAR = 1
COLLTYPE_ASTEROID = 2

class GameView(arcade.View):
    """ Main game view. """

    def __init__(self, level_width, level_height):
        """ Initializer """

        # Call the parent class initializer
        super().__init__()
        # Set up level
        self.level_width = level_width
        self.level_height = level_height
        # It has to be here in order to create pause view ASAP:
        self.window.pause_view = PauseView(self)

        # pymunk
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, 0.0)
        self.static_lines = []
        
        # Create pymunk walls around level
        #walls = [[0, 80, 700, 80],[0, 600, 700, 600],[0, 80, 0, 600],[700, 80, 700, 600]]
        walls = [[0, 0, level_width, 0],[0, level_height, level_width, level_height],[0, 0, 0, level_height],[level_width, 0, level_width, level_height]]
        for wall in walls:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, [wall[0], wall[1]], [wall[2], wall[3]], 0.0)
            shape.elasticity = 0.99
            shape.friction = 10
            self.space.add(shape, body)
            self.static_lines.append(shape)
        
        # Variables that will hold sprite lists
        self.player_list = None
        self.star_sprite_list = None
        self.asteroid_sprite_list = None
        self.bullet_sprite_list = None
        self.particle_sprite_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.view_bottom = 5
        self.view_left = 0

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()
        self.asteroid_sprite_list = arcade.SpriteList()
        self.bullet_sprite_list = arcade.SpriteList()
        self.particle_sprite_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(self.level_width, self.level_height, self, self.space, 400, 400)
        self.player_list.append(self.player_sprite)

        # Add stars
        for i in range(100):
            sprite = arcade.SpriteSolidColor(4, 4, arcade.color.WHITE)
            sprite.center_x = random.randrange(self.level_width)
            sprite.center_y = random.randrange(self.level_height)
            self.star_sprite_list.append(sprite)
            
        # Add Asteroids
        for i in range(100):
            x = random.randrange(self.level_width)
            y = random.randrange(self.level_height)
            vx = random.randrange(100)-50
            vy = random.randrange(100)-50
            sprite = Asteroid(self,self.space,x,y,vx,vy,type=['small','large'][int(random.random()>0.5)])
            self.asteroid_sprite_list.append(sprite)
        
        # scrolling background images
        self.background_list = ScrollBackground(self.window)
        
        # pymunk collision handlers
        self.collision_handlers = []
        self.collision_handlers.append(self.space.add_collision_handler(COLLTYPE_POLICECAR, COLLTYPE_ASTEROID))
        self.collision_handlers[-1].post_solve=self.player_sprite.playerasteroidcollision_func
        
        # test out some music
        self.music = arcade.Sound(assets.music_path['space_chase'], streaming=True)
        self.current_player = self.music.play(MUSIC_VOL,loop=True)

    def on_show_view(self):
        self.window.cursor.change_state(state='off')

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
        self.asteroid_sprite_list.draw()
        self.bullet_sprite_list.draw()
        self.particle_sprite_list.draw()
        self.player_list.draw()
        
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
        
        # Update scrolling background
        self.background_list.update_scroll(self.view_left, self.view_bottom)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            self.reset_viewport()
            log('Scene switched to ' + str(self.window.pause_view))
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
            # Shoot out a bullet/laser
            bullet = Bullet(self.player_sprite)
            self.bullet_sprite_list.append(bullet)

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
