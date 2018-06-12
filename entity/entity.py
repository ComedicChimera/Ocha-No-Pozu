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


class Entity:
    def __init__(self, position, speed, force):
        self.position = position
        self.speed = speed
        self.force = force

    def update(self, collisions):
        pass


class GravityEntity(Entity):
    def __init__(self, position, speed, force, gravity):
        super().__init__(position, speed, force)
        self.gravity = gravity

    def update(self, collisions):
        for collision in collisions:
            if collision.position.y < self.position.y:
                self.force.reset_multiplier()
                self.force.y_mag = 0
                break
        else:
            self.force.effect(0, -self.gravity)

        if self.force.y_mag != 0:
            self.position = self.force.apply(self.position)

            self.force.y_mul += 1


entities = []
