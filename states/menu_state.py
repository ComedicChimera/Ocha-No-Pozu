from gui.menu.main_menu import MainMenu
from render.window import Window
from render.sprite import rm
from util import WIDTH, HEIGHT, Point2D
from audio.sound import am
import pygame


class MenuState:
    def __init__(self, screen):
        am.stop_music()
        am.play_music('menu.mp3', volume=0.1, loop=True)
        self.window = Window(screen, WIDTH, HEIGHT)
        self._menu = MainMenu()
        self._title_screen = rm.load('sprites/title_screen.png')
        self.state = 0

    def update(self):
        self.window.blit(self._title_screen, (0, 0))
        x, y = pygame.mouse.get_pos()
        self._menu.update(Point2D(x, y), pygame.mouse.get_pressed()[0])
        self.window.draw_menu(self._menu)
        self.state = self._menu.state
        return self.state != 2

    def __del__(self):
        rm.unload('sprites/title_screen.png')
