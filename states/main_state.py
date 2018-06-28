import pygame
from entity.player import Player, Arrow
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
from render.lighting import render_lights
from audio.sound import am
from entity.projectile import Projectile
from entity.bosses.final_boss import FinalBoss


class MainState:
    def __init__(self, screen):
        self.player = Player()
        self.key_maps = {
            pygame.K_a: self.player.move_left,
            pygame.K_d: self.player.move_right,
            pygame.K_SPACE: self.player.jump,
            pygame.K_LSHIFT: self.fade,
            pygame.K_ESCAPE: self._invert_pause,
            pygame.K_q: self.player.swing,
            pygame.K_e: self.player.shoot
        }
        self.tile_map = generate.generate_easy_over_world()
        self.entities = [self.player] + populate(get_ground(self.tile_map), (20, 80), 5, 0, 1)
        self._teleporter = Teleporter(TILE_SIZE * 83, 0, 2, 3, 'CAVE')
        self.window = Window(screen, WIDTH, HEIGHT)
        self._cool_down_bar = CoolDownBar()
        self._fade_vignette = pygame.image.load('assets/sprites/vignette.png')
        self.player_alive = True
        self.death_text = None
        self._pause_menu = None
        self._paused = False
        self._gloom = False
        self.fill_color = (119, 171, 255)
        self.lights = []
        self.boss_fight = False
        am.play_music('overworld.mp3', volume=0.1, loop=True)

    def update(self):
        if self._paused:
            self._update_paused()
            return True

        self.window.clear(self.fill_color)
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

                if isinstance(obj, FinalBoss):
                    obj.update(self.player.position, others)
                elif obj.enemy:
                    obj.update(self.player.position)
                else:
                    obj.update()

                # add animation
                obj.animate()

                # allow entities to deal damage
                if not isinstance(obj, Player) and obj.damage > 0:
                    if isinstance(obj, Arrow):
                        for other in others:
                            if colliding(obj, other) and isinstance(other, Entity) and other.enemy:
                                other.hurt(obj.damage)
                    elif obj.should_damage and colliding(obj, self.player):
                        self.player.hurt(obj.damage)
                        obj.should_damage = False
                        obj.set_timer('reset-damage', 20, obj.reset_damage)
                # check for damage
                if colliding(self.player, obj) and self.player.swinging and obj.enemy:
                    obj.hurt(self.player.damage)

                # check for projectiles
                if isinstance(obj, Projectile):
                    for other in others:
                        if colliding(obj, other) and obj.parent != other:
                            if other.collidable or (isinstance(other, Entity) and not isinstance(other, Projectile)):
                                obj.hurt(obj.max_health)
                            break

                if hasattr(obj, 'healing'):
                    if colliding(self.player, obj):
                        self.player.heal(obj.healing)
                        obj.health -= 1

                # check spawned children
                if len(obj.children) > 0:
                    self.entities.extend(obj.children)
                    obj.children = []

                self.window.draw_entity(obj)
            # assume tile
            else:
                if obj.damage > 0 and colliding(self.player, obj):
                    self.player.hurt(obj.damage)
                self.window.draw_tile(obj)

        if self._gloom:
            self.window = render_lights(self.window, self.lights, self.window.offset)

        self.window.draw_gui_element(self._cool_down_bar)

        if self.player.health == 0:
            am.stop_music()
            self._play_death_animation()
        elif self.player.fading:
            self.window.draw_overlay(self._fade_vignette)
            self.window.draw_overlay((237, 193, 255))
        elif self._teleporter.check_collision(self.player.position):
            self._teleport(self._teleporter.destination)

        self._cool_down_bar.update(self.player)

        if not self.boss_fight:
            x_shift = 0
            if self.player.swinging and not self.player.flip_horizontal:
                x_shift = 25
            self.window.set_window_offset(-(self.player.position.x - WIDTH / 2) - x_shift, (self.player.position.y - PLAYER_SPAWN))

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
        pygame.font.init()
        self.window.draw_overlay((0, 0, 0))
        text = pygame.font.SysFont('arial.ttf', 50).render('Loading...', False, (255, 255, 255))
        self.window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        if destination == 'CAVE':
            am.stop_music()
            am.play_music('cave.mp3', volume=0.3, loop=True)
            self.player.position.x, self.player.position.y = 2 * TILE_SIZE, 7 * TILE_SIZE
            self.tile_map, self.lights = generate.generate_cave()
            self.entities = self.entities[:1] + populate(get_ground(self.tile_map), (10, 40), 6, 2, 2)
            self._gloom = True
            self.fill_color = (50, 50, 60)
            self._teleporter = Teleporter(51 * TILE_SIZE, self.tile_map[-1].position.y, 4, 4, 'LAVA_CAVE')
        elif destination == 'LAVA_CAVE':
            self.player.position.x, self.player.position.y = 0, 9 * TILE_SIZE
            self.tile_map, self.lights = generate.generate_lava_cave()
            self.entities = self.entities[:1] + populate(get_ground(self.tile_map), (10, 60), 3, 3, 3)
            self._teleporter = Teleporter(83 * TILE_SIZE, 8 * TILE_SIZE, 4, 4, 'ICE_CAVE')
        elif destination == 'ICE_CAVE':
            am.stop_music()
            am.play_music('ice_cave.mp3', volume=0.3, loop=True)
            self.player.position.x, self.player.position.y = 2 * TILE_SIZE, 9 * TILE_SIZE
            self.tile_map, self.lights = generate.generate_ice_cave()
            self.entities = self.entities[:1] + populate(get_ground(self.tile_map), (10, 70), 4, 4, 4)
            self._teleporter = Teleporter(84 * TILE_SIZE, 8 * TILE_SIZE, 4, 4, 'BOSS_ROOM')
        elif destination == 'BOSS_ROOM':
            am.stop_music()
            self.player.position.x, self.player.position.y = 2 * TILE_SIZE, 3 * TILE_SIZE
            self.tile_map, self.lights = generate.generate_boss_room(), []
            self.entities = self.entities[:1]
            self._gloom = False
            self.fill_color = (0, 0, 0)
            self._teleporter = Teleporter(40 * TILE_SIZE, 3 * TILE_SIZE, 4, 4, 'FINAL_BOSS_FIGHT')
        elif destination == 'FINAL_BOSS_FIGHT':
            am.play_music('final_boss.mp3', volume=0.2, loop=True)
            self.boss_fight = True
            self.tile_map = generate.generate_final_boss_floor()
            self.entities = self.entities[:1]
            self.entities.append(FinalBoss(WIDTH // 2 - 72, HEIGHT // 2 - 54))
            self.player.position.x, self.player.position.y = WIDTH // 2, TILE_SIZE
            self.window.set_window_offset(0, 0)
