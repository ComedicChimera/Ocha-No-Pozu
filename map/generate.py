from .generators.overworld import *
from .generators.first_cave import *
from .generators.lava_cave import *


def generate_easy_over_world():
    tile_map = [Tile(-10 * TILE_SIZE, 0, *TileSet.STONE, 90, PLAYER_SPAWN // TILE_SIZE)]
    base_height = 9
    # generate mountain
    for i in range(1, 11):
        tile_map.append(Tile(i * -TILE_SIZE, PLAYER_SPAWN // TILE_SIZE + base_height * TILE_SIZE, *TileSet.SNOW_STONE))
        tile_map.append(Tile(i * -TILE_SIZE, PLAYER_SPAWN // TILE_SIZE, *TileSet.STONE, repeat_y=base_height))
        base_height += randint(2, 4)
    # generate normal over-world
    tile_map += generate_over_world(40, 7, 2)
    tile_map += generate_over_world(40, 7, 2, 40, 7, tile_map[-1].position.y // TILE_SIZE)
    tile_map += generate_cave_entrance()
    return tile_map


def generate_cave():
    tile_map = [Tile(-10 * TILE_SIZE, HEIGHT, *TileSet.STONE, repeat_y=5, repeat_x=60)]
    for i in range(-10, 2):
        tile_map.append(Tile(i * TILE_SIZE, 0, *TileSet.STONE, repeat_y=16))
    cave, lights = generate_first_cave()
    tile_map.extend(cave)
    return tile_map, lights


def generate_lava_cave():
    tile_map = [
        Tile(-14 * TILE_SIZE, 0, *TileSet.STONE, repeat_x=14, repeat_y=8),
        Tile(-2 * TILE_SIZE, 8 * TILE_SIZE, *TileSet.CRACKED_STONE, repeat_x=2, repeat_y=3),
        Tile(-14 * TILE_SIZE, 8 * TILE_SIZE, *TileSet.GLOOM_STONE, repeat_x=12, repeat_y=3),
        Tile(-14 * TILE_SIZE, 11 * TILE_SIZE, *TileSet.STONE, repeat_x=14, repeat_y=16)
                       ]
    for i in range(0, 3):
        tile_map.extend([
            Tile(i * TILE_SIZE * 2, 0, *TileSet.STONE, repeat_x=2, repeat_y=(8 - i)),
            Tile(i * TILE_SIZE * 2, (11 + i) * TILE_SIZE, *TileSet.STONE, repeat_x=2, repeat_y=16)
        ])
    cave, lights = generate_lava_cave_gaps()
    tile_map.extend(cave)
    return tile_map, lights

