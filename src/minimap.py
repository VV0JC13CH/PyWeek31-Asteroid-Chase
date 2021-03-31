"""
minimap.py

Place for MiniMap functions.
"""
import arcade
import data

# --- Constants ---
param = data.load_parameters()

# Size of the playing field if not set
LEVEL_WIDTH = int(param['LEVEL']['DEFAULT_WIDTH'])
LEVEL_HEIGHT = int(param['LEVEL']['DEFAULT_HEIGHT'])

# --- Mini-map related ---
# Size of the minimap
MINIMAP_HEIGHT = int(param['MAP']['HEIGHT'])

PLAYERHEALTH = float(param['PLAYER']['HEALTH'])

def draw_minimap(game_view, map_height=MINIMAP_HEIGHT, level_width=LEVEL_WIDTH, level_height=LEVEL_HEIGHT):
    # Draw a background for the minimap
    arcade.draw_rectangle_outline(game_view.window.width - game_view.window.width / 2 + game_view.view_left,
                                  map_height * 0.3 + game_view.view_bottom,
                                  game_view.window.width * 0.8,
                                  map_height * 0.4,
                                  arcade.color.WHITE_SMOKE)

    # Draw a rectangle showing where the screen is
    width_ratio = game_view.window.width / level_width
    height_ratio = map_height / level_height
    width = width_ratio * game_view.window.width
    main_height = map_height
    height = height_ratio * main_height

    x = (game_view.view_left + game_view.window.width / 2) * width_ratio + game_view.view_left
    y = map_height + game_view.view_bottom + height / 2 + (main_height / level_height) * game_view.view_bottom

    arcade.draw_rectangle_outline(center_x=x, center_y=y,
                                  width=width, height=height,
                                  color=arcade.color.WHITE)
    
    # Other HUD stuff
    
    # Player health
    meter_x = 100*(game_view.player_sprite.health/PLAYERHEALTH)
    arcade.draw_text("Shield", game_view.view_left+40, game_view.view_bottom+game_view.window.height-30, arcade.color.WHITE, 18)
    x = game_view.view_left+70
    y = game_view.view_bottom+game_view.window.height-45
    arcade.draw_rectangle_filled(center_x=x-(50-meter_x/2), center_y=y,
                                  width=meter_x, height=10,
                                  color=arcade.color.ORANGE)
    arcade.draw_rectangle_outline(center_x=x, center_y=y,
                                  width=100, height=10,
                                  color=arcade.color.WHITE)
    
    # draw player on mini map
    x = game_view.window.width * 0.2 + game_view.view_left + (game_view.window.width * 0.8)*(game_view.player_sprite.center_x/level_width)
    y = map_height * 0.3 + game_view.view_bottom + (map_height * 0.4)*(game_view.player_sprite.center_y/level_height)
    arcade.draw_circle_filled(x, y, 5, arcade.color.GREEN)
    
    # draw badguys on mini map
    for badguy in game_view.badguys_sprite_list:
        x = game_view.window.width * 0.2 + game_view.view_left + (game_view.window.width * 0.8)*(badguy.center_x/level_width)
        y = map_height * 0.3 + game_view.view_bottom + (map_height * 0.4)*(badguy.center_y/level_height)
        if badguy.health > 0:
            arcade.draw_circle_filled(x, y, 5, arcade.color.RED)
        else:
            arcade.draw_circle_filled(x, y, 5, arcade.color.GRAY)


