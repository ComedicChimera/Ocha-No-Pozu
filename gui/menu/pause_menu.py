from .menu import *
from util import WIDTH, HEIGHT, Point2D
from render.sprite import Sprite
from functools import partial


class PauseMenu(Menu):
    def __init__(self):
        center = (WIDTH // 2, HEIGHT // 2)

        super().__init__([
            Button(center[0] - 100 // 2, center[1] - 30 // 2 - 60,
                   Sprite('', Point2D(100, 30)), Sprite('', Point2D(100, 30)), partial(self._set_state, 1)),
            Button(center[0] - 100 // 2, center[1] - 30 // 2 + 60,
                   Sprite('', Point2D(100, 30)), Sprite('', Point2D(100, 30)), partial(self._set_state, 2))]
        )
        self.state = 0

    def update(self, mouse_position, mouse_down):
        super().update(mouse_position, mouse_down)

    def _set_state(self, state):
        self.state = state
