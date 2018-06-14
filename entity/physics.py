class Force:
    def __init__(self):
        self.x_mag, self.y_mag = 0, 0
        self.x_mul, self.y_mul = 1, 1

    def effect(self, x, y):
        self.x_mag += x * self.x_mul
        self.y_mag += y * self.y_mul

    def apply(self, position):
        position.x += self.x_mag
        position.y += self.y_mag
        return position

    def reset_y(self):
        self.y_mag, self.y_mul = 0, 1

    def reset_x(self):
        self.x_mag, self.x_mul = 0, 1


class Range:
    def __init__(self, mx):
        self.min = 0
        self.max = mx

    def __contains__(self, item):
        return self.min <= item <= self.max

    def set(self, val):
        self.min = val
        self.max = val + self.max


class BoundingBox:
    def __init__(self, x, y, width, height):
        self.left, self.bottom = x, y
        self.right, self.top = x + width, y + height

    def get_property_list(self):
        return {self.left, self.bottom, self.right, self.top}