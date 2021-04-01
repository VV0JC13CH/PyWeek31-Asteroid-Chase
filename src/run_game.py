"""
run_game.py

Use this file to launch the Asteroid Chase game.
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data
import assets
import music
from menu import MenuView
from intro import IntroView
from campaign import CampaignView
from game import GameView
from developer import DeveloperTool, log
from cursor import Cursor
# --- Constants ---
settings = data.load_settings()
SCREEN_TITLE = settings['GAME']['TITLE']
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
SCREEN_HEIGHT = int(settings['VIDEO']['WINDOW_HEIGHT'])
MUSIC_VOL = int(settings['AUDIO']['MUSIC_VOL'])
# --- Variables ---
full_resolution = False if settings['VIDEO']['FULL_RESOLUTION'] == 'False' else True
screen_resizeable = False if settings['VIDEO']['WINDOW_RESIZEABLE'] == 'False' else True
developer_mode = False if settings['GAME']['DEVELOPER_MODE'] == 'False' else True
music_enabled = False if settings['AUDIO']['MUSIC_ON'] == 'False' else True


class GlobalWindow(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, full_resolution, resizable=screen_resizeable)
        # If levels_unlocked = 0 - play intro and add +1:
        self.levels_unlocked = 0
        self.music_manager = music.MusicManager(init_volume=MUSIC_VOL)
        self.music_manager.setup(music_enabled)
        self.music_manager.play_song('menu')
        self.music_enabled = music_enabled
        self.developer_mode = developer_mode
        # Game logic global variables:
        self.developer_tool = DeveloperTool(self.developer_mode)
        # Arcade engine global variables:
        self.set_mouse_visible(False)
        self.cursor = Cursor()
        # Start view
        self.start_view = MenuView()
        self.active_view = 0
        self.scenes = [self.start_view]
        self.current_view_name = 'menu_view'
        # Views:
        self.pause_view = None
        self.campaign_view = CampaignView()
        self.scenes.append(self.campaign_view)
        
        self.gameview = GameView()
        self.scenes.append(self.gameview)

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """
        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)
        for button in assets.button_register:
            button.center_horizontally(self)
            log(f"Window resized to: {width}, {height}")

    def on_draw(self):
        self.cursor.draw()
        if self.developer_mode and self.current_view_name != 'game_view':
            self.developer_tool.on_draw(self.height)
            self.music_manager.on_draw(self.height, self.developer_mode)

    def on_update(self, delta_time: float):
        self.developer_tool.on_update(delta_time=delta_time, enable_tools=self.developer_mode)
        self.cursor.update()

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.cursor.get_position(x, y)

    def on_key_press(self, key, modifiers):
        """Global keys. Mostly for developer control"""
        # F1 - developer mode
        if key == arcade.key.F1:
            self.developer_mode = not self.developer_mode
            log('Developer mode turned to ' + str(not self.developer_mode))
        # F2 - fullscreen mode
        elif key == arcade.key.F2 and self.developer_mode:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, self.width, 0, self.height)
            log('Fullscreen mode turned to ' + str(not self.fullscreen))
        # F3 - turn music on/off
        elif key == arcade.key.F3 and self.developer_mode:
            self.music_enabled = not self.music_enabled
            if self.music_enabled:
                self.music_manager.play_song()
            else:
                self.music_manager.stop_song()
            log('Music turned ' + str(not self.music_enabled))
        # F4 - switch to all registered views player was before:
        elif key == arcade.key.F4 and self.developer_mode:
            if self.active_view < len(self.scenes)-1:
                self.active_view += 1
            else:
                self.active_view = 0
            log('View switched to ' + str(self.scenes[self.active_view]))
            arcade.set_viewport(0, self.width, 0, self.height)
            self.show_view(self.scenes[self.active_view])


def main():
    """ Main method """
    global_window = GlobalWindow()
    global_window.show_view(global_window.start_view)
    arcade.run()


if __name__ == "__main__":
    main()