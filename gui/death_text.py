import pygame
from util import WIDTH, HEIGHT


class DeathText:
    def __init__(self):
        pygame.font.init()
        self._scale_factor = 20
        self._text = pygame.font.Font('assets/fonts/darksouls.ttf', 80).render('You Died', False, (125, 0, 0))
        self.animation_over = False

    def update(self, window):
        text = pygame.transform.scale(self._text, (self._text.get_width() + int(self._scale_factor),
                                                   self._text.get_height() + int(self._scale_factor)))
        window.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
        if self._scale_factor == 120:
            self.animation_over = True
        self._scale_factor += 0.5
        return window
