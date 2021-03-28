"""
fps.py

Place for fps related methods
"""

import timeit
import arcade


class FpsCounter:
    def __init__(self):
        self.start_time = 0
        self.processing_time = 0
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

    def on_draw_start(self):
        # Start timing how long this takes
        self.start_time = timeit.default_timer()
        # --- Calculate FPS

        fps_calculation_freq = 60
        # Once every 60 frames, calculate our FPS
        if self.frame_count % fps_calculation_freq == 0:
            # Do we have a start time?
            if self.fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            # Reset the timer
            self.fps_start_timer = timeit.default_timer()
        # Add one to our frame count
        self.frame_count += 1

    def on_draw_finish(self):
        # Stop the draw timer, and calculate total on_draw time.
        self.draw_time = timeit.default_timer() - self.start_time

    def on_draw(self, screen_height):
        """ Draw everything """
        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output, 20, screen_height - 25, arcade.color.BLACK, 18)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output, 20, screen_height - 50, arcade.color.BLACK, 18)

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcade.draw_text(output, 20, screen_height - 75, arcade.color.BLACK, 18)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Start timing how long this takes
        start_time = timeit.default_timer()

        # Stop the draw timer, and calculate total on_draw time.
        self.processing_time = timeit.default_timer() - start_time



