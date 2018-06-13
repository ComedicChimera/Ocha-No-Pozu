import pygame


class ResourceManager:
    def __init__(self):
        self.loaded = {}

    def load(self, path):
        if path not in self.loaded:
            self.loaded[path] = (pygame.image.load('assets/' + path), 1)
        else:
            self.loaded[path][1] += 1
        return self.loaded[path][0]

    def unload(self, path):
        if path in self.loaded and self.loaded[path][1] == 1:
            self.loaded.pop(path)
        else:
            self.loaded[path][1] -= 1


rm = ResourceManager()


class Sprite:
    def __init__(self, path, dimensions):
        self.path = 'sprites/' + path
        self._image = rm.load(self.path)
        self.dimensions = dimensions
        self.rotation = 0
        self.flip_horizontal, self.flip_vertical = False

    def get_image(self):
        return self._image

    def __del__(self):
        rm.unload(self.path)


class AnimatedSprite(Sprite):
    def __init__(self, path, dimensions, frames):
        super().__init__(path, dimensions)
        self.animation_counter, self.frames = 0, frames

    def get_image(self):
        x = int(self.animation_counter) * self.dimensions.x
        cropped_image = pygame.Surface((self.dimensions.x, self.dimensions.y))
        cropped_image.blit(self._image, (0, 0), (x, 0, x + self.dimensions.x, self.dimensions.y))
        if self.animation_counter < self.frames - 1:
            self.animation_counter += 0.5
        else:
            self.animation_counter = 0
        return cropped_image
