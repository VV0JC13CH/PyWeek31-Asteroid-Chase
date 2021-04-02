"""
campaign.py

Place for CampaignView class.
"""

import arcade
import assets
import data
import pause
import math
import random
import game
import planet
from developer import log
from pointer import Pointer

# --- Constants ---
param = data.load_parameters()
RADIANS_PER_FRAME = float(param['CAMPAIGN']['RADIANS_PER_FRAME'])


class CampaignView(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.current_view_name = 'campaign_view'
        self.angle = 0
        if self.window.levels_unlocked != 0:
            self.selected_level = self.window.levels_unlocked
        else:
            self.selected_level = 1
        self.sweep_length = self.window.height * 0.4
        self.mouse_position = (0, 0)
        self.player_speed = 0.005
        # Add stars
        self.star_sprite_list = arcade.SpriteList()
        # Setup levels coordinates:
        self.level_5 = (self.window.width // 2 * 0.4, self.window.height // 2 * 1.2)
        self.level_4 = (self.window.width // 2 * 1.1, self.window.height // 2 * 1.5)
        self.level_3 = (self.window.width // 2 * 1.2, self.window.height // 2 * 1.3)
        self.level_2 = (self.window.width // 2 * 0.8, self.window.height // 2 * 0.4)
        self.level_1 = (self.window.width // 2 * 0.8, self.window.height // 2 * 1.1)
        self.levels = [self.level_1, self.level_2, self.level_3, self.level_4, self.level_5]
        # Planets animated in time sprites:
        self.planet_8 = planet.Planet(planet_id=0, speed=50, center_x=self.window.width*0.9, center_y=self.window.height*0.7,
                                      scale=0.6)
        self.planet_7 = planet.Planet(planet_id=7, speed=40, center_x=self.window.width*0.8, center_y=self.window.height*0.3,
                                      scale=0.3)
        self.planet_6 = planet.Planet(planet_id=6, speed=40, center_x=self.window.width*0.3, center_y=self.window.height*0.2,
                                      scale=0.3)
        self.planet_5 = planet.Planet(planet_id=5, speed=40, center_x=self.level_5[0], center_y=self.level_5[1], scale=0.3)
        self.planet_4 = planet.Planet(planet_id=4, speed=35, center_x=self.level_4[0], center_y=self.level_4[1], scale=0.2)
        self.planet_3 = planet.Planet(planet_id=3, speed=30, center_x=self.level_3[0], center_y=self.level_3[1], scale=0.4)
        self.planet_2 = planet.Planet(planet_id=2, speed=25, center_x=self.level_2[0], center_y=self.level_2[1], scale=0.2)
        self.planet_1 = planet.Planet(planet_id=1, speed=35, center_x=self.level_1[0], center_y=self.level_1[1], scale=0.5)

        for i in range(100):
            sprite = arcade.SpriteSolidColor(2, 2, arcade.color.WHITE)
            sprite.center_x = random.randrange(self.window.width)
            sprite.center_y = random.randrange(self.window.height)
            self.star_sprite_list.append(sprite)

        # Variables that will hold sprite lists
        self.player_list = arcade.SpriteList()
        # Set up the player
        self.player_sprite = Pointer(level_width=self.window.width,
                                     level_height=self.window.height)
        if self.selected_level > 1:
            self.player_sprite.center_x = self.levels[self.selected_level-2][0]+self.player_sprite.width/2
            self.player_sprite.center_y = self.levels[self.selected_level-2][1]+self.player_sprite.height/2
            self.vector_x = self.levels[self.selected_level - 1][0] - self.levels[self.selected_level - 2][0]
            self.vector_y = self.levels[self.selected_level - 1][1] - self.levels[self.selected_level - 2][1]
            if self.vector_x < 0:
                self.player_sprite.face_right = False
        else:
            self.player_sprite.center_x = self.levels[self.selected_level - 1][0] + self.player_sprite.width / 2
            self.player_sprite.center_y = self.levels[self.selected_level - 1][1] + self.player_sprite.height / 2
            self.vector_x = 0
            self.vector_y = 0
        self.player_list.append(self.player_sprite)

    def on_show_view(self):
        self.window.cursor.change_state(state='idle')

    def on_update(self, delta_time: float):
        # Call update to move the sprite
        self.player_list.update()

        if self.selected_level > 1:
            if abs(self.levels[self.selected_level - 1][0] - self.player_sprite.center_x) > 5:
                if abs(self.levels[self.selected_level - 1][1] - self.player_sprite.center_y) > 5:
                    self.player_list.move(self.vector_x*self.player_speed, self.vector_y*self.player_speed)
        if arcade.check_for_collision_with_list(self.player_sprite, self.window.cursor):
            self.window.cursor.change_state(state='no')
        else:
            self.window.cursor.change_state(state='idle')

        self.planet_8.update_rotation(delta_time)
        self.planet_7.update_rotation(delta_time)
        self.planet_6.update_rotation(delta_time)
        self.planet_5.update_rotation(delta_time)
        self.planet_4.update_rotation(delta_time)
        self.planet_3.update_rotation(delta_time)
        self.planet_2.update_rotation(delta_time)
        self.planet_1.update_rotation(delta_time)

    def on_draw(self):
        """ Use this function to draw everything to the screen. """

        # Move the angle of the sweep.
        self.angle += RADIANS_PER_FRAME

        # Calculate the end point of our radar sweep. Using math.
        x = self.sweep_length * math.sin(self.angle) + (self.window.width // 2)
        y = self.sweep_length * math.cos(self.angle) + (self.window.height // 2)

        # Start the render. This must happen before any drawing
        # commands. We do NOT need an stop render command.
        self.window.developer_tool.on_draw_start()

        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.window.width, self.window.height,
                                            assets.bg_campaign)
        self.star_sprite_list.draw()
        # Representation of levels:
        # Level 5:
        if self.window.levels_unlocked >= 5:
            if self.selected_level >= 4:
                arcade.draw_line(self.level_5[0], self.level_5[1],
                                 self.level_4[0], self.level_4[1], arcade.color.ROMAN_SILVER,
                                 1)
            arcade.draw_circle_filled(self.level_5[0], self.level_5[1], 10,
                                      arcade.color.BROWN, 3)
        if self.window.levels_unlocked >= 4:
            # Level 4:
            if self.selected_level in range(2, 5):
                arcade.draw_line(self.level_4[0], self.level_4[1],
                                 self.level_3[0], self.level_3[1], arcade.color.ROMAN_SILVER,
                                 1)
            arcade.draw_circle_filled(self.level_4[0], self.level_4[1], 5,
                                      arcade.color.DARK_BYZANTIUM, 3)
            arcade.draw_circle_filled(self.level_4[0], self.level_4[1], 3,
                                      arcade.color.GREEN_YELLOW, 3)
        if self.window.levels_unlocked >= 3:
            # Level 3: Kingdom End
            if self.selected_level in range(1, 4):
                arcade.draw_line(self.level_3[0], self.level_3[1],
                                 self.level_2[0], self.level_2[1], arcade.color.ROMAN_SILVER,
                                 1)
            arcade.draw_circle_filled(self.level_3[0], self.level_3[1], 14,
                                      arcade.color.DARK_BYZANTIUM, 3)
            arcade.draw_circle_filled(self.level_3[0], self.level_3[1], 12,
                                      arcade.color.RED_DEVIL, 3)
        if self.window.levels_unlocked >= 2:
            # Level 2: Tartolyyn
            if self.selected_level in range(0, 3):
                arcade.draw_line(self.level_2[0], self.level_2[1],
                                 self.level_1[0], self.level_1[1], arcade.color.ROMAN_SILVER,
                                 1)
            arcade.draw_circle_filled(self.level_2[0], self.level_2[1], 8,
                                      arcade.color.DARK_BYZANTIUM, 3)
            arcade.draw_circle_filled(self.level_2[0], self.level_2[1], 5,
                                      arcade.color.BROWN_NOSE, 3)
        # Level 1: Imperial City (tutorial)
        arcade.draw_circle_filled(self.level_1[0], self.level_1[1], 20,
                                  arcade.color.SILVER_LAKE_BLUE, 3)

        # Draw the radar line
        arcade.draw_line(self.window.width // 2, self.window.height // 2, x, y, arcade.color.ROMAN_SILVER, 4)

        # Draw the outline of the radar
        arcade.draw_circle_outline(self.window.width // 2, self.window.height // 2, self.sweep_length,
                                   arcade.color.OLD_SILVER, 8)
        # Planets:
        self.planet_8.on_draw()
        self.planet_7.on_draw()
        self.planet_6.on_draw()
        self.planet_5.on_draw()
        self.planet_4.on_draw()
        self.planet_3.on_draw()
        self.planet_2.on_draw()
        self.planet_1.on_draw()

        self.player_list.draw()
        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if arcade.check_for_collision_with_list(self.player_sprite, self.window.cursor):
            self.window.gameview.setup('level1')
            self.window.show_view(self.window.gameview)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            self.window.pause_view = pause.PauseView(self)
            log('Scene switched to ' + str(self.window.pause_view))
            self.window.current_view_name = 'pause_view_after_campaign'
            self.window.scenes.append(self.window.pause_view)
            self.window.show_view(self.window.pause_view)
        if key == arcade.key.F5 and self.window.developer_mode:
            if self.window.levels_unlocked < 5:
                self.window.levels_unlocked += 1
            else:
                self.window.levels_unlocked = 1
            self.window.campaign_view = CampaignView()
            self.window.scenes.append(self.window.campaign_view)
            log('Scene switched to ' + str(self.window.campaign_view))
            self.window.show_view(self.window.campaign_view)

