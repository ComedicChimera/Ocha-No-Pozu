import pygame
from util import WIDTH, HEIGHT
from .element import GUIElement


class DeathText(GUIElement):
    def __init__(self):
        pygame.font.init()
        self._scale_factor = 20
        self._text = pygame.font.Font('assets/fonts/darksouls.ttf', 80).render('You Died', False, (125, 0, 0))
        self.animation_over = False
        super().__init__((WIDTH - self._text.get_width()) // 2, (HEIGHT - self._text.get_height()) // 2, self._text.get_width() + int(self._scale_factor), self._text.get_height() +
                         int(self._scale_factor))

    def update(self):
        if self._scale_factor == 120:
            self.animation_over = True
        self._scale_factor += 0.5

    def get_image(self):
        text = pygame.transform.scale(self._text, (self._text.get_width() + int(self._scale_factor),
                                                   self._text.get_height() + int(self._scale_factor)))
        self.position.x, self.position.y = (WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2
        self.dimensions.x, self.dimensions.y = self._text.get_width() + int(self._scale_factor), self._text.get_height() + int(self._scale_factor)
        return text
