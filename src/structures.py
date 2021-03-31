"""
structures.py

Place for Structures class (big static world objects)
"""

# --- Import external modules ---
import arcade
import pymunk
# --- Import internal classes ---
import data
import assets

import math
import random

import PIL.Image
import PIL.ImageDraw

from arcade.texture import Texture

# --- Constants ---
settings = data.load_settings()
SCREEN_WIDTH = int(settings['VIDEO']['WINDOW_WIDTH'])

def make_polyrock_texture(vertices,name,type):
    """
    Return a Texture of a rock from arbitrary poly
    """
    bg_color = (0, 0, 0, 0)  # fully transparent
    minx = min([v[0] for v in vertices])
    miny = min([v[1] for v in vertices])
    maxx = max([v[0] for v in vertices])
    maxy = max([v[1] for v in vertices])
    res_x = int(maxx-minx)
    res_y = int(maxy-miny)
    center = [minx+res_x/2,miny+res_y/2]
    
    textimg = PIL.Image.new("RGBA", (res_x, res_y), bg_color)
    if type == 'rock':
        texture = assets.structure_textures['asteroid'].image
        outline_colour = (127,127,127)
    else:
        texture = assets.structure_textures['asteroid'].image
        outline_colour = (127,127,127)
    width, height = texture.size
    for i in range(math.ceil(res_x/width)):
        for j in range(math.ceil(res_y/height)):
            textimg.paste(texture, (i*width, j*height))
    
    img = PIL.Image.new("RGBA", (res_x, res_y), bg_color)
    draw = PIL.ImageDraw.Draw(img)
    draw.polygon([(v[0]-minx,res_y-(v[1]-miny)) for v in vertices], fill=(255,255,255,255))
    img.paste(textimg, (0,0), img)
    draw.line([(v[0]-minx,res_y-(v[1]-miny)) for v in vertices]+[(vertices[0][0]-minx,res_y-(vertices[0][1]-miny))], fill=outline_colour, width=10)
    # name must be unique for caching
    return (Texture(name, img), center)

class Structure(arcade.Sprite):
    """ Structure """

    def __init__(self, parent, space, verticies, name, type='rock'):
        super().__init__()
        
        self.parent = parent
        self.space = space
        self.type = type
        
        # create static pymunk bodies for walls
        for i in range(len(verticies)):
            v1 = verticies[i]
            if i < (len(verticies)-1):
                v2 = verticies[i+1]
            else:
                v2 = verticies[0]
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, v1, v2, 0.0)
            shape.elasticity = 0.99
            shape.friction = 1
            shape.collision_type = 3
            self.space.add(shape, body)
        
        # Create texture/set sprite
        (self.texture, position) = make_polyrock_texture(verticies, name, type)
        self.center_x = position[0]
        self.center_y = position[1]
