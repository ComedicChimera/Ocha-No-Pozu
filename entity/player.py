from entity.entity import GravityEntity
from util import Point2D, WIDTH, PLAYER_SPAWN
from render.sprite import AnimatedSprite, Sprite
from enum import Enum
from audio.sound import am
from random import randint
from entity.projectile import Projectile


class Arrow(Projectile):
    def __init__(self, x, y, facing, player):
        dx = -1 if facing else 1
        super().__init__(Sprite('arrow.png', Point2D(19, 5)), x, y, dx, 0, 20, 15, player)


class Player(GravityEntity):
    class PlayerStates(Enum):
        IDLE = 0
        RUNNING = 1
        SWINGING = 2
        SWING_RUNNING = 3
        SHOOTING = 4

    def __init__(self):
        super().__init__(Point2D(WIDTH / 2, PLAYER_SPAWN + 256), 10, True, 0.3, AnimatedSprite('player_idle.png', Point2D(25, 44), 3, speed=0.25),
                         100, 4)
        self.animation_state = self.PlayerStates.IDLE
        self.fading = False
        self.can_fade = True
        self.swinging = False
        self.can_shoot = True

    def hurt(self, damage):
        if self.invulnerable:
            return
        if self.health - damage > 0:
            am.play_sound('damage.ogg')
            self.health -= damage
        else:
            self.health = 0

    def swing(self):
        if self.swinging:
            return
        am.play_sound('sword_swing_%s.ogg' % randint(1, 2))
        self.animation_state = self.PlayerStates.SWINGING
        self.swinging = True
        self.set_timer('swing', 10, self._reset_swing)
        if not self.flip_horizontal:
            self.position.x -= 25

    def _reset_swing(self):
        self.animation_state = self.PlayerStates.IDLE
        self.swinging = False
        if not self.flip_horizontal:
            self.position.x += 25

    def jump(self):
        if self.force.y_mag == 0:
            self.force.effect(self.force.x_mag, 10 + self._speed_modifier)
            am.play_sound('jump_%d.ogg' % randint(1, 2))

    def move_left(self):
        self.transform(x=-1)
        self.flip_horizontal = True
        if self.swinging:
            self.animation_state = self.PlayerStates.SWING_RUNNING
        else:
            self.animation_state = self.PlayerStates.RUNNING

    def move_right(self):
        self.transform(x=1)
        self.flip_horizontal = False
        if self.swinging:
            self.animation_state = self.PlayerStates.SWING_RUNNING
        else:
            self.animation_state = self.PlayerStates.RUNNING

    def fade(self):
        if not self.can_fade:
            return
        self._speed_modifier = 10
        self.fading = True
        self.invulnerable = True
        self.set_timer('fade', 15, end_event=self._end_fade)
        am.play_sound('fade.ogg')

    def _end_fade(self):
        self._speed_modifier = 0
        self.fading = False
        self.invulnerable = False

        self.can_fade = False
        self.set_timer('fade', 180, self._enable_fade)

    def _enable_fade(self):
        self.can_fade = True

    def animate(self):
        if self.health == 0:
            am.play_sound('death.ogg', volume=0.2)
            self._change_sprite(Sprite('player_dead.png', Point2D(44, 13)))
        elif self.animation_state == self.PlayerStates.SWINGING:
            self._change_sprite(AnimatedSprite('player_swing.png', Point2D(50, 43), 5, speed=0.5))
        elif self.animation_state == self.PlayerStates.SWING_RUNNING:
            self._change_sprite(AnimatedSprite('player_swing_running.png', Point2D(50, 44), 5, speed=0.5))
        elif self.animation_state == self.PlayerStates.SHOOTING:
            self._change_sprite(AnimatedSprite('player_shoot.png', Point2D(32, 44), 5, speed=0.5))
        elif self.force.y_mag != 0:
            self._change_sprite(Sprite('player_midair.png', Point2D(25, 44)))
            am.stop_sound('running_on_grass.ogg')
        elif self.animation_state == self.PlayerStates.RUNNING:
            self._change_sprite(AnimatedSprite('player_running.png', Point2D(25, 44), 7))
            am.play_sound('running_on_grass.ogg')
            self.animation_state = self.PlayerStates.IDLE
        else:
            self._change_sprite(AnimatedSprite('player_idle.png', Point2D(25, 44), 3, speed=0.25))
            am.stop_sound('running_on_grass.ogg')

    def shoot(self):
        if self.can_shoot:
            self.children.append(Arrow(self.position.x + 6.5, self.position.y + 20, self.flip_horizontal, self))
            self.can_shoot = False
            self.set_timer('reset-shoot', 10, self._reset_shoot)
            am.play_sound('arrow.ogg', volume=0.5)
            self.animation_state = self.PlayerStates.SHOOTING

    def _reset_shoot(self):
        self.animation_state = self.PlayerStates.IDLE
        self.can_shoot = True
