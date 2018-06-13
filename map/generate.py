import map.tile as tile
from util import Point2D


def generate_easy_over_world():
    tile_map = [tile.Tile(Point2D(0, 0), *tile.TileSet.DIRT, 40, 2), tile.Tile(Point2D(0, 2), *tile.TileSet.GRASS, 40)]
    return tile_map

