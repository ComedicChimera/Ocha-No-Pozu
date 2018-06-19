import pygame
from entity.player import Player
from render.sprite import AnimatedSprite
import map.generate as generate
from entity.collision import calculate_x_range, calculate_y_range, colliding
from render.window import Window
from util import WIDTH, HEIGHT, Point2D, PLAYER_SPAWN
from entity.entity import Entity
from gui.cooldown_bar import CoolDownBar
from gui.death_text import DeathText
from entity.populate import populate, get_ground
from .pause_state import PauseMenu


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
        self.window = Window(screen, WIDTH, HEIGHT)
        self._cool_down_bar = CoolDownBar()
        self.background = AnimatedSprite('background.png', Point2D(200, 96), 35, speed=0.25, reverse=True)
        self._fade_vignette = pygame.image.load('assets/sprites/vignette.png')
        self.player_alive = True
        self.death_text = None
        self._pause_menu = None
        self._paused = False

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.death_text and not self._paused:
            for key, fn in self.key_maps.items():
                if keys[key]:
                    fn()

        objects = self.window.clip_objects(self.entities, self.tile_map)

        for obj in objects:
            if isinstance(obj, Entity):
                others = self.tile_map + [x for x in self.entities if x != obj]
                obj.x_range, obj.y_range = calculate_x_range(obj, others), calculate_y_range(obj, others)

                if not self._paused:
                    if hasattr(obj, 'update_enemy'):
                        obj.update_enemy(self.player.position)
                    else:
                        obj.update()

                # add animation
                if hasattr(obj, 'animate'):
                    obj.animate()

                # allow entities to deal damage
                if not isinstance(obj, Player) and obj.damage > 0:
                    if obj.should_damage and colliding(obj, self.player):
                        self.player.hurt(obj.damage)
                        obj.should_damage = False
                        obj.set_timer(20, obj.reset_damage)
                    if colliding(self.player, obj) and self.player.swinging:
                        obj.hurt(self.player.damage)

                self.window.draw_entity(obj)
            # assume tile
            else:
                if obj.damage > 0 and colliding(self.player, obj):
                    self.player.hurt(obj.damage)
                self.window.draw_tile(obj)

        self.window.draw_gui_element(self._cool_down_bar)

        if self._paused:
            self._update_paused(keys)
        elif self.player.health == 0:
            self.window.draw_overlay((125, 125, 125), 5)
            self.window.draw_overlay(self._fade_vignette)
            if not self.death_text:
                self.death_text = DeathText()
            self.window = self.death_text.update(self.window)
            if self.death_text.animation_over:
                self.player_alive = False
        elif self.player.fading:
            self.window.draw_overlay(self._fade_vignette)
            self.window.draw_overlay((78, 0, 107), 10)
            self._cool_down_bar.cool_down = (15 - self.player.timer_frames) * 6
        elif not self.player.can_fade:
            self._cool_down_bar.cool_down = self.player.timer_frames / 2
        elif self._cool_down_bar.cool_down != 0:
            self._cool_down_bar.cool_down = 0

        self.window.set_window_offset(-(self.player.position.x - WIDTH / 2), (self.player.position.y - PLAYER_SPAWN))

        # trim dead entities
        self.entities = [x for x in self.entities if x.health > 0 or isinstance(x, Player)]

        return self.player_alive

    def fade(self):
        if not self.player.fading:
            self.player.fade()

    def _invert_pause(self):
        self._paused = not self._paused

    def _update_paused(self, keys):
        self.window.draw_overlay((125, 125, 125), 50)
        if not self._pause_menu:
            self._pause_menu = PauseMenu()
        for key in keys:
            if key == pygame.K_w:
                self._pause_menu.cycle_selected()
            elif key == pygame.K_s:
                self._pause_menu.cycle_selected()
        x, y = pygame.mouse.get_pos()
        self._pause_menu.set_selected_from_position(x, y, pygame.mouse.get_pressed()[0] == 1)
        self.window = self._pause_menu.draw_menu(self.window)
        if self._pause_menu.state == 1:
            self._paused = False
        elif self._pause_menu.state == 2:
            self.player_alive = False
        self._pause_menu.state = 0

