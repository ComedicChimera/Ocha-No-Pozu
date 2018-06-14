import pygame
from entity.player import Player
import render.draw as draw
from render.sprite import AnimatedSprite
import map.generate as generate
from entity.collision import calculate_x_range, calculate_y_range
from render.window import Window
from util import WIDTH, HEIGHT, Point2D, PLAYER_SPAWN
from entity.entity import Entity


class MainState:
    def __init__(self):
        self.player = Player()
        self.entities = [self.player]
        self.key_maps = {
            pygame.K_a: self.player.move_left,
            pygame.K_d: self.player.move_right,
            pygame.K_SPACE: self.player.jump
        }
        self.tile_map = generate.generate_easy_over_world()
        self.window = Window(WIDTH, HEIGHT)
        self.background = AnimatedSprite('background.png', Point2D(200, 96), 35, speed=0.25, reverse=True)

    def update(self, screen):
        keys = pygame.key.get_pressed()
        for key, fn in self.key_maps.items():
            if keys[key]:
                fn()

        image = self.background.get_image().convert_alpha(screen)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))

        screen.blit(image, (0, 0))

        objects = self.window.crop_window(self.entities, self.tile_map)

        for obj in objects:
            if isinstance(obj, Entity):
                others = self.tile_map + [x for x in self.entities if x != obj]
                obj.x_range, obj.y_range = calculate_x_range(obj, others), calculate_y_range(obj, others)
                obj.update()

                # add animation
                if hasattr(obj, 'animate'):
                    obj.animate()

                screen = draw.draw_entity(screen, obj, self.window.offset)
            # assume tile
            else:
                screen = draw.draw_tile(screen, obj, self.window.offset)

        self.window.set_window_offset(-(self.player.position.x - WIDTH / 2), (self.player.position.y - PLAYER_SPAWN))

        return screen
