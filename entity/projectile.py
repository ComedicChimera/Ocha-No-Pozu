from entity.entity import Entity
from util import Point2D
import math


class Projectile(Entity):
    def __init__(self, sprite, x, y, dx, dy, speed, damage, parent, enemy=False):
        super().__init__(Point2D(x, y), speed, False, sprite, 1, damage, enemy=enemy)
        self._update_rotation(dx, dy)
        # 0 out dx and dy
        self.dx, self.dy = 0, 0,
        self._flatten_direction(dx, dy)
        self.parent = parent

    def _update_rotation(self, dx, dy):
        rx, ry = abs(dx), abs(dy)
        rx, ry = 0.1 if rx == 0 else rx, 0.1 if ry == 0 else ry
        if dx < 0 and dy < 0:
            self.rotation = math.atan(ry / rx)
        elif dx < 0:
            self.rotation = math.tau - math.atan(ry / rx)
        elif dy < 0:
            self.rotation = math.pi - math.atan(ry / rx)
        else:
            self.rotation = math.pi + math.atan(ry / rx)
        self.rotation = math.degrees(self.rotation)

    def _flatten_direction(self, dx, dy):
        if dx == 0:
            self.dx = 0
        else:
            self.dx = -1 if dx < 0 else 1
        if dy == 0:
            self.dy = 0
        else:
            self.dy = -1 if dy < 0 else 1

    def update(self, *args):
        self.position.x += self.dx * self.speed
        self.position.y += self.dy * self.speed
        prev_pos = (self.position.x, self.position.y)
        super().update()
        if (self.position.x, self.position.y) != prev_pos:
            self.hurt(self.max_health)
