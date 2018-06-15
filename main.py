import pygame
import util
from state import GameState


pygame.init()

screen = pygame.display.set_mode((util.WIDTH, util.HEIGHT), 0, 32)
pygame.display.set_caption('Final Game')


clock = pygame.time.Clock()
game_state = GameState(screen)

while not game_state.quit:
    screen = game_state.update()
    clock.tick_busy_loop(30)





