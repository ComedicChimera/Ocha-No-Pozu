from entity.entity import GravityEntity
from util import Point2D, WIDTH, HEIGHT
from render.sprite import AnimatedSprite
from enum import Enum


class Player(GravityEntity):
    class PlayerStates(Enum):
        IDLE = 0
        RUNNING = 1

    def __init__(self):
        super().__init__(Point2D(WIDTH / 2, HEIGHT / 2), 10, True, 0.3, AnimatedSprite('player_idle.png', Point2D(32, 44), 3, speed=0.25))
        self.animation_state = self.PlayerStates.IDLE

    def jump(self):
        if self.force.y_mag == 0:
            self.force.effect(self.force.x_mag, 30)

    def move_left(self):
        self.transform(x=-1)
        self.flip_horizontal = True
        self.animation_state = self.PlayerStates.RUNNING

    def move_right(self):
        self.transform(x=1)
        self.flip_horizontal = False
        self.animation_state = self.PlayerStates.RUNNING

    def animate(self):
        if self.animation_state == self.PlayerStates.RUNNING:
            if self._sprite.path != 'sprites/player_running.png':
                self._sprite = AnimatedSprite('player_running.png', Point2D(32, 44), 7)
            self.animation_state = self.PlayerStates.IDLE
        # will break if i don't have midair sprite
        # elif self.force.y_mag != 0 and self._sprite.path != 'sprites/player_midair.png':
        #     self._sprite = AnimatedSprite('player_midair.png', Point2D(32, 44), 7)
        elif self._sprite.path != 'sprites/player_idle.png':
            self._sprite = AnimatedSprite('player_idle.png', Point2D(32, 44), 3, speed=0.25)

1