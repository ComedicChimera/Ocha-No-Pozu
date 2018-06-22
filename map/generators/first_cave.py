from map.tile import *
from random import choice, randint
from util import TILE_SIZE, HEIGHT
from render.lighting import Light


def generate_first_cave():
    top, bottom = 6, 3
    prev_height = 4
    tile_map, lights = [], []
    for i in range(1, 50):
        if i % 2 == 0:
            height = prev_height + choice([-1, 1])
            if bottom > height:
                height = prev_height + 1
            elif top < height:
                height = prev_height - 1
            tile_map.append(Tile(i * TILE_SIZE, 0, *TileSet.STONE, repeat_x=2, repeat_y=height))
            prev_height = height
            if randint(0, 2) == 0:
                tile_map.append(Tile((i + randint(0, 1)) * TILE_SIZE, height * TILE_SIZE, *TileSet.STALAGMITE, collidable=False))
            elif i % randint(5, 6) == 0:
                x_shift = randint(0, 1)
                tile_map.append(SpriteTile('torch.png', (i + x_shift) * TILE_SIZE, height * TILE_SIZE,
                                           TILE_SIZE, TILE_SIZE, frames=5, render_first=True))
                lights.append(Light((i + x_shift - 10) * TILE_SIZE + 16, HEIGHT - ((height + 10) * TILE_SIZE) - 16, (255, 240, 193), 20))
        hgt = choice([2, 3, 4])
        if randint(0, 1) == 0:
            tile_map.append(Tile(i * TILE_SIZE, HEIGHT - hgt * TILE_SIZE, *TileSet.STALACTITE, collidable=False))
        tile_map.append(Tile(i * TILE_SIZE, HEIGHT - (hgt - 1) * TILE_SIZE, *TileSet.STONE, repeat_y=hgt))
    tile_map.extend([
        Tile(50 * TILE_SIZE, 0, *TileSet.STONE, repeat_x=16, repeat_y=prev_height),
        Tile(50 * TILE_SIZE, (prev_height + 4) * TILE_SIZE, *TileSet.STONE, repeat_x=16, repeat_y=16),
        Tile(50 * TILE_SIZE, prev_height * TILE_SIZE, *TileSet.GLOOM_STONE, repeat_x=16, repeat_y=4, collidable=False, render_first=True),
    ])
    return tile_map, lights
