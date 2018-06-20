from entity.entity import Entity
from util import Point2D


class Teleporter(Entity):
    def __init__(self, x, y, entity_generator, tile_generator):
        super().__init__(Point2D(x, y), 0, False, None, 1, 0)
        self.entity_generator = entity_generator
        self.tile_generator = tile_generator

    def follow(self):
        return self.entity_generator(), self.tile_generator()
