from util import HEIGHT, TILE_SIZE, WIDTH, PLAYER_SPAWN
import pygame
from map.tile import SpriteTile


tile_sheet = pygame.image.load('assets/tile_sheet.png')


def draw_entity(screen, entity, offset):
    sprite = entity.sprite()
    if not sprite:
        return
    sprite = sprite.convert_alpha()

    if entity.rotation != 0:
        sprite = pygame.transform.rotate(sprite, entity.rotation)
    if entity.flip_horizontal or entity.flip_vertical:
        sprite = pygame.transform.flip(sprite, entity.flip_horizontal, entity.flip_vertical)

    screen.blit(sprite, (entity.position.x + offset[0], HEIGHT - entity.position.y - entity.dimensions().y + offset[1]))
    if entity.health > 0:
        screen = draw_health_bar(screen, entity, offset)
    return screen


def draw_health_bar(screen, entity, offset):
    bar_size = 3
    x_offset = (entity.dimensions().x - entity.max_health // 3) // 2
    screen.fill((90, 255, 30), (entity.position.x + offset[0] + x_offset,
                                HEIGHT - entity.position.y - entity.dimensions().y - (bar_size + 5) + offset[1], entity.health // 3, bar_size))
    return screen


def draw_tile(screen, tile, offset):
    if isinstance(tile, SpriteTile):
        screen.blit(tile.sprite, (tile.position.x + offset[0], HEIGHT - tile.position.y - tile.dimensions.y + offset[1]))
    else:
        width, height = TILE_SIZE * tile.repeat_x, TILE_SIZE * tile.repeat_y
        tile_image = pygame.Surface((width, height), pygame.SRCALPHA)
        for x in range(tile.repeat_x):
            for y in range(tile.repeat_y):
                x_pos, y_pos = x * TILE_SIZE, y * TILE_SIZE
                if -offset[0] - TILE_SIZE > x_pos + tile.position.x or x_pos + tile.position.x > -offset[0] + WIDTH:
                    continue
                elif offset[1] - PLAYER_SPAWN - TILE_SIZE > height - y_pos + tile.position.y:
                    continue
                elif height - y_pos + tile.position.y > offset[1] + HEIGHT + TILE_SIZE:
                    continue
                tile_image.blit(tile_sheet, (x_pos, y_pos), (tile.sprite_x * TILE_SIZE, tile.sprite_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        screen.blit(tile_image, (tile.position.x + offset[0], HEIGHT - tile.position.y - height + offset[1]))
    return screen
