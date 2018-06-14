from render.sprite import rm
from entity.physics import Range, Force
from util import MAP_SIZE_X, MAP_SIZE_Y


class Entity:
    def __init__(self, position, speed, collidable, sprite):
        self.position = position
        self.speed = speed
        self.force = Force()
        self.collidable = collidable
        self._sprite = sprite
        self.x_range, self.y_range = Range(MAP_SIZE_X), Range(MAP_SIZE_Y)

        # sprite controls
        self.rotation = 0
        self.flip_horizontal, self.flip_vertical = False, False

    def update(self):
        pass

    def transform(self, **kwargs):
        for k, v in kwargs.items():
            v *= self.speed
            if k == 'x' and self.position.x + v in self.x_range:
                if v > 0 and not self.position.x + self._sprite.dimensions.x + v in self.x_range:
                    return
                self.position.x += v
            elif k == 'y' and self.position.y + v in self.y_range:
                if v > 0 and self.position.y + self._sprite.dimensions.y + v in self.y_range:
                    return
                self.position.y += v

    def sprite(self, value=None):
        if value:
            rm.unload(self._sprite.path)
            self._sprite = value
        else:
            return self._sprite.get_image()

    def dimensions(self):
        return self._sprite.dimensions

    def __del__(self):
        rm.unload(self._sprite.path)


class GravityEntity(Entity):
    def __init__(self, position, speed, collidable, gravity, sprite):
        super().__init__(position, speed, collidable, sprite)
        self.gravity = gravity

    def update(self):
        if self.force.y_mag != 0:
            self.position = self.force.apply(self.position)
            self.force.effect(0, -self.gravity)

            self.force.y_mul += 1
        elif self.position.y > self.y_range.min:
            self.force.effect(0, -self.gravity)

        self._handle_collide()

    def _handle_collide(self):
        # bottom collision
        if self.position.y < self.y_range.min and self.force.y_mag <= 0:
            self.force.reset_y()
            self.position.y = self.y_range.min

        # top collision
        if self.position.y + self._sprite.dimensions.y > self.y_range.max and self.force.y_mag >= 0:
            self.force.y_mag = -self.gravity
            self.position.y = self.y_range.max - self._sprite.dimensions.y

        # left collision
        if self.position.x < self.x_range.min and self.force.x_mag <= 0:
            self.force.reset_x()
            self.position.x = self.x_range.min

        # right collision
        if self.position.x + self._sprite.dimensions.x > self.x_range.max and self.force.x_mag >= 0:
            self.force.reset_x()
            self.position.x = self.x_range.max - self._sprite.dimensions.x





