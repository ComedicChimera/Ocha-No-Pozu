from entity.entity import Entity


class BoundingBox:
    def __init__(self, x, y, width, height):
        self.left, self.bottom = x, y
        self.right, self.top = x + width, y + height

    def get_property_list(self):
        return {self.left, self.bottom, self.right, self.top}


def _create_bounding_box(game_object):
    # generate entity
    if isinstance(game_object, Entity):
        dimensions = game_object.dimensions()
        return BoundingBox(game_object.position.x, game_object.position.y, dimensions.x, dimensions.y)
    # generate tile
    else:
        dimensions = (16 * game_object.repeat_x, 16 * game_object.repeat_y)
        return BoundingBox(game_object.position.x * 16, game_object.position.y * 16, *dimensions)


def _get_collidable_boxes(e):
    return [_create_bounding_box(x) for x in e if x.collidable]


def calculate_collisions(entity, others):
    collisions = []
    entity_box = _create_bounding_box(entity)
    for other in _get_collidable_boxes(others):
        if any(ep == op for ep, op in zip(entity_box.get_property_list(), other.get_property_list())):
            collisions.append(other)
    return collisions


def calculate_y_base(entity, others):
    y_base = 0
    entity_box = _create_bounding_box(entity)
    for other in _get_collidable_boxes(others):
        if entity_box.bottom >= other.top > y_base and other.left <= entity_box.left and other.right >= entity_box.right:
            y_base = other.top
    return y_base
