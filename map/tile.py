from util import Point2D
from render.sprite import rm


class Tile:
    def __init__(self, x, y, sprite_x, sprite_y, repeat_x=1, repeat_y=1, collidable=True, damage=0):
        self.position = Point2D(x, y)
        self.sprite_x, self.sprite_y = sprite_x, sprite_y
        self.repeat_x, self.repeat_y = repeat_x, repeat_y
        self.collidable = collidable
        self.damage = damage


class SpriteTile:
    def __init__(self, path, x, y, width, height, collidable=False, damage=0):
        self.sprite = rm.load('sprites/' + path)
        self.position = Point2D(x, y)
        self.dimensions = Point2D(width, height)
        self.collidable = collidable
        self.damage = 0


class TileSet:
    GRASS_SURFACE = (0, 0)
    GRASS = (1, 0)
    DIRT = (2, 0)
    STONE = (3, 0)
    CRACKED_STONE = (4, 0)
    MOSS_STONE = (5, 0)
    SNOW = (6, 0)
    SNOW_GRASS = (7, 0)
    SNOW_STONE = (8, 0)
    STALACTITE = (9, 0)
    STALAGMITE = (10, 0)
    SPIKES = (11, 0)
    WATER = (12, 0)

