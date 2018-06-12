from enum import Enum
import pygame
from entity.player import Player


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

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self.key_maps:
                self.key_maps[event.key]()


game_state = GameState()
