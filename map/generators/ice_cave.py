from random import randint
from util import TILE_SIZE, HEIGHT
from map.tile import *
from render.lighting import Light


def generate_ice_cave_main():
    tile_map, lights = [], []
    prev_height = 3
    top, bottom = 7, 3
    for i in range(0, 80):
        height = prev_height + randint(-1, 1)
        if height < bottom:
            height = prev_height + 1
        elif height > top:
            height = prev_height - 1
        prev_height = height
        tile_map.append(Tile(i * TILE_SIZE, 3 * TILE_SIZE, *TileSet.ICE_ROCK, repeat_y=height))
        rand_len = randint(0, 3)
        tile_map.append(Tile(i * TILE_SIZE, (17 - rand_len) * TILE_SIZE, *TileSet.ICE_ROCK, repeat_y=rand_len))
        if randint(0, 1) == 0:
            tile_map.append(Tile(i * TILE_SIZE, (16 - rand_len) * TILE_SIZE, *TileSet.ICE_STALACTITE, collidable=False))
        if randint(0, 2) == 0:
            tile_map.append(Tile(i * TILE_SIZE, (3 + height) * TILE_SIZE, *TileSet.ICE_STALAGMITE, collidable=False))
        elif randint(0, 8) == 0:
            tile_map.append(SpriteTile(
                'blue_crystal.png', i * TILE_SIZE, (3 + height) * TILE_SIZE, TILE_SIZE, TILE_SIZE,
                frames=5, collidable=False
            ))
            lights.append(Light((i - 3) * TILE_SIZE + 16, HEIGHT - ((height + 6) * TILE_SIZE + 16), (191, 229, 255), spread=6))
    for i in range(0, 5):
        if i % 2 == 0:
            tile_map.append(Tile((i + 80) * TILE_SIZE, 3 * TILE_SIZE, *TileSet.ICE_ROCK, repeat_x=2, repeat_y=prev_height + i // 2))
            tile_map.append(Tile((i + 80) * TILE_SIZE, ((10 + prev_height) - i // 2) * TILE_SIZE, *TileSet.ICE_ROCK, repeat_x=2, repeat_y=20))
    tile_map.extend([
        Tile(86 * TILE_SIZE, 0, *TileSet.ICE_ROCK, repeat_x=8, repeat_y=5 + prev_height),
        Tile(86 * TILE_SIZE, (8 + prev_height) * TILE_SIZE, *TileSet.ICE_ROCK, repeat_x=8, repeat_y=18),
        Tile(85 * TILE_SIZE, (5 + prev_height) * TILE_SIZE, *TileSet.STONE, repeat_x=8, repeat_y=3)
    ])
    return tile_map, lights
