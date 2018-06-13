class Tile:
    def __init__(self, x, y, repeat_x=1, repeat_y=1, collidable=True):
        self.x, self.y = x, y
        self.repeat_x, self.repeat_y = repeat_x, repeat_y
        self.collidable = collidable
