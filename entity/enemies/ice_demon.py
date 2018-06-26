from entity.entity import Entity
from util import Point2D
from render.sprite import AnimatedSprite, Sprite
from random import randint


class IceDemon(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 5, False, AnimatedSprite('ice_demon.png', Point2D(32, 64), 4, speed=0.25), 60, 10, enemy=True)
        self._can_teleport = True
        self._invisible = False

    def update(self, player_pos):
        if randint(0, 20) == 0:
            self.teleport()

        if self._invisible:
            self.transform(x=1 if player_pos.x > self.position.x else -1, y=1 if player_pos.y > self.position.y else -1)

        super().update()

    def teleport(self):
        if not self._can_teleport:
            return
        self.invulnerable = True
        self._can_teleport = False
        self._sprite = AnimatedSprite('ice_demon_teleport.png', Point2D(32, 64), 6, speed=0.25)
        self.set_timer('disappear', 16, self._disappear)

    def _disappear(self):
        self._sprite = Sprite(None, Point2D(32, 64))
        self._invisible = True
        self.set_timer('reappear', 50, self._reappear)

    def _reappear(self):
        self._sprite = AnimatedSprite('ice_demon_teleport.png', Point2D(32, 64), 6, speed=0.25, reverse=True)
        self._invisible = False
        self.set_timer('end-teleport', 16, self._end_teleport)

    def _end_teleport(self):
        self._sprite = AnimatedSprite('ice_demon.png', Point2D(32, 64), 4, speed=0.25)
        self.invulnerable = False
        self._can_teleport = True
