from util import Point2D


class Tile:
    def __init__(self, x, y, sprite_x, sprite_y, repeat_x=1, repeat_y=1, collidable=True):
        self.position = Point2D(x, y)
        self.sprite_x, self.sprite_y = sprite_x, sprite_y
        self.repeat_x, self.repeat_y = repeat_x, repeat_y
        self.collidable = collidable


class TileSet:
    GRASS = (0, 0)
    DIRT = (1, 0)
    STONE = (2, 0)
    SNOW = (3, 0)
    SNOW_GRASS = (4, 0)
    SNOW_STONE = (5, 0)

