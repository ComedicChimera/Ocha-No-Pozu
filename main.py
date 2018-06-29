import pygame
import util
from state import GameState


pygame.init()

screen = pygame.display.set_mode((util.WIDTH, util.HEIGHT), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Ocha No Pozu')
pygame.display.set_icon(pygame.image.load('assets/game_icon.png'))


clock = pygame.time.Clock()
game_state = GameState(screen)

while not game_state.quit:
    screen = game_state.update()
    clock.tick_busy_loop(30)

pygame.quit()




