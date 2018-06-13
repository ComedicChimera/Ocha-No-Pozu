from enum import Enum
import pygame
from entity.player import Player
import render.draw as draw
import map.generate as generate
from entity.collision import calculate_collisions, calculate_y_base


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
        self.tile_map = generate.generate_easy_over_world()

    def update(self, screen, events):
        if self.state == self.States.MAIN:
            return self._update_main(screen)

    def _update_main(self, screen):
        keys = pygame.key.get_pressed()
        for key, fn in self.key_maps.items():
            if keys[key]:
                fn()

        for entity in [self.player] + self.entities:
            others = self.tile_map + [x for x in self.entities if x != entity]
            if hasattr(entity, 'y_base'):
                entity.y_base = calculate_y_base(entity, others)
            entity.update(calculate_collisions(entity, others))
            screen = draw.draw_sprite(screen, entity)

        return screen


game_state = GameState()
