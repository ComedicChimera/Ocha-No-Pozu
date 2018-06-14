from map.tile import Tile, TileSet
from random import randint
from util import PLAYER_SPAWN, TILE_SIZE


def generate_easy_over_world():
    tile_map = [Tile(-10 * TILE_SIZE, 0, *TileSet.STONE, 50, PLAYER_SPAWN // TILE_SIZE)]
    base_height = 9
    # generate mountain
    for i in range(1, 11):
        tile_map.append(Tile(i * -TILE_SIZE, PLAYER_SPAWN // TILE_SIZE, *TileSet.STONE, repeat_y=base_height))
        base_height += randint(2, 4)
    # generate normal over-world
    top, bottom = 5, 2
    prev_height = 4
    for i in range(0, 40):
        height = randint(prev_height - 2 if prev_height - 2 > bottom else bottom, prev_height)
        prev_height = height + 1 if height < top else top
        x_pos = i * TILE_SIZE
        tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 1), *TileSet.GRASS))
        if height > 1:
            tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 3), *TileSet.DIRT, repeat_y=2))
        if height > 3:
            tile_map.extend([Tile(x_pos, PLAYER_SPAWN, *TileSet.STONE, repeat_y=height - 3)])
    return tile_map

