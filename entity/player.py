from entity.entity import GravityEntity
from util import Point2D, WIDTH, PLAYER_SPAWN
from render.sprite import AnimatedSprite, Sprite
from enum import Enum


class Player(GravityEntity):
    class PlayerStates(Enum):
        IDLE = 0
        RUNNING = 1

    def __init__(self):
        super().__init__(Point2D(WIDTH / 2, PLAYER_SPAWN + 192), 10, True, 0.3, AnimatedSprite('player_idle.png', Point2D(25, 44), 3, speed=0.25))
        self.animation_state = self.PlayerStates.IDLE
        self.fading = False

    def jump(self):
        if self.force.y_mag == 0:
            self.force.effect(self.force.x_mag, 10)

    def move_left(self):
        self.transform(x=-1)
        self.flip_horizontal = True
        self.animation_state = self.PlayerStates.RUNNING

    def move_right(self):
        self.transform(x=1)
        self.flip_horizontal = False
        self.animation_state = self.PlayerStates.RUNNING

    def fade(self):
        self._speed_modifier = 10
        self.fading = True

        self.set_timer(50, end_event=self._end_fade)

    def _end_fade(self):
        self._speed_modifier = 0
        self.fading = False

    def animate(self):
        if self.force.y_mag != 0:
            if self._sprite.path != 'sprites/player_midair.png':
                self._sprite = Sprite('player_midair.png', Point2D(25, 44))
        elif self.animation_state == self.PlayerStates.RUNNING:
            if self._sprite.path != 'sprites/player_running.png':
                self._sprite = AnimatedSprite('player_running.png', Point2D(25, 44), 7)
            self.animation_state = self.PlayerStates.IDLE
        elif self._sprite.path != 'sprites/player_idle.png':
            self._sprite = AnimatedSprite('player_idle.png', Point2D(25, 44), 3, speed=0.25)
