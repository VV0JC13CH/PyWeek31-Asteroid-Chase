"""
assets.py

Let's gather all resources from gfx/sfx here, like sprites and sounds.
"""

import arcade
from button import SimpleButton

# we love Windows users:
from pathlib import Path


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


# Backgrounds
bg_menu = arcade.load_texture(path_to_string('gfx', 'bg_menu.png'))
bg_campaign = arcade.load_texture(path_to_string('gfx', 'bg_campaign.png'))


# Buttons
buttons_sprites = path_to_string('gfx', 'buttons.png')
# List of all buttons used to iterate over all in order to reset position after fullscreen switch
button_register = []

button_pause_idle = SimpleButton(button_col=0, button_row=0)
button_pause_hover = SimpleButton(button_col=1, button_row=0)
button_reset_idle = SimpleButton(button_col=0, button_row=1)
button_reset_hover = SimpleButton(button_col=1, button_row=1)
button_music_off_idle = SimpleButton(button_col=0, button_row=2)
button_music_off_hover = SimpleButton(button_col=1, button_row=2)
button_music_on_idle = SimpleButton(button_col=0, button_row=3)
button_music_on_hover = SimpleButton(button_col=1, button_row=3)
button_full_off_idle = SimpleButton(button_col=0, button_row=4)
button_full_off_hover = SimpleButton(button_col=1, button_row=4)
button_full_on_idle = SimpleButton(button_col=0, button_row=5)
button_full_on_hover = SimpleButton(button_col=1, button_row=5)
button_skip_intro_idle = SimpleButton(button_col=0, button_row=6)
button_skip_intro_hover = SimpleButton(button_col=1, button_row=6)
button_back_game_idle = SimpleButton(button_col=0, button_row=7)
button_back_game_hover = SimpleButton(button_col=1, button_row=7)
button_back_menu_idle = SimpleButton(button_col=0, button_row=8)
button_back_menu_hover = SimpleButton(button_col=1, button_row=8)
button_exit_idle = SimpleButton(button_col=0, button_row=9)
button_exit_hover = SimpleButton(button_col=1, button_row=9)
button_settings_idle = SimpleButton(button_col=0, button_row=10)
button_settings_hover = SimpleButton(button_col=1, button_row=10)
button_play_idle = SimpleButton(button_col=0, button_row=11)
button_play_hover = SimpleButton(button_col=1, button_row=11)
button_dev_on_idle = SimpleButton(button_col=0, button_row=12)
button_dev_on_hover = SimpleButton(button_col=1, button_row=12)
button_dev_off_idle = SimpleButton(button_col=0, button_row=13)
button_dev_off_hover = SimpleButton(button_col=1, button_row=13)
button_back_camp_idle = SimpleButton(button_col=0, button_row=14)
button_back_camp_hover = SimpleButton(button_col=1, button_row=14)

button_textures = {"pause": button_pause_idle,
                   "pause_hover": button_pause_hover,
                   "reset": button_reset_idle,
                   "reset_hover": button_reset_hover,
                   "music_off": button_music_off_idle,
                   "music_off_hover": button_music_off_hover,
                   "music_on": button_music_on_idle,
                   "music_on_hover": button_music_on_hover,
                   "full_off": button_full_off_idle,
                   "full_off_hover": button_full_off_hover,
                   "full_on": button_full_on_idle,
                   "full_on_hover": button_full_on_hover,
                   "skip_intro": button_skip_intro_idle,
                   "skip_intro_hover": button_skip_intro_hover,
                   "back_game": button_back_game_idle,
                   "back_game_hover": button_back_game_hover,
                   "back_menu": button_back_menu_idle,
                   "back_menu_hover": button_back_menu_hover,
                   "exit": button_exit_idle,
                   "exit_hover": button_exit_hover,
                   "settings": button_settings_idle,
                   "settings_hover": button_settings_hover,
                   "play": button_play_idle,
                   "play_hover": button_play_hover,
                   "dev_on": button_dev_on_idle,
                   "dev_on_hover": button_dev_on_hover,
                   "dev_off": button_dev_off_idle,
                   "dev_off_hover": button_dev_off_hover,
                   "back_camp": button_back_camp_idle,
                   "back_camp_hover": button_back_camp_hover
                   }

