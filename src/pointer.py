"""
pointer.py
Place for Pointer class.
"""

# --- Import external modules ---
import arcade
import math
import random
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


class BadCampaignPointer(arcade.Sprite):
    """ Player ship """

    def __init__(self, level_width, level_height, type=0):
        """ Set up player """
        super().__init__()
        self.face_right = True
        self.level_width = level_width
        self.level_height = level_height
        self.type = type

        self.animation_frame = 0
        self.texture = assets.bad_guys[self.type][0][0]
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
        self.animation_frame += 1
        if self.animation_frame > 10:
            self.animation_frame = 0
        if self.animation_frame < 5:
            animation_frame_item = 0
        else:
            animation_frame_item = 1
        if self.face_right:
            heading_ind = 0
        else:
            heading_ind = 1
        self.texture = assets.bad_guys[self.type][animation_frame_item][heading_ind]


class BadPointer(arcade.Sprite):
    """ Bad Guy """

    def __init__(self, parent, level_width, level_height, x=0, y=0, type=0, action_data=[]):
        """ Set up player """
        super().__init__()

        self.parent = parent
        self.face_right = True
        self.level_width = level_width
        self.level_height = level_height
        self.type = type
        self.action_data = []
        for action in action_data:
            self.action_data.append([action[0], action[1], False])  # type, data, completed?

        self.center_x = x
        self.center_y = y
        self.angle = 0.0
        self.track_y = y

        self.flash_ani = 0
        self.damage_to = 0

        self.controlled = False

        self.frame_ani = 0
        self.texture = assets.bad_guys[self.type][0][0]
        self.scale = 1.0

        if type == 0:
            self.maxhealth = int(param['BADGUY1']['HEALTH'])
        elif type == 1:
            self.maxhealth = int(param['BADGUY2']['HEALTH'])
        else:
            self.maxhealth = int(param['BADGUY1']['HEALTH'])
        self.health = self.maxhealth

        self.fraction = 0.0
        self.boost_to = 0
        self.bomblaunch_to = 0

    def hit(self, damage=1):
        self.track_y += 400 * random.random() - 200  # dodge vertically
        if self.track_y < 30:
            self.track_y = 30
        elif self.track_y > (self.level_height - 30):
            self.track_y = (self.level_height - 30)
        if self.flash_ani > 0:
            return
        if self.health <= 0:
            return
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.flash_ani = 10
        if self.health == 0:
            assets.game_sfx['scumbag'].play()

    def update(self):

        # Update position
        if self.health == 0:  # floating
            self.change_x -= 0.05
            if self.change_x < 0:
                self.change_x = 0
            self.angle += 1
            self.change_y = 0.0
        else:  # still driving
            dist2p = self.center_x - self.parent.player.center_x
            if self.boost_to > 0:
                vel_x = 600
            elif dist2p > 1200:
                vel_x = 100
            elif dist2p > 700:
                vel_x = 300
            elif dist2p > 400:
                vel_x = 400
            else:
                vel_x = 400 + (400 - dist2p)

            self.change_x = vel_x / 60.0

            # track y position
            if math.fabs(self.track_y - self.center_y) < (MAX_VERTICAL_MOVEMENT_SPEED / 60):
                self.change_y = 0.0
            else:
                self.change_y = (MAX_VERTICAL_MOVEMENT_SPEED / 60) * (self.track_y - self.center_y) / math.fabs(
                    self.track_y - self.center_y)

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x >= 0:
            self.face_right = True
        else:
            self.face_right = False

        # Look for behaviours
        self.fraction = self.center_x / self.level_width
        for action in self.action_data:
            if action[2] == True:  # already completed this action
                continue
            if action[0] == 'boost':
                if self.fraction > action[1]:
                    self.boost_to = 300
                    action[2] = True
                    assets.game_sfx['boost'].play()
            elif action[0] == 'bomb':
                if self.fraction > action[1]:
                    self.bomblaunch_to = 60
                    action[2] = True
                    assets.game_sfx['hehheh'].play()
        if self.boost_to > 0:
            self.boost_to -= 1
        if self.bomblaunch_to > 0:
            self.bomblaunch_to -= 1
            if self.bomblaunch_to == 0:
                sprite = FloatingBomb(self.parent, self.parent.space, self.center_x, self.center_y, self.change_x / 10,
                                      20 * random.random() - 10)
                self.parent.bomb_sprite_list.append(sprite)
                assets.game_sfx['bomblaunch'].play()

        # breakdown sparks
        if self.health == 0 and self.frame_ani == 0:
            for i in range(5):
                particle = Particle(4, 4, arcade.color.ORANGE)
                while particle.change_y == 0 and particle.change_x == 0:
                    particle.change_y = random.randrange(-2, 3)
                    particle.change_x = random.randrange(-2, 3)
                particle.center_x = self.center_x
                particle.center_y = self.center_y
                self.parent.particle_sprite_list.append(particle)

        # Update sprite/animations
        if self.flash_ani > 8:
            flash = 1
        elif self.flash_ani > 4:
            flash = 0
        elif self.flash_ani > 0:
            flash = 1
        else:
            flash = 0
        if self.flash_ani > 0:
            self.flash_ani -= 1

        # update textures
        self.frame_ani += 1
        if self.health == 0:
            repeat = 10
        else:
            repeat = 10
        if self.frame_ani > repeat:
            self.frame_ani = 0
        if self.frame_ani < (repeat / 2) or self.health == 0:
            ani_fram = 0
        else:
            ani_fram = 1
        if flash == 1:
            ani_fram = 2  # flash from hit
        if self.face_right:
            heading_ind = 0
        else:
            heading_ind = 1
        self.texture = assets.bad_guys[self.type][ani_fram][heading_ind]

    def postdraw(self):
        if self.health > 0:
            meter_x = 100 * (self.health / self.maxhealth)
            arcade.draw_text("Shield", self.center_x - 40, self.center_y + 80, arcade.color.WHITE, 18)
            arcade.draw_rectangle_filled(center_x=self.center_x - (50 - meter_x / 2), center_y=self.center_y + 75,
                                         width=meter_x, height=10,
                                         color=arcade.color.ORANGE)
            arcade.draw_rectangle_outline(center_x=self.center_x, center_y=self.center_y + 75,
                                          width=100, height=10,
                                          color=arcade.color.WHITE)
            if self.boost_to > 0:
                arcade.draw_text("Boost!", self.center_x - 100, self.center_y, arcade.color.YELLOW, 18)
        else:
            arcade.draw_text("Disabled", self.center_x - 50, self.center_y + 75, arcade.color.WHITE, 18)