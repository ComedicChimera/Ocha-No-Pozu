from render.sprite import rm
from entity.physics import Range, Force
from util import MAP_SIZE_X, MAP_SIZE_Y


class Entity:
    def __init__(self, position, speed, collidable, sprite, health, damage, enemy=False):
        self.position = position
        self.speed = speed
        self.force = Force()
        self.collidable = collidable
        self._sprite = sprite
        self.x_range, self.y_range = Range(MAP_SIZE_X), Range(MAP_SIZE_Y)
        self.timers = {}
        self._speed_modifier = 0
        self.invulnerable = False
        self.health = health
        self.max_health = health

        self.damage = damage
        self.should_damage = True

        # sprite controls
        self.rotation = 0
        self.flip_horizontal, self.flip_vertical = False, False

        # is enemy
        self.enemy = enemy

    def update(self, *args):
        remove_keys = []
        end_events = []
        for k, v in self.timers.items():
            if v[0] > 0:
                self.timers[k][0] -= 1
            else:
                remove_keys.append(k)
                end_events.append(v[1])
        for key, func in zip(remove_keys, end_events):
            self.timers.pop(key)
            func()
        self._handle_collide()

    def transform(self, **kwargs):
        for k, v in kwargs.items():
            v *= self.speed + self._speed_modifier
            if k == 'x' and self.position.x + v in self.x_range:
                if v > 0 and not self.position.x + self._sprite.dimensions.x + v in self.x_range:
                    return
                self.position.x += v
            elif k == 'y' and self.position.y + v in self.y_range:
                if v > 0 and not self.position.y + self._sprite.dimensions.y + v in self.y_range:
                    return
                self.position.y += v

    def sprite(self, value=None):
        if not self._sprite:
            return
        if value:
            self._change_sprite(value)
        else:
            return self._sprite.get_image()

    def dimensions(self):
        return self._sprite.dimensions

    def set_timer(self, timer_name, timer_frames, end_event):
        self.timers[timer_name] = [timer_frames, end_event]

    def _handle_collide(self):
        # bottom collision
        if self.position.y < self.y_range.min and self.force.y_mag <= 0:
            self.force.reset_y()
            self.position.y = self.y_range.min

        # top collision
        if self.position.y + self._sprite.dimensions.y > self.y_range.max and self.force.y_mag >= 0:
            self._compute_top_collision()

        # left collision
        if self.position.x < self.x_range.min and self.force.x_mag <= 0:
            self.force.reset_x()
            self.position.x = self.x_range.min

        # right collision
        if self.position.x + self._sprite.dimensions.x > self.x_range.max and self.force.x_mag >= 0:
            self.force.reset_x()
            self.position.x = self.x_range.max - self._sprite.dimensions.x

    # to allow gravity entity to overload the physics engine
    def _compute_top_collision(self):
        self.force.reset_y()
        self.position.y = self.y_range.max - self._sprite.dimensions.y

    def _change_sprite(self, sprite):
        if self._sprite.path == sprite.path:
            return
        rm.unload(self._sprite.path)
        self._sprite = sprite

    def reset_damage(self):
        self.should_damage = True

    def hurt(self, damage):
        if self.invulnerable:
            return
        if self.health - damage > 0:
            self.health -= damage
        else:
            self.health = 0

    # to be overloaded
    def animate(self):
        pass

    def __del__(self):
        if self._sprite:
            rm.unload(self._sprite.path)


class GravityEntity(Entity):
    def __init__(self, position, speed, collidable, gravity, sprite, health, damage):
        super().__init__(position, speed, collidable, sprite, health, damage)
        self.gravity = gravity

    def update(self, *args):
        if self.force.y_mag != 0:
            self.position = self.force.apply(self.position)
            self.force.effect(0, -self.gravity)

            self.force.y_mul += 1
        elif self.position.y > self.y_range.min:
            self.force.effect(0, -self.gravity)

        super().update()

    def _compute_top_collision(self):
        self.force.y_mag = -self.gravity
        self.position.y = self.y_range.max - self._sprite.dimensions.y




