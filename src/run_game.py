"""
run_game.py

Use this file to launch the Asteroid Chase game.
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data
from menu import MenuView
from fps import FpsCounter
from cursor import Cursor
# --- Constants ---
settings = data.load_settings()
SCREEN_TITLE = settings['GAME']['TITLE']
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
SCREEN_HEIGHT = int(settings['VIDEO']['WINDOW_HEIGHT'])
# --- Variables ---
full_resolution = False if settings['VIDEO']['FULL_RESOLUTION'] == 'False' else True
developer_mode = False if settings['GAME']['DEVELOPER_MODE'] == 'False' else True
music_enabled = False if settings['AUDIO']['MUSIC_ON'] == 'False' else True


class GlobalWindow(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, full_resolution)
        self.developer_mode = developer_mode
        self.music_enabled = music_enabled
        # Game logic global variables:
        self.fps_counter = FpsCounter()
        # Arcade engine global variables:
        self.set_mouse_visible(False)
        self.cursor = Cursor()

    def on_draw(self):
        self.cursor.draw()
        self.fps_counter.on_draw(self.height)

    def on_update(self, delta_time: float):
        self.fps_counter.on_update(delta_time=delta_time)
        self.cursor.update()

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.cursor.get_position(x, y)


def main():
    """ Main method """
    global_window = GlobalWindow()
    start_view = MenuView()
    global_window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()