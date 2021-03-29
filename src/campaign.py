"""
campaign.py

Place for CampaignView class.
"""

import arcade
import assets
import data
import pause
import math
from button import Button
from developer import log

# --- Constants ---
param = data.load_parameters()
RADIANS_PER_FRAME = float(param['CAMPAIGN']['RADIANS_PER_FRAME'])


class CampaignView(arcade.View):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.sweep_length = self.window.height * 0.4
        if self.window.pause_view is None:
            self.window.pause_view = pause.PauseView(self)

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

        # Draw the radar line
        arcade.draw_line(self.window.width // 2, self.window.height // 2, x, y, arcade.color.WHITE_SMOKE, 4)

        # Draw the outline of the radar
        arcade.draw_circle_outline(self.window.width // 2, self.window.height // 2, self.sweep_length,
                                   arcade.color.SILVER, 10)

        self.window.developer_tool.on_draw_finish()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            log('Scene switched to ' + str(self.window.pause_view))
            self.window.scenes.append(self.window.pause_view)
            self.window.show_view(self.window.pause_view)

