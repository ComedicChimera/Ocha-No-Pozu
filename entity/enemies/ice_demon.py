from entity.entity import Entity
from entity.projectile import Projectile
from util import Point2D
from render.sprite import AnimatedSprite, Sprite
from random import randint


class Icicle(Projectile):
    def __init__(self, x, y, dx, dy, parent):
        super().__init__(AnimatedSprite('icicle.png', Point2D(27, 7), 5), x, y, dx, dy, 5, 60, parent, enemy=True)
        self.set_timer('die', 1000, self._die)
        self._dead = False

    def update(self, player_pos):
        super().update()
        if self._dead:
            return
        dx, dy = player_pos.x - self.position.x, player_pos.y - self.position.y
        self._update_rotation(dx, dy)
        self._flatten_direction(dx, dy)

    def hurt(self, damage):
        if self._dead:
            return
        super().hurt(damage)
        if self.health <= 0:
            self._die()

    def _die(self):
        self.health = 1
        self._change_sprite(AnimatedSprite('icicle_death.png', Point2D(32, 32), 7, speed=0.25))
        self._dead = True
        self.invulnerable = True
        self.damage = 0
        self.set_timer('despawn', 24, self._despawn)

    def _despawn(self):
        self.invulnerable = False
        self.health = 0


class IceDemon(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 5, False, AnimatedSprite('ice_demon.png', Point2D(32, 64), 4, speed=0.25), 60, 10, enemy=True)
        self._can_teleport = True
        self._invisible = False
        self._can_fire = True

    def update(self, player_pos):
        if randint(0, 20) == 0:
            self.teleport()

        if self._invisible:
            self.transform(x=1 if player_pos.x > self.position.x else -1, y=1 if player_pos.y > self.position.y else -1)
        elif randint(0, 10) == 0:
            self._fire()

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

    def _fire(self):
        if not self._can_fire:
            return
        # dx dy is updated dynamically
        self.children.append(Icicle(self.position.x, self.position.y, 0, 0, self))
        self._can_fire = False
        self.set_timer('reset-fire', 50, self._reset_fire)

    def _reset_fire(self):
        self._can_fire = True
