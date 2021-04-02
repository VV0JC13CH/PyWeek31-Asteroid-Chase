"""
minimap.py

Place for MiniMap functions.
"""
import arcade
import data
import assets
import developer
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
    
    map_width = game_view.window.width * 0.8
    hor_offset = (game_view.window.width-map_width)/2
    vert_offset = map_height * 0.3
    
    # Draw a background for the minimap
    arcade.draw_rectangle_outline(hor_offset + map_width/ 2 + game_view.view_left,
                                  vert_offset + map_height/2 + game_view.view_bottom,
                                  map_width,
                                  map_height,
                                  arcade.color.GREEN) #WHITE_SMOKE
    
    arcade.draw_text("Police Radar", 
                    hor_offset + game_view.view_left+5, 
                    vert_offset + map_height + game_view.view_bottom-18, 
                    arcade.color.GREEN, 12)
    
    # Draw a rectangle showing where the screen is
    width_ratio = game_view.window.width / level_width
    height_ratio = game_view.window.height / level_height
    width = width_ratio * map_width
    height = height_ratio * map_height

    x = (game_view.view_left/level_width)*map_width + width/2 + game_view.view_left + hor_offset
    y = (game_view.view_bottom/level_height)*map_height + height/2 + game_view.view_bottom + vert_offset

    arcade.draw_rectangle_outline(center_x=x, center_y=y,
                                  width=width, height=height,
                                  color=arcade.color.GREEN)
    
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
    
    if game_view.outcome == 'death':
        arcade.draw_text("Police Ship\nOut of Action", game_view.view_left+game_view.window.width/2-450, game_view.view_bottom+game_view.window.height/2, arcade.color.ORANGE, 56, width=900, align="center")
    elif game_view.outcome == 'failure':
        arcade.draw_text("Mission Failed!", game_view.view_left+game_view.window.width/2-450, game_view.view_bottom+game_view.window.height/2, arcade.color.RED, 56, width=900, align="center")
    elif game_view.outcome == 'victory':
        arcade.draw_text("Mission Complete!", game_view.view_left+game_view.window.width/2-450, game_view.view_bottom+game_view.window.height/2, arcade.color.GREEN, 56, width=900, align="center")
    
    # draw player on mini map
    x = hor_offset + game_view.view_left + map_width*(game_view.player_sprite.center_x/level_width)
    y = vert_offset + game_view.view_bottom + map_height*(game_view.player_sprite.center_y/level_height)
    arcade.draw_circle_filled(x, y, 5, arcade.color.GREEN)
    
    # draw badguys on mini map
    for badguy in game_view.badguys_sprite_list:
        x = game_view.window.width * 0.1 + game_view.view_left + (game_view.window.width * 0.8)*(badguy.center_x/level_width)
        y = map_height * 0.3 + game_view.view_bottom + map_height*(badguy.center_y/level_height)
        if badguy.health > 0:
            arcade.draw_circle_filled(x, y, 5, arcade.color.RED)
        else:
            arcade.draw_circle_filled(x, y, 5, arcade.color.GRAY)

    game_view.window.developer_tool.on_draw(screen_height=game_view.view_bottom+game_view.window.height-80,
                                            screen_beginning=game_view.view_left+40)
    game_view.window.music_manager.on_draw(screen_height=game_view.view_bottom+game_view.window.height-80,
                                           developer_mode=game_view.window.developer_mode,
                                           screen_beginning=game_view.view_left+40)
    
    
    # draw lanes for bad guy path planning (Debug only)
    for lane in assets.leveldata[game_view.current_level].lanes:
        arcade.draw_line(lane[0], lane[2], lane[1], lane[2], arcade.color.PURPLE, 2)
    

