from entity.physics import Range
from entity.entity import Entity
from util import Point2D, TILE_SIZE


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x_range, self.y_range = Range(self.width), Range(self.height)
        self.offset = [0, 0]

    def set_window_offset(self, x=0, y=0):
        self.x_range.set(x)
        self.y_range.set(y)
        self.offset[0] = x
        self.offset[1] = y

    def crop_window(self, entities, tiles):
        objects = []
        for obj in entities + tiles:
            if obj.position.x in self.x_range or obj.position.x + self._dimensions(obj).x in self.x_range:
                objects.append(obj)
            elif obj.position.y in self.y_range or obj.position.y + self._dimensions(obj).y in self.y_range:
                objects.append(obj)
        return objects

    def shift_position(self, position):
        position.x += self.offset[0]
        position.y += self.offset[1]

    @staticmethod
    def _dimensions(obj):
        if isinstance(obj, Entity):
            return obj.dimensions()
        else:
            return Point2D(TILE_SIZE * obj.repeat_x, TILE_SIZE * obj.repeat_y)
