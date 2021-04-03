"""
finalcutscene.py

Place for CampaignView class.
"""

import arcade
import assets
import data
import math
import random
import game
from developer import log

class FinalCutScene(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.current_view_name = 'finalcutscene'
        self.angle = 0
        self.tic = 0

    def on_show_view(self):
        self.window.cursor.change_state(state='off')
        self.window.music_manager.play_song('menu')
        assets.game_sfx['scumbag'].play()
        self.tic = 0
    
    def setup(self):
        self.tic = 0
        assets.game_sfx['scumbag'].play()
        
    def on_update(self, delta_time: float):
        self.tic += 1
        if self.tic == 120:
            assets.game_sfx['badda_boom'].play()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(100,400,241,194,assets.finalscene_textures[0])
        if self.tic > 120:
            arcade.draw_lrwh_rectangle_textured(500,200,500,500,assets.finalscene_textures[1])
        self.window.developer_tool.on_draw_finish()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.window.gameview.setup('level5')
        self.window.show_view(self.window.gameview)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.window.gameview.setup('level5')
        self.window.show_view(self.window.gameview)
