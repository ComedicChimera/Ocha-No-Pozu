from map.tile import *
from util import TILE_SIZE
from random import randint
from render.lighting import Light


def generate_lava_cave_gaps():
    top, bottom, ceil_height = 8, 6, 15
    tile_map, counter, gap, lights, prev_height = [], 6, True, [], 6
    while counter < 80:
        if gap:
            gap_len = randint(3, 4)
            tile_map.extend([
                Tile(counter * TILE_SIZE, 3 * TILE_SIZE, *TileSet.LAVA, repeat_x=gap_len, repeat_y=2, collidable=False, damage=100),
                Tile(counter * TILE_SIZE, 0, *TileSet.STONE, repeat_x=gap_len, repeat_y=3)
            ])
            lights.append(Light((counter + gap_len // 2 - 8) * TILE_SIZE, 104, (255, 209, 191), 16))
            counter += gap_len
        else:
            plat_len = randint(1, 3)
            for i in range(plat_len):
                height = prev_height + randint(-1, 1)
                if height > top:
                    height = prev_height - 1
                elif height < bottom:
                    height = prev_height + 1
                tile_map.append(Tile((counter + i) * TILE_SIZE, 0, *TileSet.STONE, repeat_y=height))
                prev_height = height
            counter += plat_len
        gap = not gap

    tile_map.append(Tile(0, ceil_height * TILE_SIZE, *TileSet.STONE, repeat_x=counter, repeat_y=16))

    for i in range(1, counter):
        s_height = randint(0, 3)
        tile_map.append(Tile(i * TILE_SIZE, (ceil_height - s_height) * TILE_SIZE, *TileSet.STONE, repeat_y=s_height))
        if randint(0, 2) == 0:
            tile_map.append(Tile(i * TILE_SIZE, ((ceil_height - 1) - s_height) * TILE_SIZE, *TileSet.STALACTITE))

    for i in reversed(range(0, 3)):
        tile_map.extend([
            Tile((i * 2 + counter) * TILE_SIZE, 0, *TileSet.STONE, repeat_x=2, repeat_y=(5 + i)),
            Tile((i * 2 + counter) * TILE_SIZE, (14 - i) * TILE_SIZE, *TileSet.STONE, repeat_x=2, repeat_y=16)
        ])
    counter += 5
    tile_map.extend([
        Tile(counter * TILE_SIZE, 0, *TileSet.STONE, repeat_x=14, repeat_y=8),
        Tile(counter * TILE_SIZE, 8 * TILE_SIZE, *TileSet.GLOOM_STONE, repeat_x=14, repeat_y=3, collidable=False),
        Tile(counter * TILE_SIZE, 11 * TILE_SIZE, *TileSet.STONE, repeat_x=14, repeat_y=18)
    ])

    return tile_map, lights
