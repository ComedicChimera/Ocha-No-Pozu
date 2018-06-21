import states.main_state
import pygame
from audio.sound import am, AUDIO_END


class GameState:
    def __init__(self, screen):
        self._state = states.main_state.MainState(screen)
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
            self.quit = True
        pygame.display.update()
        return self._state.window.screen

