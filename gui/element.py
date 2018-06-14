from util import Point2D


class GUIElement:
    def __init__(self, x, y, width, height):
        self.position = Point2D(x, y)
        self.dimensions = Point2D(width, height)

    def update(self):
        pass
