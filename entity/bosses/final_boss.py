from entity.entity import Entity
from util import Point2D


class FinalBoss(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 0, False, None, 500, 0, True)