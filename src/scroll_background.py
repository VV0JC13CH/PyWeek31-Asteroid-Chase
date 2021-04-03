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
        """I go with a clock, center one"""
        self.sprite_list[0].texture = assets.background_texture_game
        self.sprite_list[0].center_x = self.width / 2
        self.sprite_list[0].center_y = self.height / 2
        self.sprite_list[0].change_x = 0
        self.sprite_list[0].width = self.width*3
        self.sprite_list[0].height = self.height*3

        self.append(arcade.Sprite())
        """ upper, center """
        self.sprite_list[1].texture = assets.background_texture_game
        self.sprite_list[1].center_x = self.width / 2
        self.sprite_list[1].center_y = self.height / 2 + self.height
        self.sprite_list[1].change_x = 0
        self.sprite_list[1].width = self.width*3
        self.sprite_list[1].height = self.height*3

        self.append(arcade.Sprite())
        """ upper, right"""
        self.sprite_list[2].texture = assets.background_texture_game
        self.sprite_list[2].center_x = self.width / 2 + self.width
        self.sprite_list[2].center_y = self.height / 2 + self.height
        self.sprite_list[2].change_x = 0
        self.sprite_list[2].width = self.width*3
        self.sprite_list[2].height = self.height*3
        
        self.append(arcade.Sprite())
        """ center, right """
        self.sprite_list[3].texture = assets.background_texture_game
        self.sprite_list[3].center_x = self.width / 2 + self.width
        self.sprite_list[3].center_y = self.height / 2
        self.sprite_list[3].change_x = 0
        self.sprite_list[3].width = self.width*3
        self.sprite_list[3].height = self.height*3

        self.append(arcade.Sprite())
        """ below, right """
        self.sprite_list[4].texture = assets.background_texture_game
        self.sprite_list[4].center_x = self.width / 2
        self.sprite_list[4].center_y = self.height / 2 - self.height
        self.sprite_list[4].change_x = 0
        self.sprite_list[4].width = self.width*3
        self.sprite_list[4].height = self.height*3

        self.append(arcade.Sprite())
        """ below, center """
        self.sprite_list[5].texture = assets.background_texture_game
        self.sprite_list[5].center_x = self.width / 2
        self.sprite_list[5].center_y = self.height / 2 - self.height
        self.sprite_list[5].change_x = 0
        self.sprite_list[5].width = self.width*3
        self.sprite_list[5].height = self.height*3

    def update_scroll(self,view_left,view_bottom):
        """ update sprites for current viewport """
        for sprite in self.sprite_list:
            if sprite.right <= view_left:
                sprite.center_x += 2*self.width
            if sprite.left >= (view_left+self.width/2):
                sprite.center_x -= 2*self.width
            if sprite.top <= view_bottom:
                sprite.center_y += 2*self.height
            if sprite.bottom >= (view_bottom+self.height):
                sprite.center_y -= 2*self.height
        self.update()
