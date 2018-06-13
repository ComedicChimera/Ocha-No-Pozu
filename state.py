from enum import Enum
import pygame
from entity.player import Player
from entity.entity import Entity
import render.draw as draw
from util import Point2D


class GameState:
    class States(Enum):
        MAIN = 0
        MENU = 1

    def __init__(self):
        self.state = self.States.MAIN
        self.entities = []
        self.player = Player()
        self.key_maps = {
            pygame.K_a: self.player.move_left,
            pygame.K_d: self.player.move_right,
            pygame.K_SPACE: self.player.jump
        }

    def update(self, screen, events):
        keys = pygame.key.get_pressed()
        for key, fn in self.key_maps.items():
            if keys[key]:
                fn()

        for entity in [self.player] + self.entities:
            # test collision
            entity.update([])
            screen = draw.draw_sprite(screen, entity)

        return screen


game_state = GameState()
