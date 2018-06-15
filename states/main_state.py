import pygame
from entity.player import Player
from render.sprite import AnimatedSprite
import map.generate as generate
from entity.collision import calculate_x_range, calculate_y_range
from render.window import Window
from util import WIDTH, HEIGHT, Point2D, PLAYER_SPAWN
from entity.entity import Entity
from gui.cooldown_bar import CoolDownBar


class MainState:
    def __init__(self, screen):
        self.player = Player()
        self.entities = [self.player]
        self.key_maps = {
            pygame.K_a: self.player.move_left,
            pygame.K_d: self.player.move_right,
            pygame.K_SPACE: self.player.jump,
            pygame.K_LSHIFT: self.fade
        }
        self.tile_map = generate.generate_easy_over_world()
        self.window = Window(screen, WIDTH, HEIGHT)
        self._cooldown_bar = CoolDownBar()
        self.background = AnimatedSprite('background.png', Point2D(200, 96), 35, speed=0.25, reverse=True)

    def update(self):
        keys = pygame.key.get_pressed()
        for key, fn in self.key_maps.items():
            if keys[key]:
                fn()

        # image = self.background.get_image().convert_alpha(self.window.screen)
        # image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        #
        # self.window.blit(image, (0, 0))

        objects = self.window.clip_objects(self.entities, self.tile_map)

        for obj in objects:
            if isinstance(obj, Entity):
                others = self.tile_map + [x for x in self.entities if x != obj]
                obj.x_range, obj.y_range = calculate_x_range(obj, others), calculate_y_range(obj, others)

                obj.update()

                # add animation
                if hasattr(obj, 'animate'):
                    obj.animate()

                self.window.draw_entity(obj)
            # assume tile
            else:
                self.window.draw_tile(obj)

        if self.player.fading:
            self.window.draw_overlay((200, 200, 200), 20)
        if not self.player.can_fade:
            self._cooldown_bar.cool_down = self.player.timer_frames / 2

        self.window.set_window_offset(-(self.player.position.x - WIDTH / 2), (self.player.position.y - PLAYER_SPAWN))
        self.window.draw_gui_element(self._cooldown_bar)

    def fade(self):
        if not self.player.fading:
            self.player.fade()
