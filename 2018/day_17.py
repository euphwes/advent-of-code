from collections import defaultdict
from typing import List, Set, Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import bidirectional_range

DAY = 17
YEAR = 2018

PART_ONE_DESCRIPTION = "Number of tiles the water can reach"
PART_ONE_ANSWER = 42429

PART_TWO_DESCRIPTION = "Settled water tiles left after spring stops"
PART_TWO_ANSWER = 35998

SAND = "."
CLAY = "#"
WATER = "~"
MOVING_WATER = "|"

WATER_SOURCE = (500, 0)


def _get_underground_map(underground_info):
    """Parses the input file and returns a dictionary of coordinates to what's there, starting
    with empty except where the input file specifies there is clay."""

    underground_map = defaultdict(lambda: ".")

    while underground_info:
        # Each line specifies a vertical or horizontal vein of clay
        wall_info = underground_info.pop(0)
        coords = wall_info.split(", ")

        first_chunk = coords[0]
        second_chunk = coords[1]

        if first_chunk[0] == "x":
            # vertical vein, fix x and iterate over y
            x = int(first_chunk.replace("x=", ""))
            start_y, stop_y = [
                int(n) for n in second_chunk.replace("y=", "").split("..")
            ]

            for y in bidirectional_range(start_y, stop_y, inclusive=True):
                underground_map[(x, y)] = CLAY

        else:
            # horizontal vein, fix y and iterate over x
            y = int(first_chunk.replace("y=", ""))
            start_x, stop_x = [
                int(n) for n in second_chunk.replace("x=", "").split("..")
            ]
            for x in bidirectional_range(start_x, stop_x, inclusive=True):
                underground_map[(x, y)] = CLAY

    return underground_map


def _fill_with_water(underground_map, lowest_y):
    """Given an underground map, simulates water falling from a source, filling up "containers"
    of veins of clay, until the water falls beyond the lowest point scanned underground.
    """

    sources_already_seen: Set[Tuple[int, int]] = set([WATER_SOURCE])
    water_sources: List[Tuple[int, int]] = [WATER_SOURCE]

    while water_sources:
        # Water falls in from the source
        source_to_start_from = water_sources.pop(0)
        water_x, water_y = source_to_start_from

        # Keeping making the water fall further down until it settles, or until the function
        # that decides if we should end the sim returns true.
        while True:
            # If the water is below the lowest point we've scanned, no need to simulate
            # this water source any further.
            if water_y >= lowest_y:
                break

            # Check if the water can fall straight down, and if so, move it that way.
            if underground_map[(water_x, water_y + 1)] in {SAND, MOVING_WATER}:
                water_y += 1
                underground_map[(water_x, water_y)] = MOVING_WATER
                continue

            # If the water can't fall, see if it can settle in the horizontal strip it's in.
            # That is, if the water is between 2 clay walls, each sand block in between those
            # becomes filled with settled water.

            # If the water can't fall down, it'll either settle in the horizontal row it's in,
            # or it'll overflow 1 or more sides. Check the boundaries of this row to figure
            # out what'll happen.
            left_bound_is_clay = True
            right_bound_is_clay = True
            left_boundary = None
            right_boundary = None

            # Start at the water's current x coord, look right until we find the boundary
            temp_x = water_x
            while True:
                temp_x += 1
                if underground_map[(temp_x, water_y)] == CLAY:
                    right_boundary = temp_x
                    break
                elif underground_map[(temp_x, water_y + 1)] in {SAND, MOVING_WATER}:
                    right_boundary = temp_x
                    right_bound_is_clay = False
                    # The water will overflow here -- let's consider this another water source
                    # tile to simulate.
                    if (temp_x, water_y) not in sources_already_seen:
                        sources_already_seen.add((temp_x, water_y))
                        water_sources.append((temp_x, water_y))
                        underground_map[(temp_x, water_y)] = MOVING_WATER
                    break

            # Start at the water's current x coord, look left until we find the boundary
            temp_x = water_x
            while True:
                temp_x -= 1
                if underground_map[(temp_x, water_y)] == CLAY:
                    left_boundary = temp_x
                    break
                elif underground_map[(temp_x, water_y + 1)] in {SAND, MOVING_WATER}:
                    left_boundary = temp_x
                    left_bound_is_clay = False
                    # The water will overflow here -- let's consider this another water source
                    # tile to simulate.
                    if (temp_x, water_y) not in sources_already_seen:
                        sources_already_seen.add((temp_x, water_y))
                        water_sources.append((temp_x, water_y))
                        underground_map[(temp_x, water_y)] = MOVING_WATER
                    break

            # See if the water can settle here because it's framed by 2 clay tiles.
            can_settle = left_bound_is_clay and right_bound_is_clay

            if can_settle:
                # If the water can settle here, fill the entire row between the clay tiles
                # with settled water, and then move up 1 y unit so we can check the next level
                # higher (water filling the container).
                for x in range(left_boundary + 1, right_boundary):
                    underground_map[(x, water_y)] = WATER
                water_y -= 1
                continue
            else:
                # If the water can't settle here because it'll overflow on one or more sides,
                # fill the row with "moving water" tiles indicating water can reach this point.
                x_left = left_boundary + 1 if left_bound_is_clay else left_boundary
                x_right = right_boundary if right_bound_is_clay else right_boundary + 1
                for x in range(x_left, x_right):
                    underground_map[(x, water_y)] = MOVING_WATER
                # We're overflowing from the container we're in, so stop simulating the water
                # falling from the current water source.
                break

    return underground_map


def _print_map(underground_map):
    """Utility function to print the map for debugging."""

    max_y = max(y for _, y in underground_map.keys())
    min_y = min(y for _, y in underground_map.keys())
    max_x = max(x for x, _ in underground_map.keys())
    min_x = min(x for x, _ in underground_map.keys())

    for y in range(min_y, max_y + 3):
        line = ""
        for x in range(min_x - 2, max_x + 2):
            line += underground_map.get((x, y), " ")
        print(line)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(underground_info):
    underground_map = _get_underground_map(underground_info)
    lowest_y = max(y for _, y in underground_map.keys())
    highest_y = min(y for _, y in underground_map.keys())

    filled_map = _fill_with_water(underground_map, lowest_y)
    # _print_map(filled_map)

    return sum(
        1
        for coord, material in filled_map.items()
        if highest_y <= coord[1] <= lowest_y and material in {WATER, MOVING_WATER}
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(underground_info):
    underground_map = _get_underground_map(underground_info)
    lowest_y = max(y for _, y in underground_map.keys())
    highest_y = min(y for _, y in underground_map.keys())

    filled_map = _fill_with_water(underground_map, lowest_y)
    _print_map(filled_map)

    return sum(
        1
        for coord, material in filled_map.items()
        if highest_y <= coord[1] <= lowest_y and material == WATER
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):
    underground_info = get_input(input_file)
    part_one(underground_info)

    underground_info = get_input(input_file)
    part_two(underground_info)
