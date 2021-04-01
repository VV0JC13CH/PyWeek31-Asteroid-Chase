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
        self.button_skip = Button(x=self.window.width,
                                  y=self.window.height * 1 / 8,
                                  width=250, height=50,
                                  texture_idle='skip_intro',
                                  texture_hover='skip_intro_hover'
                                  )
        self.background_move_left = False
        self.background_move_left_change_pos = 0
        self.background_move_left_change_pos_speed = 1
        self.background_goes_up = True
        self.background_goes_down = False
        self.background_position = 0
        self.background_finish_animation = False
        self.show_skip_button = False
        self.frame = 0
        self.player = pointer.Pointer(level_width=self.window.width*60, level_height=self.window.height*2)

    def on_show_view(self):
        self.window.cursor.change_state(state='off')

    def on_update(self, delta_time: float):
        self.button_skip.detect_mouse(self.window.cursor)
        if self.background_goes_up and self.background_position < self.window.height:
            self.background_position += 1
        elif self.background_position == self.window.height:
            self.background_move_left = True
        if self.background_move_left:
            self.background_move_left_change_pos += 1
            if self.background_move_left_change_pos_speed < 5:
                self.background_move_left_change_pos_speed += 0.1
            if self.background_move_left_change_pos_speed < 15:
                self.background_move_left_change_pos_speed += 0.01
            else:
                self.background_goes_down = True
        if self.background_goes_down and self.background_position > 0:
            self.background_position -= 5
        elif self.background_position == 0 and self.background_goes_down:
            self.background_goes_up = False
            self.background_move_left = False
        else:
            self.background_goes_down = False
            self.background_move_left = False

    def on_draw(self):
        self.window.developer_tool.on_draw_start()
        arcade.start_render()
        # In order to count FPS in proper way, add objects below:

        # Draw the background texture
        for x in range(0, 15, 1):
            arcade.draw_lrwh_rectangle_textured(0-self.background_move_left_change_pos *
                                                self.background_move_left_change_pos_speed+
                                                self.window.width*x,
                                                self.background_position-self.window.height,
                                                self.window.width, self.window.height*2,
                                                assets.intro_bg_paths[(x // 5)])
        if self.show_skip_button:
            self.button_skip.draw()
        self.window.developer_tool.on_draw_finish()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if dx+dy > 50:
            self.window.cursor.change_state('idle')
            self.show_skip_button = True

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.button_skip.current_state == 'hover':
            self.window.game_view = GameView(LEVEL_WIDTH, LEVEL_HEIGHT)
            self.window.scenes.append(self.window.game_view)
            log('View switched to ' + str(self.window.game_view))
            self.window.show_view(self.window.game_view)
