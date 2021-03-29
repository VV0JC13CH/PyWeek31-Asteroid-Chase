"""
run_game.py

Use this file to launch the Asteroid Chase game.
"""

# --- Import external modules ---
import arcade
# --- Import internal classes ---
import data
import assets
from menu import MenuView
from developer import DeveloperTool
from cursor import Cursor
# --- Constants ---
settings = data.load_settings()
SCREEN_TITLE = settings['GAME']['TITLE']
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])
SCREEN_HEIGHT = int(settings['VIDEO']['WINDOW_HEIGHT'])
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
        self.developer_mode = developer_mode
        self.music_enabled = music_enabled
        # Game logic global variables:
        self.developer_tool = DeveloperTool(developer_mode)
        # Arcade engine global variables:
        self.set_mouse_visible(False)
        self.cursor = Cursor()
        # Start view
        self.start_view = MenuView()

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """
        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)
        for button in assets.button_register:
            button.center_horizontally(self)

    def on_draw(self):
        self.cursor.draw()
        self.developer_tool.on_draw(self.height)

    def on_update(self, delta_time: float):
        self.developer_tool.on_update(delta_time=delta_time, enable_tools=self.developer_mode)
        self.cursor.update()

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.cursor.get_position(x, y)


def main():
    """ Main method """
    global_window = GlobalWindow()
    global_window.show_view(global_window.start_view)
    arcade.run()


if __name__ == "__main__":
    main()