"""
player.py

Place for Player class.
"""

import arcade

# Control the physics of how the player moves
MAX_HORIZONTAL_MOVEMENT_SPEED = 10
MAX_VERTICAL_MOVEMENT_SPEED = 5
HORIZONTAL_ACCELERATION = 0.5
VERTICAL_ACCELERATION = 0.2
MOVEMENT_DRAG = 0.08
# Size of the playing field
PLAYING_FIELD_WIDTH = 5000
PLAYING_FIELD_HEIGHT = 1000


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
        elif self.right > PLAYING_FIELD_WIDTH - 1:
            self.right = PLAYING_FIELD_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > PLAYING_FIELD_HEIGHT - 1:
            self.top = PLAYING_FIELD_HEIGHT - 1