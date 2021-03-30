"""
scroll_background.py

Class that controls scrolling star field background
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data
import assets

# --- Constants ---
settings = data.load_settings()
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])

class ScrollBackground(arcade.SpriteList):
    """ ScrollBackground """

    def __init__(self, window):
        super().__init__()
        
        self.width = window.width
        self.height = window.height
        
        self.append(arcade.Sprite())
        self.sprite_list[0].texture = assets.background_texture
        self.sprite_list[0].center_x = self.width // 2
        self.sprite_list[0].center_y = self.height // 2
        self.sprite_list[0].change_x = 0
        
        self.append(arcade.Sprite())
        self.sprite_list[1].texture = assets.background_texture
        self.sprite_list[1].center_x = self.width // 2 + 1220
        self.sprite_list[1].center_y = self.height // 2
        self.sprite_list[1].change_x = 0
        
        self.append(arcade.Sprite())
        self.sprite_list[2].texture = assets.background_texture
        self.sprite_list[2].center_x = self.width // 2
        self.sprite_list[2].center_y = self.height // 2 + 820
        self.sprite_list[2].change_x = 0
        
        self.append(arcade.Sprite())
        self.sprite_list[3].texture = assets.background_texture
        self.sprite_list[3].center_x = self.width // 2 + 1220
        self.sprite_list[3].center_y = self.height // 2 + 820
        self.sprite_list[3].change_x = 0

    def update_scroll(self,view_left,view_bottom):
        """ update sprites for current viewport """
        
        for sprite in self.sprite_list:
            if sprite.right <= view_left:
                sprite.center_x += 2*1220
            if sprite.left >= (view_left+self.width):
                sprite.center_x -= 2*1220
            if sprite.top <= view_bottom:
                sprite.center_y += 2*820
            if sprite.bottom >= (view_bottom+self.height):
                sprite.center_y -= 2*820
        
        self.update()
        
