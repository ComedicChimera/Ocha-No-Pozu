from entity.entity import Entity
from util import Point2D
from render.sprite import AnimatedSprite


class Heart(Entity):
    def __init__(self, x, y, healing):
        super().__init__(Point2D(x, y), 0, False, AnimatedSprite('heart.png', Point2D(32, 32), 7, speed=0.25), 1, 0)
        self.healing = healing
