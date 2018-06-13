from entity.entity import GravityEntity
from util import Point2D
from render.sprite import AnimatedSprite


class Player(GravityEntity):
    def __init__(self):
        super().__init__(Point2D(0, 0), 20, 0.3, AnimatedSprite('player.png', Point2D(50, 50), 1))

    def jump(self):
        if self.force.y_mag == 0:
            self.force.effect(self.force.x_mag, 30)

    def move_left(self):
        self.transform(x=-1)

    def move_right(self):
        self.transform(x=1)
