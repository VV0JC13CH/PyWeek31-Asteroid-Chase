"""
intro.py

Place for IntroView class.
"""

import arcade
import assets
import data
from game import GameView
import pointer
from button import Button
from developer import log

# --- Constants ---
param = data.load_parameters()

# Size of the first level (intro plays only before first level)
LEVEL_WIDTH = int(param['LEVEL']['DEFAULT_WIDTH'])
LEVEL_HEIGHT = int(param['LEVEL']['DEFAULT_HEIGHT'])


class IntroView(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.current_view_name = 'intro_view'
        self.button_skip = Button(x=self.window.width/2,
                                  y=self.window.height * 1 / 8,
                                  width=250, height=50,
                                  texture_idle='skip_intro',
                                  texture_hover='skip_intro_hover'
                                  )
        self.button_play_game = Button(x=self.window.width/2,
                                  y=self.window.height*3/6,
                                  width=500, height=100,
                                  texture_idle='play',
                                  texture_hover='play_hover'
                                  )
        self.background_move_left = False
        self.background_move_left_change_pos = 0
        self.background_move_left_change_pos_speed = 1
        self.background_goes_up = True
        self.background_goes_down = False
        self.background_position = 0
        self.background_finish_animation = False
        self.show_skip_button = False
        self.show_play_game = False
        self.frame = 0
        self.player = pointer.Pointer(level_width=self.window.width*20, level_height=self.window.height*2)
        self.player.center_y = self.window.height+self.player.height
        self.player.center_x = self.window.width/2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.player_sirens_on = False
        self.bad_guys_came_in = False
        self.bad_guys_list = arcade.SpriteList()
        self.bad_guy_a = pointer.BadPointer(self, self.window.width, self.window.height,
                                            (self.window.width/2)*(-100), self.window.height*0.75,0)
        self.bad_guy_b = pointer.BadPointer(self, self.window.width, self.window.height,
                                            (self.window.width/2)*(-85), self.window.height*0.6, 1)
        self.bad_guy_c = pointer.BadPointer(self, self.window.width, self.window.height,
                                            (self.window.width/2)*(-60), self.window.height*0.65, 1)
        self.bad_guys_list.append(self.bad_guy_a)
        self.bad_guys_list.append(self.bad_guy_b)
        self.bad_guys_list.append(self.bad_guy_c)
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shift_pressed = False
        self.space_pressed = False
        self.escape_pressed = False
        self.keyboard_int = 8
        self.keyboard_image = assets.keyboard_hints_paths[7]
        
        # start dialogue
        self.window.music_manager.music.set_volume(0.3) # turn down just for dialogue
        self.voice_channel = assets.game_sfx['voice001'].play()

    def on_show_view(self):
        self.window.cursor.change_state(state='off')

    def on_update(self, delta_time: float):
        self.button_skip.detect_mouse(self.window.cursor)
        self.button_play_game.detect_mouse(self.window.cursor)
        if self.background_goes_up and self.background_position < self.window.height:
            self.background_position += 1
            self.player.center_y -= 0.6
        elif self.background_position == self.window.height:
            self.background_move_left = True
        if self.background_move_left:
            self.background_move_left_change_pos += 1
            if self.background_move_left_change_pos_speed < 5:
                self.background_move_left_change_pos_speed += 0.1
            #if self.background_move_left_change_pos_speed < 15:
            if self.voice_channel.get_busy(): # check now if dialogue still playing before flying up
                if self.background_move_left_change_pos_speed < 15:
                    self.background_move_left_change_pos_speed += 0.01
                if self.background_move_left_change_pos_speed > 7:
                    self.bad_guys_came_in = True
                if self.background_move_left_change_pos_speed > 10:
                    self.player_sirens_on = True

            else:
                if not self.background_goes_down: # start second part of dialogue as ship flies up
                    assets.game_sfx['voice002'].play()
                self.background_goes_down = True
        if self.background_goes_down and self.background_position > 0:
            self.background_position -= 5
        elif self.background_position == 0 and self.background_goes_down:
            self.background_goes_up = False
            self.background_move_left = False
            self.show_skip_button = False
            self.show_play_game = True
        else:
            self.background_goes_down = False
            self.background_move_left = False
        if self.player_sirens_on:
            self.player.update()
        if self.bad_guys_came_in:
            self.bad_guy_a.update()
            self.bad_guy_b.update()
            self.bad_guy_c.update()
        if self.shift_pressed:
            self.keyboard_int = 1
        elif self.escape_pressed:
            self.keyboard_int = 2
        elif self.left_pressed:
            self.keyboard_int = 3
        elif self.down_pressed:
            self.keyboard_int = 4
        elif self.right_pressed:
            self.keyboard_int = 5
        elif self.up_pressed:
            self.keyboard_int = 6
        elif self.space_pressed:
            self.keyboard_int = 7
        else:
            self.keyboard_int = 8
        self.keyboard_image = assets.keyboard_hints_paths[self.keyboard_int-1]

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()
        # In order to count FPS in proper way, add objects below:

        # Draw the background texture
        for x in range(0, 60, 1):
            arcade.draw_lrwh_rectangle_textured(0-self.background_move_left_change_pos *
                                                self.background_move_left_change_pos_speed+
                                                self.window.width*x,
                                                self.background_position-self.window.height,
                                                self.window.width, self.window.height*2,
                                                assets.intro_bg_paths[(x // 10)])

        self.player_list.draw()
        self.bad_guys_list.draw()

        if self.show_skip_button:
            self.button_skip.draw()
        elif self.show_play_game:
            self.button_play_game.draw()
            arcade.draw_lrwh_rectangle_textured(self.window.width / 2 - 500, self.window.height / 2 - 400,
                                                500 * 2, 200 * 2,
                                                self.keyboard_image)

        self.window.developer_tool.on_draw_finish()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if dx+dy > 50:
            self.window.cursor.change_state('idle')
            if not self.show_play_game:
                self.show_skip_button = True

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_skip.current_state == 'hover':
            log('View switched to ' + str(self.window.gameview))
            self.window.music_manager.music.set_volume(1.0)
            if self.voice_channel.get_busy():
                assets.game_sfx['voice001'].stop()
            self.window.gameview.setup('level1')
            self.window.show_view(self.window.gameview)
        elif self.button_play_game.current_state == 'hover':
            log('View switched to ' + str(self.window.gameview))
            self.window.music_manager.music.set_volume(1.0)
            if self.voice_channel.get_busy():
                assets.game_sfx['voice001'].stop()
            self.window.gameview.setup('level1')
            self.window.show_view(self.window.gameview)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            self.window.cursor.change_state('idle')
            self.show_skip_button = True
            self.escape_pressed = True
        elif key == arcade.key.SPACE:
            self.window.cursor.change_state('idle')
            self.space_pressed = True
            self.show_skip_button = True
        elif key == arcade.key.ENTER:
            self.window.cursor.change_state('idle')
            self.show_skip_button = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True
        elif key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.LSHIFT:
            self.shift_pressed = True

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
        elif key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.LSHIFT:
            self.shift_pressed = False
        elif key == arcade.key.ESCAPE:
            self.escape_pressed = False

