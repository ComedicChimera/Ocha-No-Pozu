from .generators.overworld import *
from .generators.first_cave import *


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
    tile_map = [Tile(-10 * TILE_SIZE, HEIGHT, *TileSet.STONE, repeat_y=5, repeat_x=40)]
    for i in range(-10, 2):
        tile_map.append(Tile(i * TILE_SIZE, 0, *TileSet.STONE, repeat_y=16))
    cave, lights = generate_first_cave()
    tile_map.extend(cave)
    return tile_map, lights

