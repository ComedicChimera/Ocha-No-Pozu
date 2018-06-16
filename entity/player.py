from entity.entity import GravityEntity
from util import Point2D, WIDTH, PLAYER_SPAWN
from render.sprite import AnimatedSprite, Sprite
from enum import Enum
from audio.sound import am


class Player(GravityEntity):
    class PlayerStates(Enum):
        IDLE = 0
        RUNNING = 1

    def __init__(self):
        super().__init__(Point2D(WIDTH / 2, PLAYER_SPAWN + 192), 10, True, 0.3, AnimatedSprite('player_idle.png', Point2D(25, 44), 3, speed=0.25),
                         100)
        self.animation_state = self.PlayerStates.IDLE
        self.fading = False
        self.can_fade = True

    def jump(self):
        if self.force.y_mag == 0:
            self.force.effect(self.force.x_mag, 10 + self._speed_modifier)

    def move_left(self):
        self.transform(x=-1)
        self.flip_horizontal = True
        self.animation_state = self.PlayerStates.RUNNING

    def move_right(self):
        self.transform(x=1)
        self.flip_horizontal = False
        self.animation_state = self.PlayerStates.RUNNING

    def fade(self):
        if not self.can_fade:
            return
        self._speed_modifier = 10
        self.fading = True
        self.invulnerable = True
        self.set_timer(15, end_event=self._end_fade)

    def _end_fade(self):
        self._speed_modifier = 0
        self.fading = False
        self.invulnerable = False

        self.can_fade = False
        self.set_timer(180, self._enable_fade)

    def _enable_fade(self):
        self.can_fade = True

    def animate(self):
        if self.force.y_mag != 0:
            self._change_sprite(Sprite('player_midair.png', Point2D(25, 44)))
            am.stop_sound('running.ogg')
        elif self.animation_state == self.PlayerStates.RUNNING:
            self._change_sprite(AnimatedSprite('player_running.png', Point2D(25, 44), 7))
            am.play_sound('running.ogg')
            self.animation_state = self.PlayerStates.IDLE
        else:
            self._change_sprite(AnimatedSprite('player_idle.png', Point2D(25, 44), 3, speed=0.25))
            am.stop_sound('running.ogg')
