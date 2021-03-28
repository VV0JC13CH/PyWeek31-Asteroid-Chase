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

# --- Constants ---
settings = data.load_settings()
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
SCREEN_HEIGHT = int(settings['VIDEO']['WINDOW_HEIGHT'])
SCREEN_TITLE = settings['GAME']['TITLE']


class GlobalWindow(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Game logic global variables:
        self.fps_counter = FpsCounter()
        # Arcade engine global variables:
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def on_draw(self):
        self.fps_counter.on_draw(self.height)

    def on_update(self, delta_time: float):
        self.fps_counter.on_update(delta_time=delta_time)


def main():
    """ Main method """
    global_window = GlobalWindow()
    start_view = MenuView()
    global_window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()