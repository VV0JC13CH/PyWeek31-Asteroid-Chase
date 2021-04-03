"""
assets.py

Let's gather all resources from gfx/sfx here, like sprites and sounds.
"""

import arcade
from button import SimpleButton

import math

# we love Windows users:
from pathlib import Path
# we love Ubuntu users (bug fix):
import pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()


def path_to_string(directory, file):
    return str(Path.cwd().joinpath(directory, file).resolve())


# Backgrounds
bg_menu = arcade.load_texture(path_to_string('gfx', 'bg_menu.png'))
bg_campaign = arcade.load_texture(path_to_string('gfx', 'bg_campaign.png'))

# Logo
logo_1 = arcade.load_texture(path_to_string('gfx', 'logo1.png'))
logo_2 = arcade.load_texture(path_to_string('gfx', 'logo2.png'))


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
police_textures = [[]]
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship001.png')))
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship001.png'),flipped_horizontally=True))
police_textures.append([])
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship002.png')))
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship002.png'),flipped_horizontally=True))
police_textures.append([])
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship003.png')))
police_textures[-1].append(arcade.load_texture(path_to_string('gfx', 'police_ship003.png'),flipped_horizontally=True))

# Bad guys
bad_guys = [[]]

bad_guys[-1].append([]) # green dude
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

bad_guys.append([]) # boss :)
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'boss001.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'boss001.png'),flipped_horizontally=True))
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'boss002.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'boss002.png'),flipped_horizontally=True))
bad_guys[-1].append([])
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'boss003.png')))
bad_guys[-1][-1].append(arcade.load_texture(path_to_string('gfx', 'boss003.png'),flipped_horizontally=True))

# laser explosion sprites
explode_textures = [arcade.load_texture(path_to_string('gfx', 'blast001.png')),
                    arcade.load_texture(path_to_string('gfx', 'blast002.png')),
                    arcade.load_texture(path_to_string('gfx', 'blast003.png')),
                    arcade.load_texture(path_to_string('gfx', 'blast004.png')),
                    arcade.load_texture(path_to_string('gfx', 'blast005.png')),
                    arcade.load_texture(path_to_string('gfx', 'blast006.png'))]

# bomb explosion
explodeb_textures = [arcade.load_texture(path_to_string('gfx', 'explode001.png')),
                     arcade.load_texture(path_to_string('gfx', 'explode002.png')),
                     arcade.load_texture(path_to_string('gfx', 'explode003.png')),
                     arcade.load_texture(path_to_string('gfx', 'explode004.png'))]

# bullet/laser textures
bullet_textures = [arcade.load_texture(path_to_string('gfx', 'laser001.png')),
                   arcade.load_texture(path_to_string('gfx', 'laser001.png'), flipped_horizontally=True)]

# Background texture
background_texture = arcade.load_texture(path_to_string('gfx', 'background.png'))
background_texture_game = arcade.load_texture(path_to_string('gfx', 'bg_game.png'))


