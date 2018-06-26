import pygame


class ResourceManager:
    def __init__(self):
        self.loaded = {}

    def load(self, path):
        if path not in self.loaded:
            self.loaded[path] = [pygame.image.load('assets/' + path), 1]
        else:
            self.loaded[path][1] += 1
        return self.loaded[path][0]

    def unload(self, path):
        if not path:
            return
        if path in self.loaded and self.loaded[path][1] == 1:
            self.loaded.pop(path)
        else:
            self.loaded[path][1] -= 1


rm = ResourceManager()


class Sprite:
    def __init__(self, path, dimensions):
        if not path:
            self.path, self._image = None, None
        else:
            self.path = 'sprites/' + path
            self._image = rm.load(self.path)
        self.dimensions = dimensions

    def get_image(self):
        return self._image


class AnimatedSprite(Sprite):
    def __init__(self, path, dimensions, frames, speed=1, reverse=False):
        super().__init__(path, dimensions)
        self.reverse = reverse
        self.animation_counter, self.frames = frames - 1 if self.reverse else 0, frames
        self.animation_speed = speed

    def get_image(self):
        x = int(self.animation_counter) * self.dimensions.x
        cropped_image = pygame.Surface((self.dimensions.x, self.dimensions.y), pygame.SRCALPHA)
        cropped_image.blit(self._image, (0, 0), (x, 0, x + self.dimensions.x, self.dimensions.y))
        if self.reverse:
            if self.animation_counter > 0:
                self.animation_counter -= self.animation_speed
            else:
                self.animation_counter = self.frames - 1
        else:
            if self.animation_counter < self.frames - 1:
                self.animation_counter += self.animation_speed
            else:
                self.animation_counter = 0
        return cropped_image
