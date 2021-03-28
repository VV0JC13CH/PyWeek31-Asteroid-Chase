"""
gui.py

Place for UI objects and methods
"""
from arcade import gui
from arcade.gui import UIManager

# In order to call single UI manager, we are going to init it here:
manager = UIManager()


class ChangeSceneButton(gui.UIFlatButton):
    def __init__(self, global_window, on_click_scene):
        self._global_window = global_window
        self._on_click_scene = on_click_scene
        super().__init__()

    def on_click(self):
        """ Called when user lets off button """
        self._global_window.show_view(self._on_click_scene)
