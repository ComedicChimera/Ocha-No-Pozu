from render.sprite import rm


class Force:
    def __init__(self):
        self.x_mag, self.y_mag = 0, 0
        self.x_mul, self.y_mul = 1, 1

    def effect(self, x, y):
        self.x_mag += x * self.x_mul
        self.y_mag += y * self.y_mul

    def reset_multiplier(self):
        self.x_mul, self.y_mul = 1, 1

    def apply(self, position):
        position.x += self.x_mag
        position.y += self.y_mag
        return position


class Entity:
    def __init__(self, position, speed, sprite):
        self.position = position
        self.speed = speed
        self.force = Force()
        self._sprite = sprite

    def update(self, collisions):
        pass

    def transform(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'x':
                self.position.x += v * self.speed
            elif k == 'y':
                self.position.y += v * self.speed

    def sprite(self, value=None):
        if value:
            rm.unload(self._sprite.path)
            self._sprite = value
        else:
            return self._sprite.get_image()

    def dimensions(self):
        return self._sprite.dimensions


class GravityEntity(Entity):
    def __init__(self, position, speed, gravity, sprite):
        super().__init__(position, speed, sprite)
        self.gravity = gravity

    def update(self, collisions):
        for collision in collisions:
            if collision.position.y <= self.position.y and self.force.y_mag <= 0:
                self.force.reset_multiplier()
                self.force.y_mag = 0
                break
        # instantly fall
        else:
            self.force.effect(0, -self.gravity)

        if self.force.y_mag != 0:
            self.position = self.force.apply(self.position)
            self.force.effect(0, -self.gravity)

            self.force.y_mul += 1

