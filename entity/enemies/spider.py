from entity.entity import GravityEntity
from render.sprite import AnimatedSprite, Sprite
from random import randint
from util import Point2D


class Spider(GravityEntity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 8, False, 0.3, AnimatedSprite('spider_idle.png', Point2D(32, 32), 2, speed=0.25), 50, 20, enemy=True)
        self._midair = False

    def update(self, player_pos):
        if self.force.y_mag != 0:
            self._midair = True
            self._change_sprite(Sprite('spider_midair.png', Point2D(32, 32)))
            self.transform(x=1 if player_pos.x > self.position.x else -1, y=1 if player_pos.y > self.position.y else -1)
        else:
            self._change_sprite(AnimatedSprite('spider_idle.png', Point2D(32, 32), 2, speed=0.25))
            self.should_damage = False
            if randint(0, 10) == 0:
                self._jump()

        super().update()

    def _jump(self):
        self.force.effect(0, 40)
        self.should_damage = True

