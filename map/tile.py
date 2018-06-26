from util import Point2D
from render.sprite import rm
from pygame import Surface, SRCALPHA


class Tile:
    def __init__(self, x, y, sprite_x, sprite_y, repeat_x=1, repeat_y=1, collidable=True, damage=0, render_first=False):
        self.position = Point2D(x, y)
        self.sprite_x, self.sprite_y = sprite_x, sprite_y
        self.repeat_x, self.repeat_y = repeat_x, repeat_y
        self.collidable = collidable
        self.damage = damage
        self.render_first = render_first


class SpriteTile:
    def __init__(self, path, x, y, width, height, collidable=False, damage=0, frames=1, speed=0.25, render_first=False):
        self._path = 'sprites/' + path
        self._sprite = rm.load(self._path)
        self.frames = frames
        self.position = Point2D(x, y)
        self.dimensions = Point2D(width, height)
        self.collidable = collidable
        self.damage = damage
        self._animation_counter = 0
        self._animation_speed = speed
        self.render_first= render_first

    def sprite(self):
        if self.frames == 1:
            return self._sprite
        else:
            if self._animation_counter < self.frames - 1:
                self._animation_counter += self._animation_speed
            else:
                self._animation_counter = 0

            x = int(self._animation_counter) * self.dimensions.x
            cropped_image = Surface((self.dimensions.x, self.dimensions.y), SRCALPHA)
            cropped_image.blit(self._sprite, (0, 0), (x, 0, x + self.dimensions.x, self.dimensions.y))
            return cropped_image

    def __del__(self):
        rm.unload(self._path)


class TileSet:
    GRASS_SURFACE = (0, 0)
    GRASS = (1, 0)
    DIRT = (2, 0)
    STONE = (3, 0)
    CRACKED_STONE = (4, 0)
    MOSS_STONE = (5, 0)
    SNOW = (6, 0)
    SNOW_GRASS = (0, 1)
    SNOW_STONE = (1, 1)
    STALACTITE = (2, 1)
    STALAGMITE = (3, 1)
    SPIKES = (4, 1)
    WATER = (5, 1)
    PINK_FLOWER = (6, 1)
    YELLOW_FLOWER = (0, 2)
    BOULDER = (1, 2)
    SHORT_LOG = (2, 2)
    SHORT_MOSSY_LOG = (3, 2)
    LOG = (4, 2)
    MOSSY_LOG = (5, 2)
    LAVA = (6, 2)
    ICE = (0, 3)
    ICE_ROCK = (1, 3)
    ICE_STALACTITE = (2, 3)
    ICE_STALAGMITE = (3, 3)
    GLOOM_STONE = (4, 3)
    BRICKS = (2, 4)
