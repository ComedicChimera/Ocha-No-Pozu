import pygame
import util


pygame.init()

screen = pygame.display.set_mode((util.WIDTH, util.HEIGHT), 0, 32)
pygame.display.set_caption('Final Game')


def loop():
    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        if pygame.QUIT in [e.type for e in events]:
            pygame.quit()
            break
        update(events)
        clock.tick_busy_loop(30)


def update(events):
    pass


loop()





