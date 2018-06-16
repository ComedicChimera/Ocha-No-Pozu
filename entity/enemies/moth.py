from entity.entity import Entity
from util import Point2D
from render.sprite import AnimatedSprite


class Moth(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 5, True, AnimatedSprite('moth.png', Point2D(64, 64), 8), 60, 20)

    def update_enemy(self, player_pos):
        self.position.x += self.speed if player_pos.x > self.position.x else -self.speed
        self.position.y += self.speed if player_pos.y > self.position.y else -self.speed


