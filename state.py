from states.main_state import MainState
from states.menu_state import MenuState
from states.credit_state import CreditState

import pygame
from audio.sound import am, AUDIO_END


class GameState:
    def __init__(self, screen):
        self._screen = screen
        self._state = MenuState(self._screen)
        self.quit = False

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                self.quit = True
                return
            elif e.type == AUDIO_END:
                am.remove_bottom()

        if not self._state.update():
            self._handle_state_close()

        if isinstance(self._state, MenuState):
            if self._state == 1:
                self._state = MainState(self._screen)

        pygame.display.update()
        return self._state.window.screen

    def _handle_state_close(self):
        if isinstance(self._state, MainState):
            if self._state.won:
                self._state = CreditState(self._screen)
            else:
                self._state = MenuState(self._screen)
        elif isinstance(self._state, CreditState):
            self._state = MenuState(self._screen)
        else:
            self.quit = True