# Cursor
cursor_hover = arcade.Sprite(filename=path_to_string('gfx', 'cursor_hover.png'))
cursor_idle = arcade.Sprite(filename=path_to_string('gfx', 'cursor_idle.png'))
cursor_no = arcade.Sprite(filename=path_to_string('gfx', 'cursor_no.png'))

# Player Police Car
police_textures = []
police_textures.append([])
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship001.png')))
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship001.png'),flipped_horizontally=True))
police_textures.append([])
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship002.png')))
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship002.png'),flipped_horizontally=True))
police_textures.append([])
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship003.png')))
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship003.png'),flipped_horizontally=True))

# Bad guys
bad_guys = []

bad_guys.append([]) # first green dude
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandit001.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandit001.png'),flipped_horizontally=True))
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandit002.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandit002.png'),flipped_horizontally=True))
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandit003.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandit003.png'),flipped_horizontally=True))

bad_guys.append([]) # second purple dude :)
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandita001.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandita001.png'),flipped_horizontally=True))
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandita002.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandita002.png'),flipped_horizontally=True))
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandita003.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'bandita003.png'),flipped_horizontally=True))

# laser explosion sprites
explode_textures = []
explode_textures.append(arcade.load_texture(path_to_string('gfx', 'blast001.png')))
explode_textures.append(arcade.load_texture(path_to_string('gfx', 'blast002.png')))
explode_textures.append(arcade.load_texture(path_to_string('gfx', 'blast003.png')))
explode_textures.append(arcade.load_texture(path_to_string('gfx', 'blast004.png')))
explode_textures.append(arcade.load_texture(path_to_string('gfx', 'blast005.png')))
explode_textures.append(arcade.load_texture(path_to_string('gfx', 'blast006.png')))

# bullet/laser textures
bullet_textures = []
bullet_textures.append(arcade.load_texture(path_to_string('gfx', 'laser001.png')))
bullet_textures.append(arcade.load_texture(path_to_string('gfx', 'laser001.png'),flipped_horizontally=True))

# Background texture
background_texture = arcade.load_texture(path_to_string('gfx', 'background.png'))

# Asteroid Textures
asteroid_textures = {}
asteroid_textures['small'] = []
asteroid_textures['small'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_small.png')))
asteroid_textures['small'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_small_f.png')))
asteroid_textures['large'] = []
asteroid_textures['large'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_large.png')))
asteroid_textures['large'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_large_f.png')))
asteroid_textures['broken_sat'] = []
asteroid_textures['broken_sat'].append(arcade.load_texture(path_to_string('gfx', 'broken_sat.png')))
asteroid_textures['broken_sat'].append(arcade.load_texture(path_to_string('gfx', 'broken_sat_f.png')))

# Music paths
music_path = {}
music_path['space_chase'] = path_to_string('music', 'space_chase.ogg')
music_path['the_drop'] = path_to_string('music', 'the_drop.ogg')

musics = {}
for path in music_path:
    musics[path] = arcade.Sound(music_path[path], streaming=True)

# Sounds
game_sfx = {}
game_sfx['crashsmall'] = []
game_sfx['crashsmall'].append(arcade.Sound(path_to_string('sound', 'crashsmall.ogg')))
game_sfx['crashsmall'].append(arcade.Sound(path_to_string('sound', 'crashsmall2.ogg')))
game_sfx['crashbig'] = arcade.Sound(path_to_string('sound', 'crashbig.ogg'))
game_sfx['laser'] = []
game_sfx['laser'].append(arcade.Sound(path_to_string('sound', 'laser001.ogg')))
game_sfx['laser'].append(arcade.Sound(path_to_string('sound', 'laser002.ogg')))
game_sfx['asteroid_break_small'] = arcade.Sound(path_to_string('sound', 'asteroid_break_small.ogg'))
game_sfx['asteroid_break_big'] = arcade.Sound(path_to_string('sound', 'asteroid_break_big.ogg'))

# Structure textures
structure_textures = {}
structure_textures['asteroid'] = arcade.load_texture(path_to_string('gfx', 'asteroid_texture.png'))

# Static Structures Data
class Collection(object):
    pass
static_structure = {}
static_structure['rock1'] = Collection()
static_structure['rock1'].verts = [[600,600],[600,700],[1000,700],[1200,650],[800,550]]
static_structure['rock1'].type = 'rock'

