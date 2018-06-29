import pygame
from util import WIDTH, HEIGHT
from render.window import Window


class FadeInText:
    def __init__(self, text, font, duration):
        self._text = text
        self._font = font
        self._opacity = 0
        self._duration = duration
        self._timer = 0

    def draw(self, window):
        if self._timer < self._duration // 4:
            self._opacity += 255 / (self._duration // 4)

        elif self._timer > self._duration // 4 * 3:
            self._opacity -= 255 / (self._duration // 4)

        text = self._font.render(self._text, (255, 255, 255, self._opacity))

        window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        self._timer += 1


class CreditState:
    def __init__(self, screen):
        self.window = Window(screen, WIDTH, HEIGHT)
        self._timer = 0
        self._font = pygame.font.SysFont('system.ttf', 100)
        self._opacity = 0
        self._text = FadeInText('Thanks for playing!', self._font, 200)
        self.completed = False

    def update(self):
        if self._timer == 200:
            self._text = FadeInText('Programmed by Jordan Gaines', self._font, 200)
        elif self._timer == 400:
            self._text = FadeInText('Artwork by Jon Choi and Brandon Braswell', self._font, 200)
        elif self._timer == 600:
            self._text = FadeInText('Sound Design by Jordan Gaines and Jon Choi', self._font, 200)
        elif self._timer == 800:
            self._text = FadeInText('Developed at Duke TIP 2018', self._font, 200)
        elif self._timer == 1000:
            self._text = FadeInText('Special Thanks to All of our Duke TIP Class (except Rene)', self._font, 200)
        elif self._timer == 1200:
            self.completed = True
        return self.completed