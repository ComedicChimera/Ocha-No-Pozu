import pygame
from util import WIDTH, HEIGHT
from render.window import Window
from audio.sound import am


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

        self._opacity = 0 if self._opacity < 0 else self._opacity

        text = self._font.render(self._text, True, (255, 255, 255))
        surf = pygame.Surface((text.get_width(), text.get_height()))
        surf.blit(text, (0, 0))
        surf.set_alpha(self._opacity)

        window.blit(surf, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        self._timer += 1

        return window


class CreditState:
    def __init__(self, screen):
        am.stop_music()
        am.play_music('credits.mp3', volume=0.1)
        self.window = Window(screen, WIDTH, HEIGHT)
        self._timer = 0
        self._font = pygame.font.SysFont('system.ttf', 40)
        self._opacity = 0
        self._text = FadeInText('Thanks for playing!', self._font, 100)
        self.completed = False

        self._credits = [
                    'Thanks for Playing!',
                    '~ Developers ~',
                    'Jordan Gaines',
                    'Jeongwoo Choi',
                    'Brandon Braswell',
                    '~ Music Used ~',
                    'Paragon X9 - Chaoz Japan',
                    'Waterflame - Jumper',
                    'Trickster Imps - Dark Cave Music',
                    'Megamerge! Music - Shadowy Cascade',
                    'Toby Fox - Megalo Strike Back [Kaatu Remix]',
                    'Sheet Music Boss - Rush B',
                    '~ Special Thanks ~',
                    'E-Money',
                    'Andrew Arnold',
                    'Roman Testroet',
                    'ScrumMaster69',
                    'Eli Edds',
                    '~ Developed at Duke TIP 2018 ~'
        ]

    def update(self):
        self.window.clear((0, 0, 0))
        if self._timer < len(self._credits) * 100:
            if self._timer % 100 == 0:
                self._text = FadeInText(self._credits[self._timer // 100], self._font, 100)
        else:
            self.completed = True
        self.window = self._text.draw(self.window)
        self._timer += 1
        return not self.completed
