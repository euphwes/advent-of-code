from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable
from util.structures import get_neighbors_of

from functools import reduce

#---------------------------------------------------------------------------------------------------

def _find_basin(x, y, heightmap, lowpoints, point_to_basin_map):
    """ For a given point (x, y), heightmap and lowpoints, find the low point which identifies the
    basin to which it flows. """

    # Get all of this point's neighbors at once.
    neighbors = list(get_neighbors_of(x, y, heightmap, include_diagonals=False, with_coords=True))

    # Check each neighbor to see if it's the basin, or if we know the basin to which it belongs.
    for neighbor, coord in neighbors:
        # If we already know the basin that this neighbor belongs to, the point being checked also
        # belongs to the same basin.
        if coord in point_to_basin_map.keys():
            return point_to_basin_map[coord]

        # If the neighbor is a known lowpoint, it defines the basin! Return the lowpoint neighbor
        if coord in lowpoints:
            return coord

    # If checking the neighbors didn't immediately reveal the basin, "flow down" by finding the
    # smallest neighboring point and recursively callind _find_basin on it.
    smallest_neighbor = min(neighbors, key=lambda n: n[0])
    neighbor_coords = smallest_neighbor[1]
    x, y = neighbor_coords[0], neighbor_coords[1]

    return _find_basin(x, y, heightmap, lowpoints, point_to_basin_map)


def _get_low_points(heightmap):
    """ Returns a dictionary (coordinate to value) all low points in the heightmap. A low point is
    any point which is lower than any of its immediate neighbors. """

    lowpoints = dict()

    for x, y in nested_iterable(range(len(heightmap[0])), range(len(heightmap))):
        value = heightmap[y][x]

        # If the value is lower than all of its neighbors, it's a low point on the map.
        neighbors = list(get_neighbors_of(x, y, heightmap, include_diagonals=False))
        if all(value < n for n in neighbors):
            lowpoints[(x, y)] = value

    return lowpoints


@aoc_output_formatter(2021, 9, 1, 'sum of risk levels of all low points')
def part_one(heightmap):
    return sum(1 + value for value in _get_low_points(heightmap).values())


@aoc_output_formatter(2021, 9, 2, 'product of sizes of three largest basins')
def part_two(heightmap):
    basins = {}

    # Get the coordinates of all the low points
    lowpoints = _get_low_points(heightmap).keys()

    # Track a basins dictionary where the key is the lowpoint of that basin, and the value is a
    # set of all points in that basin.
    basins_map = {lowpoint: set() for lowpoint in lowpoints}

    # Separately keep a map of points to which basins they occupy. This will reduce the basin search
    # space later, since a given point's smaller neighbor's basin might already been known, and
    # they'll belong to the same basin.
    point_to_basin_map = dict()

    for x, y in nested_iterable(range(len(heightmap[0])), range(len(heightmap))):
        # 9 is the hightest, those are basin borders and don't belong in any basin
        if heightmap[y][x] == 9:
            continue

        # A lowpoint defines its own basin, add it and contnue
        if (x, y) in lowpoints:
            basins_map[(x, y)].add((x, y))
            continue

        # Find the coordinate of the lowpoint which define the basin this point is in, and track
        # it as belong ing to that basin.
        basin = _find_basin(x, y, heightmap, lowpoints, point_to_basin_map)
        basins_map[basin].add((x, y))
        point_to_basin_map[(x, y)] = basin

    # Calculate all the basin sizes, and select the biggest three
    basin_sizes = [len(points) for points in basins_map.values()]
    biggest_basins = sorted(basin_sizes)[-3:]

    # Return the product of the biggest three basins
    return reduce(lambda a, b: a*b, biggest_basins)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    lines = [line for line in get_input(input_file)]
    heightmap = list()
    for line in lines:
        line = list(line)
        heightmap.append([int(x) for x in line])

    part_one(heightmap)
    part_two(heightmap)
