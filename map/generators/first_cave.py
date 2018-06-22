from map.tile import *
from random import choice, randint
from util import TILE_SIZE, HEIGHT
from render.lighting import Light


def generate_first_cave():
    top, bottom = 6, 3
    prev_height = 4
    tile_map, lights = [], []
    for i in range(30):
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
            elif i % randint(4, 7) == 0:
                x_shift = randint(0, 1)
                tile_map.append(SpriteTile('torch.png', (i + x_shift) * TILE_SIZE, height * TILE_SIZE,
                                           TILE_SIZE, TILE_SIZE, frames=5, render_first=True))
                lights.append(Light((i + x_shift - 10) * TILE_SIZE + 16, HEIGHT - ((height + 10) * TILE_SIZE) - 16, (255, 240, 193), 20))
        hgt = choice([2, 3, 4])
        if randint(0, 1) == 0:
            tile_map.append(Tile(i * TILE_SIZE, HEIGHT - hgt * TILE_SIZE, *TileSet.STALACTITE, collidable=False))
        tile_map.append(Tile(i * TILE_SIZE, HEIGHT - (hgt - 1) * TILE_SIZE, *TileSet.STONE, repeat_y=hgt))

    return tile_map, lights
