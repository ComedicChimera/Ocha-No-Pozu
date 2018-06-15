import states.main_state
import pygame


class GameState:
    def __init__(self, screen):
        self._state = states.main_state.MainState(screen)
        self.quit = False

    def update(self):
        events = pygame.event.get()
        if pygame.QUIT in [e.type for e in events]:
            pygame.quit()
            self.quit = True
            return
        self._state.window.clear((119, 171, 255))
        self._state.update()
        pygame.display.update()
        return self._state.window.screen

