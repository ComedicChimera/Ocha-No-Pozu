from PIL import Image
import pygame


class ResourceManager:
    def __init__(self):
        self.loaded = {}

    def load(self, path):
        if path not in self.loaded:
            with open('assets/' + path) as file:
                self.loaded[path] = (file, 1)
        else:
            self.loaded[path][1] += 1
        return self.loaded[path][0]

    def unload(self, path):
        if path in self.loaded and self.loaded[path][1] == 1:
            self.loaded.pop(path)


rm = ResourceManager()


class Sprite:
    def __init__(self, path, dimensions):
        self.path = 'sprites/' + path
        self._image = rm.load(self.path)
        self.dimensions = dimensions

    def get_image(self):
        return pygame.image.load(self._image)

    def __del__(self):
        rm.unload(self.path)


class AnimatedSprite(Sprite):
    def __init__(self, path, dimensions, frames):
        super().__init__(path, dimensions)
        self._image = Image.open(self._image)
        self.animation_counter, self.frames = 0, frames

    def get_image(self):
        x = self.animation_counter * self.dimensions.x
        cropped_image = self._image.crop((x, 0, x + self.dimensions.x, self.dimensions.y))
        if self.animation_counter < self.frames:
            self.animation_counter += 1
        else:
            self.animation_counter = 0
        return pygame.image.fromstring(cropped_image.to_bytes(), cropped_image.size, cropped_image.mode)
