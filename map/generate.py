from map.tile import *
from random import randint, choice
from util import PLAYER_SPAWN, TILE_SIZE
import itertools


def generate_easy_over_world():
    tile_map = [Tile(-10 * TILE_SIZE, 0, *TileSet.STONE, 90, PLAYER_SPAWN // TILE_SIZE)]
    base_height = 9
    # generate mountain
    for i in range(1, 11):
        tile_map.append(Tile(i * -TILE_SIZE, PLAYER_SPAWN // TILE_SIZE + base_height * TILE_SIZE, *TileSet.SNOW_STONE))
        tile_map.append(Tile(i * -TILE_SIZE, PLAYER_SPAWN // TILE_SIZE, *TileSet.STONE, repeat_y=base_height))
        base_height += randint(2, 4)
    # generate normal over-world
    tile_map += _generate_over_world(40, 7, 2)
    tile_map += _generate_over_world(40, 7, 2, 40, 7, tile_map[-1].position.y // TILE_SIZE)
    return tile_map


# generate standard over world map
def _generate_over_world(tiles, top, bottom, x_offset=0, gaps=0, start_height=None):
    gap_locations = []
    if gaps > 0:
        gap_locations = [randint(x_offset, tiles + x_offset) for _ in range(gaps)]
        gap_locations = itertools.chain.from_iterable([[x, x+1] if randint(0, 1) == 0 else [x] for x in gap_locations])
        gap_locations = list(map(lambda x: x * TILE_SIZE, gap_locations))
    prev_height = (top + bottom) // 2
    tile_map = []
    spawned_tree = False
    spawned_pits = 0
    for i in [x for x in range(0, tiles) if x % 2 == 0]:
        x_pos = i * TILE_SIZE + x_offset * TILE_SIZE
        if x_pos in gap_locations and i < tiles - 2 and spawned_pits < 2:
            tile_map.append(Tile(x_pos, TILE_SIZE * 3, *TileSet.SPIKES, 2, collidable=False, damage=100))
            spawned_pits += 1
            continue
        spawned_pits = 0
        height = prev_height + choice([-1, -1, 1, 1, 0])
        height = height if bottom <= height <= top else prev_height
        if start_height:
            height = start_height
            start_height = None
        for _ in range(2):
            if randint(0, 1) == 0:
                tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * height, *_get_decorate_tile(), collidable=False))
            elif randint(0, 4) == 0 and not spawned_tree and prev_height <= height:
                tile_map.append(SpriteTile('tree.png', x_pos - 48,
                                           (PLAYER_SPAWN + TILE_SIZE * height), 128, 128))
                spawned_tree = True
            else:
                spawned_tree = False
            tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 1), *TileSet.GRASS))
            if height > 1:
                tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 3), *TileSet.DIRT, repeat_y=2))
            if height > 3:
                tile_map.extend([Tile(x_pos, PLAYER_SPAWN, *TileSet.STONE, repeat_y=height - 3)])
            x_pos += TILE_SIZE
        prev_height = height
    return tile_map


def _get_decorate_tile():
    if randint(0, 4) == 0:
        return choice([
            TileSet.GRASS_SURFACE,
            TileSet.PINK_FLOWER,
            TileSet.YELLOW_FLOWER,
            TileSet.MOSSY_LOG,
            TileSet.LOG
        ])
    else:
        return TileSet.GRASS_SURFACE
