"""
pointer.py
Place for Pointer class.
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data
import assets

# --- Constants ---
param = data.load_parameters()

# Control the physics of how the player moves
MAX_HORIZONTAL_MOVEMENT_SPEED = int(param['PLAYER']['MAX_HORIZONTAL_MOVEMENT_SPEED'])
MAX_VERTICAL_MOVEMENT_SPEED = int(param['PLAYER']['MAX_VERTICAL_MOVEMENT_SPEED'])
HORIZONTAL_ACCELERATION = float(param['PLAYER']['HORIZONTAL_ACCELERATION'])
VERTICAL_ACCELERATION = float(param['PLAYER']['VERTICAL_ACCELERATION'])
MOVEMENT_DRAG = float(param['PLAYER']['MOVEMENT_DRAG'])


class Pointer(arcade.Sprite):
    """ Player ship """

    def __init__(self, level_width, level_height):
        """ Set up player """
        super().__init__()
        self.face_right = True
        self.level_width = level_width
        self.level_height = level_height

        self.siren_ani = 0
        self.texture = assets.police_textures[0][0]
        self.scale = 1.0



    def update(self):
        """ Move the player """
        # Move
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Drag
        if self.change_x > 0:
            self.change_x -= MOVEMENT_DRAG
        if self.change_x < 0:
            self.change_x += MOVEMENT_DRAG
        if abs(self.change_x) < MOVEMENT_DRAG:
            self.change_x = 0

        if self.change_y > 0:
            self.change_y -= MOVEMENT_DRAG
        if self.change_y < 0:
            self.change_y += MOVEMENT_DRAG
        if abs(self.change_y) < MOVEMENT_DRAG:
            self.change_y = 0

        # Check bounds
        if self.left < 0:
            self.left = 0
        elif self.right > self.level_width - 1:
            self.right = self.level_width - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > self.level_height - 1:
            self.top = self.level_height - 1

        # update textures
        self.siren_ani += 1
        if self.siren_ani > 10:
            self.siren_ani = 0
        if self.siren_ani < 5:
            siren_ani_fram = 0
        else:
            siren_ani_fram = 1
        if self.face_right:
            heading_ind = 0
        else:
            heading_ind = 1
        self.texture = assets.police_textures[siren_ani_fram][heading_ind]