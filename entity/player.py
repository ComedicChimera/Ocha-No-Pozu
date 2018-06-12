from entity.entity import GravityEntity
from util import Point2D
from render.sprite import AnimatedSprite


class Player(GravityEntity):
    def __init__(self):
        # TODO change to use actual sprite
        super().__init__(Point2D(0, 0), 20, 0.3, AnimatedSprite('player.png', Point2D(0, 0), 1))

    def jump(self):
        self.force.effect(0, 30)

    def move_left(self):
        self.transform(x=-1)

    def move_right(self):
        self.transform(x=1)
