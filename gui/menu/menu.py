from render.sprite import rm
from util import Point2D


class Button:
    def __init__(self, x, y, sprite_selected, sprite_deselected, fn):
        self.position = Point2D(x, y)
        self.sprite_selected = sprite_selected
        self.sprite_deselected = sprite_deselected
        self.selected = False
        self._click_event = fn

    def check_hover(self, pos):
        sprite = self.sprite_selected if self.selected else self.sprite_deselected
        if not (self.position.x <= pos.x <= self.position.x + sprite.dimensions.x):
            return False
        elif not (self.position.y <= pos.y <= self.position.y + sprite.dimensions.y):
            return False
        return True

    def click(self):
        self._click_event()

    def get_image(self):
        if self.selected:
            return self.sprite_selected.get_image()
        else:
            return self.sprite_deselected.get_image()

    def __del__(self):
        rm.unload(self.sprite_selected.path)
        rm.unload(self.sprite_deselected.path)


class Menu:
    def __init__(self, buttons):
        self.buttons = buttons
        self.closed = False

    def update(self, mouse_position, mouse_down):
        for button in self.buttons:
            if button.check_hover(mouse_position):
                button.selected = True
                if mouse_down:
                    button.click()
            else:
                button.selected = False

