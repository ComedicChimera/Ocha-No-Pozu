from entity.physics import Range
from entity.entity import Entity
from map.tile import SpriteTile
from util import Point2D, TILE_SIZE
import render.draw as draw
from pygame import BLEND_RGBA_MULT


class Window:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.x_range, self.y_range = Range(self.width), Range(self.height)
        self.offset = [0, 0]

    def set_window_offset(self, x=0, y=0):
        self.x_range.set(-x)
        self.y_range.set(y)
        self.offset[0] = x
        self.offset[1] = y

    def shift_position(self, position):
        position.x += self.offset[0]
        position.y += self.offset[1]

    def clip_objects(self, entities, tiles):
        def check(a, b, rng):
            if a in rng or b in rng:
                return True
            elif a <= rng.min and b >= rng.max:
                return True
            return False

        objects = []
        for obj in entities + tiles:
            if check(obj.position.x, obj.position.x + self._dimensions(obj).x, self.x_range):
                if check(obj.position.y, obj.position.y + self._dimensions(obj).y, self.y_range):
                    objects.append(obj)
        return objects

    def draw_gui_element(self, element):
        self.blit(element.get_image(), (element.position.x, element.position.y))

    @staticmethod
    def _dimensions(obj):
        if isinstance(obj, Entity):
            return obj.dimensions()
        elif isinstance(obj, SpriteTile):
            return Point2D(obj.dimensions.x, obj.dimensions.y)
        else:
            return Point2D(TILE_SIZE * obj.repeat_x, TILE_SIZE * obj.repeat_y)

    def draw_entity(self, entity):
        self.screen = draw.draw_entity(self.screen, entity, self.offset)

    def draw_tile(self, tile):
        self.screen = draw.draw_tile(self.screen, tile, self.offset)

    def blit(self, source, dest, area=None, special_flags=0):
        self.screen.blit(source, dest, area, special_flags)

    def draw_overlay(self, o, opacity=100):
        if isinstance(o, tuple):
            self.screen.fill((*o, opacity), None, BLEND_RGBA_MULT)
        else:
            image = o.convert_alpha()
            image.fill((255, 255, 255, opacity), None, BLEND_RGBA_MULT)
            self.blit(image, (0, 0))

    def clear(self, color):
        self.screen.fill(color)
