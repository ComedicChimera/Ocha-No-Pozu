WIDTH = 640
HEIGHT = 480


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)
