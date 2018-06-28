from entity.entity import Entity
from util import Point2D, TILE_SIZE, WIDTH
from render.sprite import AnimatedSprite
from entity.enemies.moth import Moth
from entity.enemies.ice_demon import Icicle
from entity.enemies.fire_skull import Fireball
from random import randint
from entity.heart import Heart
from audio.sound import am


class DeathField(Entity):
    def __init__(self, x):
        super().__init__(Point2D(x, 0), 0, False, AnimatedSprite('death_field.png', Point2D(144, 480), 7), 1, 100, False)
        self.time_alive = 0

    def update(self, *args):
        if self.time_alive < 50:
            self.time_alive += 1
        else:
            self.health = 0


class FinalBoss(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 0, False, AnimatedSprite('final_boss.png', Point2D(144, 108), 32, speed=0.25), 400, 0, True)
        self.y_offset = 0
        self.start_y = y
        self.downward = False
        self._spawned_moths = 0
        self.phase = 2
        self._spawned_fire_balls = 0
        self._spawned_icicles = 0
        self._teleported = 0
        self._can_teleport = True
        self._set_phase_5_timer = False
        self._can_shoot = True

    def update(self, player_pos, entities):
        super().update()

        if len(self.children) != 0:
            return
        if self.phase == 0:
            if self._spawned_moths < 2 and randint(0, 40) == 0:
                self.children.append(Moth(self.position.x, self.position.y))
                self._spawned_moths += 1
            elif self._spawned_moths > 1 and len([x for x in entities if isinstance(x, Moth)]) == 0:
                self.children.extend([
                    Icicle(self.position.x, self.position.y, 0, 0, self),
                    Icicle(self.position.x + 72, self.position.y, 0, 0, self),
                    Icicle(self.position.x + 144, self.position.y, 0, 0, self)])
                self.phase = 1
        elif self.phase == 1:
            if len([x for x in entities if isinstance(x, Icicle)]) == 0:
                self.phase = 2
        elif self.phase == 2:
            self._spawn_fire_ball()
            self.phase = 3
        elif self.phase == 4:
            if len([x for x in entities if isinstance(x, Heart)]) == 0 and not self._set_phase_5_timer:
                print('progressing for some reason')
                self.set_timer('progress-5', 30, self._set_to_5)
                self._set_phase_5_timer = True
        elif self.phase == 5:
            if self._can_teleport and randint(0, 5) == 0:
                self._teleport(player_pos)
        elif self.phase == 6:
            self._spawn_icicle()
            self.phase = 7
        elif self.phase == 8:
            if len([x for x in entities if isinstance(x, Heart)]) == 0:
                self.phase = 9
        elif self.phase == 9:
            if self.position.y > TILE_SIZE * 2:
                self.position.y -= 1
            else:
                self.phase = 10
            return
        elif self.phase == 10:
            if self.health < 50:
                self.invulnerable = True
                self.phase = 11
            elif self._can_shoot:
                self._shoot_fireball(player_pos)
            return
        elif self.phase == 11:
            self._change_sprite(AnimatedSprite('final_boss_death.png', Point2D(144, 108), 8, speed=0.25))
            self.set_timer('death-timer', 24, self._die)
            self.phase = 12
            return
        else:
            return

        self.position.y = self.start_y + self.y_offset

        if abs(self.y_offset) > 16:
            self.downward = not self.downward
        if self.downward:
            self.y_offset -= 0.25
        else:
            self.y_offset += 0.25

    def _spawn_fire_ball(self):
        if self._spawned_fire_balls < 15:
            if randint(0, 1) == 0:
                f_ball = Fireball(1, TILE_SIZE + 1, 1, 0, self)
            else:
                f_ball = Fireball(639 - TILE_SIZE, TILE_SIZE + 1, -1, 0, self)
            f_ball.speed = 10
            f_ball.enemy = False
            self.children.append(f_ball)
            self._spawned_fire_balls += 1
            self.set_timer('spawn-fire-ball', 50, self._spawn_fire_ball)
        else:
            self.phase = 4
            self.children.append(Heart(WIDTH // 2 - 16, TILE_SIZE * 2, 100))

    def _spawn_icicle(self):
        if self._spawned_icicles < 15:
            self.children.append(Icicle(randint(20, 620), 300, 0, 0, self))
            self._spawned_icicles += 1
            self.set_timer('spawn-icicle', 50, self._spawn_icicle)
        else:
            self.phase = 8
            self.children.append(Heart(WIDTH // 2 - 16, TILE_SIZE * 2, 100))

    def _teleport(self, player_pos):
        am.play_sound('death_field.ogg', volume=0.2)
        self._can_teleport = False
        self.children.append(DeathField(self.position.x))
        self._teleported += 1
        self.set_timer('set-respawn', 50, lambda: self._move(player_pos))

    def _move(self, player_pos):
        if self._teleported > 15:
            self.position.x = WIDTH // 2 - 72
        elif player_pos.x - 72 < 1:
            self.position.x = 1
        elif player_pos.x - 72 > 572:
            self.position.x = 572
        else:
            self.position.x = player_pos.x - 72
        self._change_sprite(AnimatedSprite('final_boss_teleport.png', Point2D(144, 108), 7, speed=0.5))
        self.set_timer('reset', 14, self._reset)

    def _reset(self):
        self._change_sprite(AnimatedSprite('final_boss.png', Point2D(144, 108), 32, speed=0.25))
        if self._teleported > 15:
            self.phase = 6
        else:
            self._can_teleport = True

    def _set_to_5(self):
        self.phase = 5

    def _shoot_fireball(self, player_pos):
        dx = -1 if player_pos.x < self.position.x else 1
        f_ball = Fireball(self.position.x + 72, TILE_SIZE + 10, dx, 0, self)
        f_ball.speed = 10
        f_ball.enemy = False
        self.children.append(f_ball)
        self._can_shoot = False
        self.set_timer('shoot_again', 50, self._reset_shoot)

    def _reset_shoot(self):
        self._can_shoot = True

    def _die(self):
        self.health = 0

