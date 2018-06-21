import pygame
from util import WIDTH, HEIGHT, TILE_SIZE


circle_filter = pygame.image.load('assets/light.png')


class Light:
    def __init__(self, x, y, width, height, color=None, spread=4):
        self.x, self.y = x, y
        self.width, self.height = width, height
        color = tuple(map(lambda v: 255 - v, color)) if color else None
        if color:
            self.filter = _colorize(pygame.transform.scale(circle_filter, (spread * TILE_SIZE, spread * TILE_SIZE)), color)
        else:
            self.filter = pygame.transform.scale(circle_filter, (spread * TILE_SIZE, spread * TILE_SIZE))

    def draw_light(self, gloom, offset):
        for px in range(self.width):
            for py in range(self.height):
                gloom.blit(self.filter, (self.x + offset[0] + px, self.y + offset[1] + py))
        return gloom


def _colorize(surface, color):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), (*color, a))
    return surface


def render_lights(window, lights, offset):
    gloom = pygame.Surface((WIDTH, HEIGHT))
    gloom.fill((60, 60, 60))
    for light in lights:
        gloom = light.draw_light(gloom, offset)
    window.blit(gloom, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return window
