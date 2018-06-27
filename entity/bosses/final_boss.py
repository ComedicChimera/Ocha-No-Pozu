from entity.entity import Entity
from util import Point2D, TILE_SIZE, WIDTH
from render.sprite import AnimatedSprite
from entity.enemies.moth import Moth
from entity.enemies.ice_demon import Icicle
from entity.enemies.fire_skull import Fireball
from random import randint
from entity.heart import Heart


class FinalBoss(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 0, False, AnimatedSprite('final_boss.png', Point2D(144, 108), 32, speed=0.25), 500, 0, True)
        self.y_offset = 0
        self.start_y = y
        self.downward = False
        self.spawned_moths = 0
        self.phase = 0
        self._spawned_fire_balls = 0

    def update(self, player_pos, entities):
        if self.phase == 0:
            if self.spawned_moths < 2 and randint(0, 40) == 0:
                self.children.append(Moth(self.position.x, self.position.y))
                self.spawned_moths += 1
            elif self.spawned_moths > 1 and len([x for x in entities if isinstance(x, Moth)]) == 0:
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

        self.position.y = self.start_y + self.y_offset

        super().update()
        if abs(self.y_offset) > 16:
            self.downward = not self.downward
        if self.downward:
            self.y_offset -= 0.25
        else:
            self.y_offset += 0.25

    def _spawn_fire_ball(self):
        if self._spawned_fire_balls < 20:
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
