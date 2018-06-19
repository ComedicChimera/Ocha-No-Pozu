from util import Point2D, WIDTH, HEIGHT
import pygame


class PauseMenu:
    def __init__(self):
        self.menu = {
            'Continue': [self._continue, True],
            'Quit': [self._quit, False]
        }
        self.state = 0
        self._button_dimensions = Point2D(200, 60)
        self._continue_text = pygame.font.SysFont('arial.ttf', self._button_dimensions.y - 10).render('Continue', False, (0, 0, 0))
        self._quit_text = pygame.font.SysFont('arial.ttf', self._button_dimensions.y - 10).render('Quit', False, (0, 0, 0))

    def _continue(self):
        self.state = 1

    def _quit(self):
        self.state = 2

    def _set_selected(self, menu_item):
        for key in self.menu.keys():
            if key == menu_item:
                self.menu[key][1] = True
            else:
                self.menu[key][1] = False

    def draw_menu(self, window):
        top, bottom = self._calculate_button_positions()
        deselected_color, selected_color = (80, 80, 80), (143, 39, 255)
        width, height = self._button_dimensions.x, self._button_dimensions.y
        window.draw_rect(selected_color if self.menu['Continue'][1] else deselected_color, (*top, width, height))
        window.draw_rect((180, 180, 180), (top[0] + 2, top[1] + 2, width - 4, height - 4))
        window.draw_text(self._continue_text, (top[0] + (self._button_dimensions.x - self._continue_text.get_width()) // 2,
                                               top[1] + (self._button_dimensions.y - self._continue_text.get_height()) // 2))
        window.draw_rect(selected_color if self.menu['Quit'][1] else deselected_color, (*bottom, width, height))
        window.draw_rect((180, 180, 180), (bottom[0] + 2, bottom[1] + 2, width - 4, height - 4))
        window.draw_text(self._quit_text, (bottom[0] + (self._button_dimensions.x - self._quit_text.get_width()) // 2,
                                           bottom[1] + (self._button_dimensions.y - self._quit_text.get_height()) // 2))
        return window

    def _calculate_button_positions(self):
        center = (WIDTH // 2, HEIGHT // 2)
        top = [center[0] - self._button_dimensions.x // 2, center[1] - self._button_dimensions.y // 2 - 60]
        bottom = [center[0] - self._button_dimensions.x // 2, center[1] - self._button_dimensions.y // 2 + 60]
        return top, bottom

    def cycle_selected(self):
        self.menu['Continue'][1] = not self.menu['Quit'][1]

    def set_selected_from_position(self, x, y, mouse_down):
        top, bottom = self._calculate_button_positions()
        if top[0] <= x <= top[0] + self._button_dimensions.x and top[1] <= y <= top[1] + self._button_dimensions.y:
            self._set_selected('Continue')
        elif bottom[0] <= x <= bottom[0] + self._button_dimensions.x and bottom[1] <= y <= bottom[1] + self._button_dimensions.y:
            self._set_selected('Quit')
        else:
            # will set none of them to selected
            self._set_selected('NONE')
        if mouse_down:
            for item in self.menu.values():
                if item[1]:
                    item[0]()
