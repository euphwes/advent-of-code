from collections import defaultdict
from enum import Enum
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 14
YEAR = 2023

PART_ONE_DESCRIPTION = "total load on north support beams"
PART_ONE_ANSWER = 103614

PART_TWO_DESCRIPTION = "total load on north support beams after 1B spin cycles"
PART_TWO_ANSWER = 83790

EMPTY = "."
ROUND_ROCK = "O"
SQUARE_ROCK = "#"
ALL_ROCKS = set("O#")


class Direction(Enum):
    N = "n"
    E = "e"
    S = "s"
    W = "w"


direction_map = {
    Direction.N: (0, -1),
    Direction.S: (0, 1),
    Direction.E: (1, 0),
    Direction.W: (-1, 0),
}


def _can_slide(rock_map, rock_coord, direction):
    rx, ry = rock_coord
    dx, dy = direction_map[direction]

    return rock_map.get((rx + dx, ry + dy), "#") == EMPTY


# The _tilt_<direction> functions below could all be made less redundant
# by accepting a direction parameter and working off that... but I don't wanna.


def _tilt_north(rock_map, height, width):
    for rx in range(width):
        for ry in range(height):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue

            while _can_slide(rock_map, (rx, ry), Direction.N):
                rock_map[(rx, ry)] = EMPTY
                ry -= 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _tilt_west(rock_map, height, width):
    for ry in range(height):
        for rx in range(width):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue

            while _can_slide(rock_map, (rx, ry), Direction.W):
                rock_map[(rx, ry)] = EMPTY
                rx -= 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _tilt_south(rock_map, height, width):
    for rx in reversed(range(width)):
        for ry in reversed(range(height)):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue

            while _can_slide(rock_map, (rx, ry), Direction.S):
                rock_map[(rx, ry)] = EMPTY
                ry += 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _tilt_east(rock_map, height, width):
    for ry in reversed(range(height)):
        for rx in reversed(range(width)):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue
            while _can_slide(rock_map, (rx, ry), Direction.E):
                rock_map[(rx, ry)] = EMPTY
                rx += 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _spin_cycle(rock_map, height, width):
    _tilt_north(rock_map, height, width)
    _tilt_west(rock_map, height, width)
    _tilt_south(rock_map, height, width)
    _tilt_east(rock_map, height, width)


def _calculate_load(rock_map, height, width):
    total_load = 0
    for y in range(height):
        for x in range(width):
            char = rock_map[(x, y)]
            if char == ROUND_ROCK:
                total_load += height - y

    return total_load


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    rock_map = dict()

    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            rock_map[(x, y)] = char

    height = len(stuff)
    width = len(stuff[0])

    _tilt_north(rock_map, height, width)

    return _calculate_load(rock_map, height, width)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    rock_map = dict()

    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            rock_map[(x, y)] = char

    height = len(stuff)
    width = len(stuff[0])

    seen_rock_sets_cycle_nums = defaultdict(list)
    cycle_size = -1
    r = -1

    # Start by running spin cycles over and over...
    for r in range(1_000_000_000):
        _spin_cycle(rock_map, height, width)

        # ... recording the state of where all the round rocks are after each
        rock_set = frozenset(c for c, r in rock_map.items() if r == ROUND_ROCK)
        seen_rock_sets_cycle_nums[rock_set].append(r)

        # If we've seen this specific state of rock locations before, we've entered
        # cycle. We can see the size of the cycle by subtracting this spin cycle number
        # from the first time we saw this rock arrangement.
        if len(seen_rock_sets_cycle_nums[rock_set]) > 1:
            rs = seen_rock_sets_cycle_nums[rock_set]
            cycle_size = rs[1] - rs[0]
            break

    # Because we're in a cycle now, we can keep skipping ahead by `cycle_size`
    # spin cycles because we know the rock arrangements will stay the same.
    # Do that and get as close to 1B as possible.
    while r < 1_000_000_000:
        r += cycle_size
    r -= cycle_size

    # Simulate the last little bit to reach 1B spin cycles
    for _ in range(r + 1, 1_000_000_000):
        _spin_cycle(rock_map, height, width)

    return _calculate_load(rock_map, height, width)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)
