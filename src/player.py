"""
player.py

Place for Player class.
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data

# --- Constants ---
param = data.load_parameters()

# Control the physics of how the player moves
MAX_HORIZONTAL_MOVEMENT_SPEED = int(param['PLAYER']['MAX_HORIZONTAL_MOVEMENT_SPEED'])
MAX_VERTICAL_MOVEMENT_SPEED = int(param['PLAYER']['MAX_VERTICAL_MOVEMENT_SPEED'])
HORIZONTAL_ACCELERATION = float(param['PLAYER']['HORIZONTAL_ACCELERATION'])
VERTICAL_ACCELERATION = float(param['PLAYER']['VERTICAL_ACCELERATION'])
MOVEMENT_DRAG = float(param['PLAYER']['MOVEMENT_DRAG'])
# Size of the playing field
LEVEL_WIDTH = int(param['LEVEL']['WIDTH'])
LEVEL_HEIGHT = int(param['LEVEL']['HEIGHT'])


class Player(arcade.SpriteSolidColor):
    """ Player ship """
    def __init__(self):
        """ Set up player """
        super().__init__(40, 10, arcade.color.SLATE_GRAY)
        self.face_right = True

    def accelerate_up(self):
        """ Accelerate player up """
        self.change_y += VERTICAL_ACCELERATION
        if self.change_y > MAX_VERTICAL_MOVEMENT_SPEED:
            self.change_y = MAX_VERTICAL_MOVEMENT_SPEED

    def accelerate_down(self):
        """ Accelerate player down """
        self.change_y -= VERTICAL_ACCELERATION
        if self.change_y < -MAX_VERTICAL_MOVEMENT_SPEED:
            self.change_y = -MAX_VERTICAL_MOVEMENT_SPEED

    def accelerate_right(self):
        """ Accelerate player right """
        self.face_right = True
        self.change_x += HORIZONTAL_ACCELERATION
        if self.change_x > MAX_HORIZONTAL_MOVEMENT_SPEED:
            self.change_x = MAX_HORIZONTAL_MOVEMENT_SPEED

    def accelerate_left(self):
        """ Accelerate player left """
        self.face_right = False
        self.change_x -= HORIZONTAL_ACCELERATION
        if self.change_x < -MAX_HORIZONTAL_MOVEMENT_SPEED:
            self.change_x = -MAX_HORIZONTAL_MOVEMENT_SPEED

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
        elif self.right > LEVEL_WIDTH - 1:
            self.right = LEVEL_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > LEVEL_HEIGHT - 1:
            self.top = LEVEL_HEIGHT - 1