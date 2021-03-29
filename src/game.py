"""
game.py

Place for GameView class.
"""

# --- Import external modules ---
import arcade
from arcade.gl import geometry
import random
# --- Import internal classes ---
import data
from pause import PauseView
from player import Player
from particle import Particle

# --- Constants ---
param = data.load_parameters()

# Size of the playing field
LEVEL_WIDTH = int(param['LEVEL']['WIDTH'])
LEVEL_HEIGHT = int(param['LEVEL']['HEIGHT'])

# --- Mini-map related ---
# Size of the minimap
MINIMAP_HEIGHT = int(param['MAP']['HEIGHT'])


# How far away from the edges do we get before scrolling?
TOP_VIEWPORT_MARGIN = int(param['VIEWPORT']['MARGIN_TOP'])
DEFAULT_BOTTOM_VIEWPORT = int(param['VIEWPORT']['DEFAULT_BOTTOM_VIEWPORT'])


class GameView(arcade.View):
    """ Main game view. """

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.star_sprite_list = None
        self.enemy_sprite_list = None
        self.bullet_sprite_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.view_bottom = 0
        self.view_left = 0

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        # --- Mini-map related ---
        # How big is our screen?
        screen_size = (self.window.width, self.window.height)
        # How big is the mini-map?
        mini_map_size = (self.window.width, MINIMAP_HEIGHT)
        # Where is the mini-map to be drawn?
        mini_map_pos = (self.window.width / 2, self.window.height - MINIMAP_HEIGHT / 2)
        # Load a vertex and fragment shader
        self.program = self.window.ctx.load_program(
            vertex_shader=arcade.resources.shaders.vertex.default_projection,
            fragment_shader=arcade.resources.shaders.fragment.texture)
        # Add a color attachment to store pixel colors
        self.mini_map_color_attachment = self.window.ctx.texture(screen_size)
        # Create a frame buffer with the needed color attachment
        self.mini_map_screen = self.window.ctx.framebuffer(color_attachments=[self.mini_map_color_attachment])
        # Create a rectangle that will hold where the mini-map goes
        self.mini_map_rect = geometry.screen_rectangle(0, self.window.width, MINIMAP_HEIGHT, self.window.height)

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()
        self.enemy_sprite_list = arcade.SpriteList()
        self.bullet_sprite_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)

        # Add stars
        for i in range(100):
            sprite = arcade.SpriteSolidColor(4, 4, arcade.color.WHITE)
            sprite.center_x = random.randrange(LEVEL_WIDTH)
            sprite.center_y = random.randrange(LEVEL_HEIGHT)
            self.star_sprite_list.append(sprite)

        # Add enemies
        for i in range(30):
            sprite = arcade.SpriteSolidColor(20, 20, arcade.csscolor.LIGHT_SALMON)
            sprite.center_x = random.randrange(LEVEL_WIDTH)
            sprite.center_y = random.randrange(LEVEL_HEIGHT)
            self.enemy_sprite_list.append(sprite)

    def on_draw(self):
        """ Render the screen. """
        self.window.developer_tool.on_draw_start()
        # This command has to happen before we start drawing
        arcade.start_render()

        # --- Mini-map related ---

        # Draw to the frame buffer used in the mini-map
        self.mini_map_screen.use()
        self.mini_map_screen.clear()

        arcade.set_viewport(0,
                            LEVEL_WIDTH,
                            0,
                            LEVEL_HEIGHT)

        self.enemy_sprite_list.draw()
        self.player_list.draw()

        # Now draw to the actual screen
        self.window.use()

        arcade.set_viewport(self.view_left,
                            self.window.width + self.view_left,
                            self.view_bottom,
                            self.window.height + self.view_bottom)

        self.star_sprite_list.draw()
        self.enemy_sprite_list.draw()
        self.bullet_sprite_list.draw()
        self.player_list.draw()

        # Draw the ground
        arcade.draw_line(0, 0, LEVEL_WIDTH, 0, arcade.color.WHITE)

        # Draw a background for the minimap
        arcade.draw_rectangle_filled(self.window.width - self.window.width / 2 + self.view_left,
                                     self.window.height - MINIMAP_HEIGHT + MINIMAP_HEIGHT / 2 + self.view_bottom,
                                     self.window.width,
                                     MINIMAP_HEIGHT,
                                     arcade.color.DARK_GREEN)

        # --- Mini-map related ---

        # Draw the minimap
        self.mini_map_color_attachment.use(0)
        self.mini_map_rect.render(self.program)

        # Draw a rectangle showing where the screen is
        width_ratio = self.window.width / LEVEL_WIDTH
        height_ratio = MINIMAP_HEIGHT / LEVEL_HEIGHT
        width = width_ratio * self.window.width
        main_height = self.window.height - MINIMAP_HEIGHT
        height = height_ratio * main_height

        x = (self.view_left + self.window.width / 2) * width_ratio + self.view_left
        y = (self.window.height - MINIMAP_HEIGHT) + self.view_bottom + height / 2 + (main_height / LEVEL_HEIGHT) * self.view_bottom

        arcade.draw_rectangle_outline(center_x=x, center_y=y,
                                      width=width, height=height,
                                      color=arcade.color.WHITE)
        self.window.developer_tool.on_draw_finish()

    def on_update(self, delta_time):
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

        for bullet in self.bullet_sprite_list:
            enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_sprite_list)
            for enemy in enemy_hit_list:
                enemy.remove_from_sprite_lists()
                for i in range(10):
                    particle = Particle(4, 4, arcade.color.RED)
                    while particle.change_y == 0 and particle.change_x == 0:
                        particle.change_y = random.randrange(-2, 3)
                        particle.change_x = random.randrange(-2, 3)
                        particle.center_x = enemy.center_x
                        particle.center_y = enemy.center_y
                        self.bullet_sprite_list.append(particle)

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

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
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
            bullet = arcade.SpriteSolidColor(35, 3, arcade.color.WHITE)
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y
            bullet.change_x = max(12, abs(self.player_sprite.change_x) + 10)

            if not self.player_sprite.face_right:
                bullet.change_x *= -1

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
