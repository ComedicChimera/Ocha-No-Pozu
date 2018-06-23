from entity.entity import Entity
from util import Point2D
from render.sprite import AnimatedSprite
from random import randint
from entity.projectile import Projectile


class Fireball(Projectile):
    def __init__(self, x, y, dx, dy, parent):
        super().__init__(AnimatedSprite('fire_ball.png', Point2D(32, 32), 3), x, y, dx, dy, 20, 50, parent)


class FireSkull(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 3, False, AnimatedSprite('fire_skull.png', Point2D(32, 50), 11, speed=0.25), 100, 0, enemy=True)
        self._can_fire = True

    def update(self, player_pos):
        x_trans, y_trans = player_pos.x - self.position.x, player_pos.y - self.position.y
        x, y = -1 if x_trans < 0 else 1, -1 if y_trans < 0 else 1
        x, y = 0 if x_trans == 1 else x, 0 if y_trans == 1 else y
        x, y = x if abs(x_trans) > 64 else 0, y if abs(y_trans) > 64 else 0

        if randint(0, 15) == 0:
            self.fire(x_trans, y_trans)

        if x < 0:
            self.flip_horizontal = True
        elif x > 0:
            self.flip_horizontal = False
        self.transform(x=x, y=y)
        super().update()

    def fire(self, dx, dy):
        if not self._can_fire:
            return
        self.children.append(Fireball(self.position.x + 16, self.position.y + 25, dx, dy, self))
        self._can_fire = False
        self.set_timer('reset-fire', 15, self._restore_fire)

    def _restore_fire(self):
        self._can_fire = True
