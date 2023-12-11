from util.decorators import aoc_output_formatter
from util.input import get_input

from itertools import combinations

DAY = 11
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of distances between galaxy pairs"
PART_ONE_ANSWER = 10289334

PART_TWO_DESCRIPTION = "sum of distances between galaxy pairs with huge expansion"
PART_TWO_ANSWER = 649862989626


def _get_x_y_coordinates_expanded(space_chart):
    """Returns a tuple of the sets of x and y coordinates which are subject to spacetime
    expansion because those rows or columns are only empty space."""

    y_to_expand = set()
    for y, line in enumerate(space_chart):
        if all(c == "." for c in line):
            y_to_expand.add(y)

    x_to_expand = set()
    for x in range(len(space_chart[0])):
        if all(line[x] == "." for line in space_chart):
            x_to_expand.add(x)

    return (x_to_expand, y_to_expand)


def _get_coords_of_galaxies(space_chart):
    """Returns a set of (x, y) coords of all the galaxies in the space chart."""

    galaxy_coords = set()
    for y, line in enumerate(space_chart):
        for x, char in enumerate(line):
            if char == "#":
                galaxy_coords.add((x, y))

    return galaxy_coords


def _galaxy_distance(galaxy1, galaxy2, x_to_expand, y_to_expand, expansion_factor):
    """Modified Manhattan distance algorithm which accounts for the expansion of space."""

    x1, y1 = galaxy1
    x2, y2 = galaxy2

    # Some x and y values are subject to be expanded by a certain factor.
    # Count each of the x and y values that you must cross to navigate from galaxy 1
    # to galaxy 2. Rather than counting crossing that space as a distance of 1, we'll count it
    # as a distance of `expansion_factor`.

    min_x, max_x = min([x1, x2]), max([x1, x2])
    min_y, max_y = min([y1, y2]), max([y1, y2])

    num_x_expansions = len([x for x in x_to_expand if x > min_x and x <= max_x])
    num_y_expansions = len([y for y in y_to_expand if y > min_y and y <= max_y])
    total_expansions = num_x_expansions + num_y_expansions

    # For each "expansion", add `expansion_factor - 1` to the total distance, because 1 of
    # those units we already covered with the standard Manhattan distance calculation.
    additional_space_traversed = (expansion_factor - 1) * total_expansions

    return abs(x1 - x2) + abs(y1 - y2) + additional_space_traversed


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(space_chart):
    x_to_expand, y_to_expand = _get_x_y_coordinates_expanded(space_chart)
    galaxy_coords = _get_coords_of_galaxies(space_chart)

    return sum(
        _galaxy_distance(galaxy1, galaxy2, x_to_expand, y_to_expand, 2)
        for galaxy1, galaxy2 in combinations(galaxy_coords, 2)
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(space_chart):
    x_to_expand, y_to_expand = _get_x_y_coordinates_expanded(space_chart)
    galaxy_coords = _get_coords_of_galaxies(space_chart)

    return sum(
        _galaxy_distance(galaxy1, galaxy2, x_to_expand, y_to_expand, 1_000_000)
        for galaxy1, galaxy2 in combinations(galaxy_coords, 2)
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):
    space_chart = get_input(input_file)
    part_one(space_chart)
    part_two(space_chart)
