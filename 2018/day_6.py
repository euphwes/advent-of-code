from collections import defaultdict

from util.algs import manhattan_distance
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

DAY = 6
YEAR = 2018

PART_ONE_DESCRIPTION = "size of largest non-infinite region"
PART_ONE_ANSWER = 5941

PART_TWO_DESCRIPTION = "size of region with total distance < 10k"
PART_TWO_ANSWER = 40244


def _get_nearest_coord(target_coord, coords_list):
    """For a given target coordinate, return the coordinate in the list which is closest (as
    measured by Manhattan distance), only if that coordinate is the *only* closest coordinate.
    If there is a tie for closest, nothing is closest."""

    distance_map = defaultdict(list)

    for anchor_coord in coords_list:
        distance = manhattan_distance(anchor_coord, target_coord)
        distance_map[distance].append(anchor_coord)

    min_distance = min(distance_map.keys())

    if len(distance_map[min_distance]) == 1:
        return distance_map[min_distance][0]
    else:
        return None


def _get_distance_sum(target_coord, coords_list):
    """For a given target coordinate, return the sum of the Manhattan distance between that
    target and all the coordinates in the provided list."""

    return sum(manhattan_distance(anchor, target_coord) for anchor in coords_list)


def _get_all_coords_in_region_bounded_by(coords):
    """Yield all coordinates in the smallest rectangle bounding the provided set of coords."""

    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)

    yield from nested_iterable(range(min_x, max_x + 1), range(min_y, max_y + 1))


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_coords):
    coords = set()

    for line in raw_coords:
        x, y = (int(n) for n in line.split(", "))
        coords.add((x, y))

    areas = defaultdict(list)

    for test_coord in _get_all_coords_in_region_bounded_by(coords):
        nearest_coord = _get_nearest_coord(test_coord, coords)
        if nearest_coord is None:
            continue

        areas[nearest_coord].append(test_coord)

    return max([len(area) for area in areas.values()])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_coords):
    coords = set()

    for line in raw_coords:
        x, y = (int(n) for n in line.split(", "))
        coords.add((x, y))

    region = 0
    for test_coord in _get_all_coords_in_region_bounded_by(coords):

        distance_sum = _get_distance_sum(test_coord, coords)
        if distance_sum < 10000:
            region += 1

    return region


# ----------------------------------------------------------------------------------------------


def run(input_file):

    raw_coords = get_input(input_file)

    part_one(raw_coords)
    part_two(raw_coords)