# Asteroid Textures
asteroid_textures = {'small': []}
asteroid_textures['small'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_small.png')))
asteroid_textures['small'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_small_f.png')))
asteroid_textures['large'] = []
asteroid_textures['large'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_large.png')))
asteroid_textures['large'].append(arcade.load_texture(path_to_string('gfx', 'asteroid_large_f.png')))
asteroid_textures['broken_sat'] = []
asteroid_textures['broken_sat'].append(arcade.load_texture(path_to_string('gfx', 'broken_sat.png')))
asteroid_textures['broken_sat'].append(arcade.load_texture(path_to_string('gfx', 'broken_sat_f.png')))

# Bomb textures
bomb_textures = [arcade.load_texture(path_to_string('gfx', 'bomb001.png')),
                 arcade.load_texture(path_to_string('gfx', 'bomb002.png'))]

# Music paths

music_list = {'menu': path_to_string('music', 'asteroid_chase_menu.ogg'),
              'space_chase': path_to_string('music', 'space_chase.ogg'),
              'the_drop': path_to_string('music', 'the_drop.ogg')}

# Sounds
game_sfx = {'crashsmall': []}
game_sfx['crashsmall'].append(pygame.mixer.Sound(path_to_string('sound', 'crashsmall.ogg')))
game_sfx['crashsmall'].append(pygame.mixer.Sound(path_to_string('sound', 'crashsmall2.ogg')))
game_sfx['crashbig'] = pygame.mixer.Sound(path_to_string('sound', 'crashbig.ogg'))
game_sfx['laser'] = []
game_sfx['laser'].append(pygame.mixer.Sound(path_to_string('sound', 'laser001.ogg')))
game_sfx['laser'].append(pygame.mixer.Sound(path_to_string('sound', 'laser002.ogg')))
game_sfx['asteroid_break_small'] = pygame.mixer.Sound(path_to_string('sound', 'asteroid_break_small.ogg'))
game_sfx['asteroid_break_big'] = pygame.mixer.Sound(path_to_string('sound', 'asteroid_break_big.ogg'))
game_sfx['explode'] = pygame.mixer.Sound(path_to_string('sound', 'explode_big.ogg'))
game_sfx['beep'] = pygame.mixer.Sound(path_to_string('sound', 'beep.ogg'))
game_sfx['fastbeeps'] = pygame.mixer.Sound(path_to_string('sound', 'fastbeeps.ogg'))
game_sfx['boost'] = pygame.mixer.Sound(path_to_string('sound', 'boost.ogg'))
game_sfx['bomblaunch'] = pygame.mixer.Sound(path_to_string('sound', 'bomblaunch.ogg'))
game_sfx['scumbag'] = pygame.mixer.Sound(path_to_string('sound', 'scumbag.ogg'))
game_sfx['hehheh'] = pygame.mixer.Sound(path_to_string('sound', 'hehheh.ogg'))
game_sfx['giant_laser_charge'] = pygame.mixer.Sound(path_to_string('sound', 'giant_laser_charge.ogg'))
game_sfx['giant_laser'] = pygame.mixer.Sound(path_to_string('sound', 'giant_laser.ogg'))
game_sfx['getaway'] = pygame.mixer.Sound(path_to_string('sound', 'getaway.ogg'))
game_sfx['boost_boss'] = pygame.mixer.Sound(path_to_string('sound', 'boost_boss.ogg'))
game_sfx['hehheh_boss'] = pygame.mixer.Sound(path_to_string('sound', 'hehheh_boss.ogg'))
game_sfx['badda_boom'] = pygame.mixer.Sound(path_to_string('sound', 'badda_boom.ogg'))
game_sfx['wallofdeath'] = pygame.mixer.Sound(path_to_string('sound', 'wallofdeath.ogg'))

game_sfx['voice001'] = pygame.mixer.Sound(path_to_string('sound', 'voice001.ogg'))
game_sfx['voice002'] = pygame.mixer.Sound(path_to_string('sound', 'voice002.ogg'))

# Structure textures
structure_textures = {'asteroid': arcade.load_texture(path_to_string('gfx', 'asteroid_texture.png'))}

# Planets
planets_filenames = []
for x in range(1,9,1):
    planet = path_to_string("gfx", "planet_"+str(x)+".png")
    planets_filenames.append(planet)

planet_sprite = None
planet_sprite_list = arcade.SpriteList()
planet_rows = 6
planet_cols = 6
planet_width = 100
planet_height = 100
for z in planets_filenames:
    planet_sprite = arcade.AnimatedTimeBasedSprite()
    planet_sprite_list.append(planet_sprite)
    for x in range(0, planet_rows, 1):
        for y in range(0, planet_cols, 1):
            planet_texture = arcade.texture.load_texture(file_name=z, x=planet_width*x,
                                                         y=planet_height*y, width=planet_width, height=planet_height)
            planet_sprite.textures.append(planet_texture)
        planet_sprite.texture = planet_sprite.textures[0]

# Intro backgrounds:
# Planets
intro_bg_paths = []
for x in range(1,7,1):
    bg_path = arcade.load_texture(path_to_string("gfx", "bg_intro"+str(x)+".png"))
    intro_bg_paths.append(bg_path)

keyboard_hints_paths = []
for x in range(1,9,1):
    bg_path = arcade.load_texture(path_to_string("gfx", "keyboard"+str(x)+".png"))
    keyboard_hints_paths.append(bg_path)




# Static Structures Data

# utility function for planetoids
def CreatePlanetoid(xc,yc,r,nface,rot=0,sx=1.0,sy=1.0):
    dang = (2*math.pi)/nface
    offrad = rot*math.pi/180.0
    verts = []
    for i in range(nface):
        x1 = sx*r*math.cos(i*dang)
        y1 = sy*r*math.sin(i*dang)
        x2 = x1*math.cos(offrad)-y1*math.sin(offrad)
        y2 = x1*math.sin(offrad)+y1*math.cos(offrad)
        verts.append([x2+xc,y2+yc])
    return verts

class Collection(object):
    pass
static_structure = {}

# level 3 big structures

static_structure['rock9'] = Collection()
static_structure['rock9'].verts = CreatePlanetoid(2550,50,150,11)
static_structure['rock9'].type = 'rock'
static_structure['rock1'] = Collection()
static_structure['rock1'].verts = CreatePlanetoid(3000,1000,250,7,sx=1.5)
static_structure['rock1'].type = 'rock'
static_structure['rock2'] = Collection()
static_structure['rock2'].verts = CreatePlanetoid(3600,1000,250,6,sx=1.9)
static_structure['rock2'].type = 'rock'
static_structure['rock3'] = Collection()
static_structure['rock3'].verts = CreatePlanetoid(4250,1000,220,9,sx=1.3)
static_structure['rock3'].type = 'rock'
static_structure['rock4'] = Collection()
static_structure['rock4'].verts = CreatePlanetoid(4900,1000,400,13,rot=-55,sx=1.2)
static_structure['rock4'].type = 'rock'
static_structure['rock8'] = Collection()
static_structure['rock8'].verts = CreatePlanetoid(5700,700,300,11,sx=1.9)
static_structure['rock8'].type = 'rock'

static_structure['rock5'] = Collection()
static_structure['rock5'].verts = CreatePlanetoid(3000,300,250,9,sx=1.9)
static_structure['rock5'].type = 'rock'
static_structure['rock6'] = Collection()
static_structure['rock6'].verts = CreatePlanetoid(3700,200,270,8,rot=-35,sx=1.7)
static_structure['rock6'].type = 'rock'
static_structure['rock7'] = Collection()
static_structure['rock7'].verts = CreatePlanetoid(4250,0,220,7)
static_structure['rock7'].type = 'rock'

static_structure['rock10'] = Collection()
static_structure['rock10'].verts = CreatePlanetoid(8000,750,300,24,sx=3.0)
static_structure['rock10'].type = 'rock'
static_structure['rock11'] = Collection()
static_structure['rock11'].verts = CreatePlanetoid(8820,430,195,7,sx=1.1)
static_structure['rock11'].type = 'rock'
static_structure['rock12'] = Collection()
static_structure['rock12'].verts = CreatePlanetoid(8900,0,220,9,sx=1.2)
static_structure['rock12'].type = 'rock'

static_structure['rock13'] = Collection()
static_structure['rock13'].verts = CreatePlanetoid(13000,750,400,11,sx=3.0)
static_structure['rock13'].type = 'rock'

static_structure['rock14'] = Collection()
static_structure['rock14'].verts = CreatePlanetoid(16000,450,200,11,sx=3.0)
static_structure['rock14'].type = 'rock'
static_structure['rock15'] = Collection()
static_structure['rock15'].verts = CreatePlanetoid(16000,1050,200,11,sx=3.0)
static_structure['rock15'].type = 'rock'


static_structure['rock16'] = Collection()
static_structure['rock16'].verts = CreatePlanetoid(19000,750,200,7,sx=1.4)
static_structure['rock16'].type = 'rock'
static_structure['rock17'] = Collection()
static_structure['rock17'].verts = CreatePlanetoid(19500,1000,200,7,sx=1.2)
static_structure['rock17'].type = 'rock'
static_structure['rock18'] = Collection()
static_structure['rock18'].verts = CreatePlanetoid(20000,300,200,7,sx=1.3)
static_structure['rock18'].type = 'rock'
static_structure['rock19'] = Collection()
static_structure['rock19'].verts = CreatePlanetoid(20500,750,200,7,sx=1.1)
static_structure['rock19'].type = 'rock'

static_structure['rock20'] = Collection()
static_structure['rock20'].verts = CreatePlanetoid(22000,0,400,7,sy=2.5)
static_structure['rock20'].type = 'rock'
static_structure['rock21'] = Collection()
static_structure['rock21'].verts = CreatePlanetoid(23000,1400,400,7,sy=2.4)
static_structure['rock21'].type = 'rock'
static_structure['rock22'] = Collection()
static_structure['rock22'].verts = CreatePlanetoid(24000,0,400,7,sy=2.6)
static_structure['rock22'].type = 'rock'

# Wall of death
static_structure['wod1'] = Collection()
static_structure['wod1'].verts = CreatePlanetoid(3000,750,400,7,sx=1.3)
static_structure['wod1'].type = 'rock'

static_structure['wod2'] = Collection()
static_structure['wod2'].verts = CreatePlanetoid(6000,300,700,7,sx=1.4)
static_structure['wod2'].type = 'rock'

static_structure['wod3'] = Collection()
static_structure['wod3'].verts = CreatePlanetoid(9000,1500,800,7,sx=1.7)
static_structure['wod3'].type = 'rock'

static_structure['wod4'] = Collection()
static_structure['wod4'].verts = CreatePlanetoid(11000,400,400,9,sx=1.3)
static_structure['wod4'].type = 'rock'

static_structure['wod5'] = Collection()
static_structure['wod5'].verts = CreatePlanetoid(13000,1100,500,9,sx=1.4)
static_structure['wod5'].type = 'rock'

# Bad Guy Archetypes
bad_guydata = {}
bad_guydata['green1'] = Collection()
bad_guydata['green1'].type = 0
bad_guydata['green1'].start_pos = (900,900)
bad_guydata['green1'].action_data = [('boost',0.5)]

bad_guydata['green2'] = Collection()
bad_guydata['green2'].type = 0
bad_guydata['green2'].start_pos = (300,300)
bad_guydata['green2'].action_data = [('boost',0.55)]

bad_guydata['purple1'] = Collection()
bad_guydata['purple1'].type = 1
bad_guydata['purple1'].start_pos = (700,600)
bad_guydata['purple1'].action_data = action_data = [('bomb',0.2),('bomb',0.4),('bomb',0.6),('bomb',0.8),('bomb',0.9),
            ('boost',0.3),('boost',0.6)]

bad_guydata['green1_3'] = Collection()
bad_guydata['green1_3'].type = 0
bad_guydata['green1_3'].start_pos = (900,900)
bad_guydata['green1_3'].action_data = [('boost',0.08),('boost',0.5)]

bad_guydata['green2_3'] = Collection()
bad_guydata['green2_3'].type = 0
bad_guydata['green2_3'].start_pos = (300,300)
bad_guydata['green2_3'].action_data = [('boost',0.08),('boost',0.55)]

bad_guydata['green3_3'] = Collection()
bad_guydata['green3_3'].type = 0
bad_guydata['green3_3'].start_pos = (9100,1400)
bad_guydata['green3_3'].action_data = [('boost',0.08),('boost',0.55)]

bad_guydata['purple1_3'] = Collection()
bad_guydata['purple1_3'].type = 1
bad_guydata['purple1_3'].start_pos = (700,600)
bad_guydata['purple1_3'].action_data = action_data = [('bomb',0.2),('bomb',0.25),('bomb',0.50),('bomb',0.6),('bomb',0.8),('bomb',0.9),
            ('boost',0.07),('boost',0.1),('boost',0.25),('boost',0.4),('boost',0.6)]

bad_guydata['boss'] = Collection()
bad_guydata['boss'].type = 2
bad_guydata['boss'].start_pos = (700,600)
bad_guydata['boss'].action_data = [('bomb',0.1),('bomb',0.2),('bomb',0.3),('bomb',0.4),('bomb',0.5),
                                ('bomb',0.6),('bomb',0.7),('bomb',0.8),('bomb',0.9),('boost',0.3),('boost',0.6)]

# Level Data (it's sort of like an asset :) )
class LevelData(object):
    pass

leveldata = {}

leveldata['level1'] = LevelData()
leveldata['level1'].music = 'space_chase'
leveldata['level1'].size = (25000,2000) # level_width, level_height
leveldata['level1'].player_start = (400,600) # position
leveldata['level1'].asteroid_density = 10 # asteroids per screen width
leveldata['level1'].badguy_ids = ['green1','green2']
leveldata['level1'].static_structures = []
leveldata['level1'].lanes = [] # each lane is [start-x, finish-x, ypos]

leveldata['level2'] = LevelData()
leveldata['level2'].music = 'space_chase'
leveldata['level2'].size = (25000,3000) # level_width, level_height
leveldata['level2'].player_start = (400,400) # position
leveldata['level2'].asteroid_density = 20 # asteroids per screen width
leveldata['level2'].badguy_ids = ['green1','green2','purple1']
leveldata['level2'].static_structures = []
leveldata['level2'].lanes = []

leveldata['level3'] = LevelData()
leveldata['level3'].music = 'space_chase'
leveldata['level3'].size = (35000,1500) # level_width, level_height
leveldata['level3'].player_start = (400,600) # position
leveldata['level3'].asteroid_density = 10 # asteroids per screen width
leveldata['level3'].badguy_ids = ['green1_3','green2_3','green3_3','purple1_3']
leveldata['level3'].static_structures = ['rock1','rock2','rock3','rock4','rock5','rock6',
                                        'rock7','rock8','rock9','rock10','rock11','rock12',
                                        'rock13','rock14','rock15',
                                        'rock16','rock17','rock18','rock19',
                                        'rock20','rock21','rock22']
leveldata['level3'].lanes = [[1500,4100,600],[4300,5000,200],[6500,9000,230],
                            [11500,14000,200],[11500,14000,1300],
                            [14000,16600,750],[14000,16600,1300]] 
# each lane is [start-x, finish-x, ypos]



leveldata['level4'] = LevelData()
leveldata['level4'].music = 'the_drop'
leveldata['level4'].size = (65000,2000) # level_width, level_height
leveldata['level4'].player_start = (400,400) # position
leveldata['level4'].asteroid_density = 10 # asteroids per screen width
leveldata['level4'].badguy_ids = ['boss']
leveldata['level4'].static_structures = []
leveldata['level4'].lanes = [] # each lane is [start-x, finish-x, ypos]

leveldata['level5'] = LevelData()
leveldata['level5'].music = 'the_drop'
leveldata['level5'].size = (30000,1500) # level_width, level_height
leveldata['level5'].player_start = (800,400) # position
leveldata['level5'].asteroid_density = 10 # asteroids per screen width
leveldata['level5'].badguy_ids = []
leveldata['level5'].static_structures = ['wod1','wod2','wod3','wod4','wod5']
leveldata['level5'].lanes = [] # each lane is [start-x, finish-x, ypos]

