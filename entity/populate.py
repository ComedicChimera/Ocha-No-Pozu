from random import choices, randint
from util import TILE_SIZE
from entity.enemies.moth import Moth
from entity.enemies.spider import Spider
from entity.enemies.fire_skull import FireSkull
from map.tile import Tile
from entity.heart import Heart


entity_table = {
    1: (Moth, (3, 5)),
    2: (Spider, (2, 4)),
    3: (FireSkull, (3, 3))
}


def get_ground(tile_map):
    ground_positions = {}
    for tile in tile_map:
        if tile.damage > 0:
            continue
        if isinstance(tile, Tile):
            y_pos = tile.position.y + tile.repeat_y * TILE_SIZE
        else:
            y_pos = tile.position.y + tile.dimensions.y
        if tile.position.x in ground_positions:
            if ground_positions[tile.position.x] > y_pos:
                ground_positions[tile.position.x] = y_pos
        else:
            ground_positions[tile.position.x] = y_pos

    return list(ground_positions.values())


def populate(ground, area, entity_count, min_diff, max_diff):
    spawn_points = choices(range(area[0], area[1]), k=entity_count + 1)
    possible_entities = [v for k, v in entity_table.items() if min_diff <= k <= max_diff]
    entities = []
    for i in range(len(spawn_points)):
        if i == entity_count:
            entities.append(spawn_entity(spawn_points[i] * TILE_SIZE, (lambda x, y: Heart(x, y, 50), [0, 1]), ground[spawn_points[i]]))
        else:
            entities.append(spawn_entity(spawn_points[i] * TILE_SIZE, possible_entities[randint(0, len(possible_entities) - 1)], ground[spawn_points[i]]))
    return entities


def spawn_entity(x_pos, entity_tuple, floor):
    entity, y_range = entity_tuple
    return entity(x_pos, floor + randint(*y_range) * TILE_SIZE)



