from .menu import Menu, Button
from util import WIDTH, HEIGHT, Point2D
from functools import partial
from render.sprite import Sprite


class MainMenu(Menu):
    def __init__(self):
        center = (WIDTH // 2, HEIGHT // 2)
        super().__init__([
            Button(40, center[1] - 30 + 110, Sprite('buttons/start_selected.png', Point2D(200, 60)),
                   Sprite('buttons/start_deselected.png', Point2D(200, 60)), partial(self._set_state, 1)),
            Button(40, center[1] - 30 + 200, Sprite('buttons/quit_selected.png', Point2D(200, 60)),
                   Sprite('buttons/quit_deselected.png', Point2D(200, 60)), partial(self._set_state, 2))
        ])
        self.state = 0

    def _set_state(self, state):
        self.state = state
