from gui.element import GUIElement
from render.sprite import rm
from copy import copy


class CoolDownBar(GUIElement):
    def __init__(self):
        super().__init__(10, 10, 100, 40)
        self.cool_down = 0
        self.base_image = rm.load('sprites/cooldown_bar.png')

    def update(self):
        if self.cool_down > 0:
            self.cool_down -= 1

    def get_image(self):
        if self.cool_down > 0:
            image = copy(self.base_image)
            image.fill((39, 255, 93), (36, 16, self.cool_down, 6))
            return image
        return self.base_image
