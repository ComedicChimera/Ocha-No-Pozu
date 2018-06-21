from entity.entity import Entity
from util import Point2D, TILE_SIZE


class Teleporter(Entity):
    def __init__(self, x, y, destination):
        super().__init__(Point2D(x, y), 0, False, None, 1, 0)
        self.destination = destination

    def check_collision(self, position):
        if self.position.x <= position.x <= self.position.x + TILE_SIZE:
            if self.position.y <= position.y <= self.position.y + TILE_SIZE:
                return True
        return False
