from entity.entity import Entity
from map.tile import SpriteTile
from util import TILE_SIZE, MAP_SIZE_X, MAP_SIZE_Y
from entity.physics import Range, BoundingBox


def _create_bounding_box(game_object):
    # generate entity
    if isinstance(game_object, Entity):
        dimensions = game_object.dimensions()
        return BoundingBox(game_object.position.x, game_object.position.y, dimensions.x, dimensions.y)
    # generate sprite tile
    elif isinstance(game_object, SpriteTile):
        return BoundingBox(game_object.position.x, game_object.position.y, game_object.dimensions.x, game_object.dimensions.y)
    # generate tile
    else:
        dimensions = (TILE_SIZE * game_object.repeat_x, TILE_SIZE * game_object.repeat_y)
        return BoundingBox(game_object.position.x, game_object.position.y, *dimensions)


def _get_collidable_boxes(obj_list, fn):
    return [x for x in map(lambda e: _create_bounding_box(e), [e for e in obj_list if e.collidable]) if fn(x)]


def calculate_x_range(entity, others):
    rng, entity_box = Range(MAP_SIZE_X), _create_bounding_box(entity)

    def fn(x): return x.bottom <= entity_box.bottom < x.top or x.bottom < entity_box.top <= x.top
    for other in _get_collidable_boxes(others, fn):
        if entity_box.left >= other.right > rng.min:
            rng.min = other.right
        elif entity_box.right <= other.left < rng.max:
            rng.max = other.left
    return rng


def calculate_y_range(entity, others):
    rng, entity_box = Range(MAP_SIZE_Y), _create_bounding_box(entity)

    def fn(x): return x.left <= entity_box.left < x.right or x.left < entity_box.right < x.right

    for other in _get_collidable_boxes(others, fn):
        if entity_box.bottom >= other.top > rng.min:
            rng.min = other.top
        elif entity_box.top <= other.bottom < rng.max:
            rng.max = other.bottom
    return rng
