import pygame
import util
from state import game_state


pygame.init()

screen = pygame.display.set_mode((util.WIDTH, util.HEIGHT), 0, 32)
pygame.display.set_caption('Final Game')


clock = pygame.time.Clock()

while True:
    events = pygame.event.get()
    if pygame.QUIT in [e.type for e in events]:
        pygame.quit()
        break
    screen.fill((0, 0, 0))
    screen = game_state.update(screen, events)
    pygame.display.update()
    clock.tick_busy_loop(30)





