from gui.element import GUIElement


class CoolDownBar(GUIElement):
    def __init__(self):
        super().__init__(10, 10, 100, 40)
        self.cool_down = 0

    def update(self):
        pass
