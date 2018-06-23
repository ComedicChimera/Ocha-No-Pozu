from entity.entity import Entity
from util import Point2D
import math


class Projectile(Entity):
    def __init__(self, sprite, x, y, dx, dy, speed, damage, parent):
        super().__init__(Point2D(x, y), speed, False, sprite, 1, damage)
        self.dx, self.dy = dx // self.speed, dy // self.speed
        rx, ry = abs(dx), abs(dy)
        if dx < 0 and dy < 0:
            self.rotation = math.atan(ry/rx)
        elif dx < 0:
            self.rotation = math.tau - math.atan(ry/rx)
        elif dy < 0:
            self.rotation = math.pi + math.atan(ry/rx)
        else:
            self.rotation = math.pi / 2 + math.atan(rx/ry)
        self.rotation = math.degrees(self.rotation)
        self.parent = parent

    def update(self):
        self.position.x += self.dx
        self.position.y += self.dy
