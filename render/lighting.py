import pygame
from util import WIDTH, HEIGHT


circle_filter = pygame.image.load('assets/light.png')


class Light:
    def __init__(self, x, y, width, height, color=None, spread=1):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.spread = spread

    def draw_light(self, gloom, offset):
        for px in range(self.width):
            for py in range(self.height):
                if self.color:
                    gloom.blit(_colorize(circle_filter, self.color), (self.x + offset[0] + px, self.y + offset[1] + py))
                else:
                    gloom.blit(circle_filter, (self.x + offset[0] + px, self.y + offset[1] + py))
        return gloom


def _colorize(surface, color):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color((*color, a)))
    return surface


def render_lights(window, lights, offset):
    gloom = pygame.Surface((WIDTH, HEIGHT))
    gloom.fill(pygame.Color('Grey'))
    for light in lights:
        gloom = light.draw_light(gloom, offset)
    window.blit(gloom, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return window
