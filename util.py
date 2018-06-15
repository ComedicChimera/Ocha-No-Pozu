WIDTH, HEIGHT = 640, 480

MAP_SIZE_X, MAP_SIZE_Y = 2560, 960

TILE_SIZE = 32

PLAYER_SPAWN = 96


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)
