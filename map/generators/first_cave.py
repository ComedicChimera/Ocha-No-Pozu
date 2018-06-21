from map.tile import *
from random import choice
from util import TILE_SIZE, HEIGHT


def generate_first_cave():
    top, bottom = 6, 3
    prev_height = 4
    tile_map = []
    for i in range(30):
        if i % 2 == 0:
            height = prev_height + choice([-1, 1])
            if bottom > height:
                height = prev_height + 1
            elif top < height:
                height = prev_height - 1
            tile_map.append(Tile(i * TILE_SIZE, 0, *TileSet.STONE, repeat_x=2, repeat_y=height))
            prev_height = height
        hgt = choice([2, 3, 4])
        tile_map.append(Tile(i * TILE_SIZE, HEIGHT - (hgt - 1) * TILE_SIZE, *TileSet.STONE, repeat_y=hgt))

    return tile_map
