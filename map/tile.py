class Tile:
    def __init__(self, position, sprite_x, sprite_y, repeat_x=1, repeat_y=1, collidable=True):
        self.position = position
        self.sprite_x, self.sprite_y = sprite_x, sprite_y
        self.repeat_x, self.repeat_y = repeat_x, repeat_y
        self.collidable = collidable


class TileSet:
    DIRT = (0, 0)
    GRASS = (0, 1)

