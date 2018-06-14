from inspect import signature
import states.main_state


class GameState:
    def __init__(self):
        self.state = states.main_state.MainState()

    def update(self, screen, events):
        if len(signature(self.state.update).parameters) > 1:
            return self.state.update(screen, events)
        else:
            return self.state.update(screen)


game_state = GameState()
