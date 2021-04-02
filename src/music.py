"""
music.py
Let's play music!
"""

import arcade
import assets
import time


class MusicManager:
    def __init__(self, init_volume=0.8):
        self.volume = float(init_volume)
        self.current_player = None
        self.music_list = []
        self.current_song = 0
        self.music = None
        self.music_enabled = False

    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """
        self.current_song += 1
        if self.current_song >= len(self.music_list):
            self.current_song = 0

    def start_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        # Play the next song
        if self.music and self.music_enabled:
            self.music.stop(self.current_player)
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.current_player = self.music.play(self.volume)
        self.music_enabled = True
        time.sleep(0.03)

    def play_song(self, song_to_play):
        """Force song to be played"""
        for song, path in assets.music_list.items():
            if song == song_to_play:
                for known_song in self.music_list:
                    if known_song == path:
                        self.current_song = self.music_list.index(known_song)
        if self.music_enabled:
            # Play the song
            self.start_song()

    def stop_song(self):
        time.sleep(0.03)
        self.music.stop(self.current_player)
        self.music_enabled = False

    def setup(self, music_enabled):
        """ Set up the game here. Call this function to restart the game. """
        for song, path in assets.music_list.items():
            self.music_list.append(path)
        # Array index of what to play
        self.current_song = 0
        if music_enabled:
            # Play the song
            self.start_song()
            self.music_enabled = music_enabled

    def on_draw(self, screen_height, developer_mode, screen_beginning=0):
        """ Render the screen. """
        if developer_mode:
            position = self.music.get_stream_position(self.current_player)
            length = self.music.get_length()
            text_position = f"Currently playing: {int(position) // 60}:{int(position) % 60:02} of {int(length) // 60}:{int(length) % 60:02}"
            text_song = f" {self.music_list[self.current_song]}"
            arcade.draw_text(text_position + ' ' + text_song, screen_beginning + 20, screen_height - 20,
                             arcade.color.WHITE_SMOKE, 18)

    def on_update(self, dt):
        position = self.music.get_stream_position()
        if position == 0.0:
            self.advance_song()
            self.start_song()