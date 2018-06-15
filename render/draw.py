from util import HEIGHT, TILE_SIZE
import pygame


tile_sheet = pygame.image.load('assets/tile_sheet.png')


def draw_entity(screen, entity, offset):
    sprite = entity.sprite().convert_alpha()

    if entity.rotation != 0:
        sprite = pygame.transform.rotate(sprite, entity.rotation)
    if entity.flip_horizontal or entity.flip_vertical:
        sprite = pygame.transform.flip(sprite, entity.flip_horizontal, entity.flip_vertical)

    screen.blit(sprite, (entity.position.x + offset[0], HEIGHT - entity.position.y - entity.dimensions().y + offset[1]))
    return screen


def draw_tile(screen, tile, offset):
    width, height = TILE_SIZE * tile.repeat_x, TILE_SIZE * tile.repeat_y
    tile_image = pygame.Surface((width, height), pygame.SRCALPHA)
    for x in range(tile.repeat_x):
        for y in range(tile.repeat_y):
            tile_image.blit(tile_sheet, (x * TILE_SIZE, y * TILE_SIZE), (tile.sprite_x * TILE_SIZE, tile.sprite_y * TILE_SIZE,
                                                                         TILE_SIZE, TILE_SIZE))
    screen.blit(tile_image, (tile.position.x + offset[0], HEIGHT - tile.position.y - height + offset[1]))
    return screen
