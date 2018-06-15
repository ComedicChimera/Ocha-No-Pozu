from map.tile import Tile, TileSet
from random import randint, choice
from util import PLAYER_SPAWN, TILE_SIZE


def generate_easy_over_world():
    tile_map = [Tile(-10 * TILE_SIZE, 0, *TileSet.STONE, 50, PLAYER_SPAWN // TILE_SIZE)]
    base_height = 9
    # generate mountain
    for i in range(1, 11):
        tile_map.append(Tile(i * -TILE_SIZE, PLAYER_SPAWN // TILE_SIZE + base_height * TILE_SIZE, *TileSet.SNOW_STONE))
        tile_map.append(Tile(i * -TILE_SIZE, PLAYER_SPAWN // TILE_SIZE, *TileSet.STONE, repeat_y=base_height))
        base_height += randint(2, 4)
    # generate normal over-world
    top, bottom = 6, 2
    prev_height = 4
    for i in [x for x in range(0, 40) if x % 2 == 0]:
        height = prev_height + choice([-1, -1, 1, 1, 0])
        height = height if bottom <= height <= top else prev_height
        prev_height = height
        x_pos = i * TILE_SIZE
        for _ in range(2):
            if randint(0, 1) == 0:
                tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * height, *TileSet.GRASS_SURFACE, collidable=False))
            tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 1), *TileSet.GRASS))
            if height > 1:
                tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 3), *TileSet.DIRT, repeat_y=2))
            if height > 3:
                tile_map.extend([Tile(x_pos, PLAYER_SPAWN, *TileSet.STONE, repeat_y=height - 3)])
            x_pos += TILE_SIZE
    return tile_map

