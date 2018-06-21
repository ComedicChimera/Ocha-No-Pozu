import pygame
from entity.player import Player
from render.sprite import AnimatedSprite
import map.generate as generate
from entity.collision import calculate_x_range, calculate_y_range, colliding
from render.window import Window
from util import WIDTH, HEIGHT, Point2D, PLAYER_SPAWN, TILE_SIZE
from entity.entity import Entity
from gui.hud.cooldown_bar import CoolDownBar
from gui.hud.death_text import DeathText
from entity.populate import populate, get_ground
from gui.menu.pause_menu import PauseMenu
from entity.teleporter import Teleporter
from render.lighting import render_lights, Light


class MainState:
    def __init__(self, screen):
        self.player = Player()
        self.key_maps = {
            pygame.K_a: self.player.move_left,
            pygame.K_d: self.player.move_right,
            pygame.K_SPACE: self.player.jump,
            pygame.K_LSHIFT: self.fade,
            pygame.K_ESCAPE: self._invert_pause,
            pygame.K_q: self.player.swing
        }
        self.tile_map = generate.generate_easy_over_world()
        self.entities = [self.player] + populate(get_ground(self.tile_map), (20, 80), 5, 0, 1)
        self._teleporter = Teleporter(TILE_SIZE * 83, 0, 2, 4, 'CAVE')
        self.window = Window(screen, WIDTH, HEIGHT)
        self._cool_down_bar = CoolDownBar()
        self.background = AnimatedSprite('background.png', Point2D(200, 96), 35, speed=0.25, reverse=True)
        self._fade_vignette = pygame.image.load('assets/sprites/vignette.png')
        self.player_alive = True
        self.death_text = None
        self._pause_menu = None
        self._paused = False
        self._gloom = False
        self.lights = []

    def update(self):
        self.window.clear((50, 50, 60) if self._gloom else (119, 171, 255))
        if not self.death_text and not self._paused:
            keys = pygame.key.get_pressed()
            for key, fn in self.key_maps.items():
                if keys[key]:
                    fn()

        objects = self.window.clip_objects(self.entities, self.tile_map)

        for obj in objects:
            if isinstance(obj, Entity):
                others = self.tile_map + [x for x in self.entities if x != obj]
                obj.x_range, obj.y_range = calculate_x_range(obj, others), calculate_y_range(obj, others)

                if not self._paused:
                    if obj.enemy:
                        obj.update(self.player.position)
                    else:
                        obj.update()

                # add animation
                obj.animate()

                # allow entities to deal damage
                if not isinstance(obj, Player) and obj.damage > 0:
                    if obj.should_damage and colliding(obj, self.player):
                        self.player.hurt(obj.damage)
                        obj.should_damage = False
                        obj.set_timer('reset-damage', 20, obj.reset_damage)
                    if colliding(self.player, obj) and self.player.swinging:
                        obj.hurt(self.player.damage)

                self.window.draw_entity(obj)
            # assume tile
            else:
                if obj.damage > 0 and colliding(self.player, obj):
                    self.player.hurt(obj.damage)
                self.window.draw_tile(obj)

        if self._gloom:
            self.window = render_lights(self.window, self.lights, self.window.offset)

        self.window.draw_gui_element(self._cool_down_bar)

        if self._paused:
            self._update_paused()
        elif self.player.health == 0:
            self._play_death_animation()
        elif self.player.fading:
            self.window.draw_overlay(self._fade_vignette)
            self.window.draw_overlay((78, 0, 107), 10)
        elif self._teleporter.check_collision(self.player.position):
            self._teleport(self._teleporter.destination)

        self._cool_down_bar.update(self.player)

        self.window.set_window_offset(-(self.player.position.x - WIDTH / 2), (self.player.position.y - PLAYER_SPAWN))

        # trim dead entities
        self.entities = [x for x in self.entities if x.health > 0 or isinstance(x, Player)]

        return self.player_alive

    def fade(self):
        if not self.player.fading:
            self.player.fade()

    def _invert_pause(self):
        self._paused = not self._paused

    def _update_paused(self):
        self.window.draw_overlay((125, 125, 125), 50)
        if not self._pause_menu:
            self._pause_menu = PauseMenu()
        x, y = pygame.mouse.get_pos()
        self._pause_menu.update(Point2D(x, y), pygame.mouse.get_pressed()[0] == 1)
        self.window.draw_menu(self._pause_menu)
        if self._pause_menu.state == 1:
            self._paused = False
        elif self._pause_menu.state == 2:
            self.player_alive = False
        self._pause_menu.state = 0

    def _play_death_animation(self):
        self.window.draw_overlay((125, 125, 125), 5)
        self.window.draw_overlay(self._fade_vignette)
        if not self.death_text:
            self.death_text = DeathText()
        self.death_text.update()
        self.window.draw_gui_element(self.death_text)
        if self.death_text.animation_over:
            self.player_alive = False

    def _teleport(self, destination):
        if destination == 'CAVE':
            self.player.position.x, self.player.position.y = 2 * TILE_SIZE, 7 * TILE_SIZE
            self.entities = [self.player]
            self.tile_map = generate.generate_cave()
            self._gloom = True
            self.lights = [Light(200, 100, (255, 209, 191), 10)]
