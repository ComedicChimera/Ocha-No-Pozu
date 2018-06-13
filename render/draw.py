from util import HEIGHT, TILE_SIZE
import pygame


tile_sheet = pygame.image.load('assets/tile_sheet.png')


def draw_sprite(screen, entity):
    sprite = entity.sprite()
    screen.blit(sprite.convert(), (entity.position.x, HEIGHT - entity.position.y - entity.dimensions().y))
    return screen


def draw_tile(screen, tile):
    width, height = TILE_SIZE * tile.repeat_x, TILE_SIZE * tile.repeat_y
    tile_image = pygame.Surface((width, height))
    for x in range(tile.repeat_x):
        for y in range(tile.repeat_y):
            tile_image.blit(tile_sheet, (x * TILE_SIZE, y * TILE_SIZE), (tile.sprite_x * TILE_SIZE, tile.sprite_y * TILE_SIZE,
                                                                         TILE_SIZE, TILE_SIZE))
    screen.blit(tile_image, (tile.position.x, HEIGHT - tile.position.y - height))
    return screen
