from collections import defaultdict
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 14
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

EMPTY = "."
ROUND_ROCK = "O"
SQUARE_ROCK = "#"
ALL_ROCKS = set("O#")


def _can_slide_north(rock_map, rock_coord):
    rx, ry = rock_coord
    above = (rx, ry - 1)

    above_char = rock_map.get(above, SQUARE_ROCK)
    return above_char == EMPTY


def _can_slide_west(rock_map, rock_coord):
    rx, ry = rock_coord
    left = (rx - 1, ry)

    left_char = rock_map.get(left, SQUARE_ROCK)
    return left_char == EMPTY


def _can_slide_south(rock_map, rock_coord):
    rx, ry = rock_coord
    below = (rx, ry + 1)

    below_char = rock_map.get(below, SQUARE_ROCK)
    return below_char == EMPTY


def _can_slide_east(rock_map, rock_coord):
    rx, ry = rock_coord
    right = (rx + 1, ry)

    right_char = rock_map.get(right, SQUARE_ROCK)
    return right_char == EMPTY


def _tilt_north(rock_map, height, width):
    # For each column... start at the highest Y and move any rocks up until it won't go
    # any further. Then go to the next Y and do the same.

    for rx in range(width):
        for ry in range(height):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue

            while _can_slide_north(rock_map, (rx, ry)):
                rock_map[(rx, ry)] = EMPTY
                ry -= 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _tilt_west(rock_map, height, width):
    for ry in range(height):
        for rx in range(width):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue

            while _can_slide_west(rock_map, (rx, ry)):
                rock_map[(rx, ry)] = EMPTY
                rx -= 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _tilt_south(rock_map, height, width):
    for rx in reversed(range(width)):
        for ry in reversed(range(height)):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue

            while _can_slide_south(rock_map, (rx, ry)):
                rock_map[(rx, ry)] = EMPTY
                ry += 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _tilt_east(rock_map, height, width):
    for ry in reversed(range(height)):
        for rx in reversed(range(width)):
            maybe_rock = rock_map[(rx, ry)]
            if maybe_rock != ROUND_ROCK:
                continue

            while _can_slide_east(rock_map, (rx, ry)):
                rock_map[(rx, ry)] = EMPTY
                rx += 1
                rock_map[(rx, ry)] = ROUND_ROCK


def _spin_cycle(rock_map, height, width):
    _tilt_north(rock_map, height, width)
    _tilt_west(rock_map, height, width)
    _tilt_south(rock_map, height, width)
    _tilt_east(rock_map, height, width)


def _render_rocks(rock_map, height, width):
    print()
    for y in range(height):
        line = []
        for x in range(width):
            line.append(rock_map[(x, y)])
        line = "".join(line)
        print(line)


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

    # _render_rocks(rock_map, height, width)

    _tilt_north(rock_map, height, width)

    # _render_rocks(rock_map, height, width)

    return _calculate_load(rock_map, height, width)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    rock_map = dict()

    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            rock_map[(x, y)] = char

    height = len(stuff)
    width = len(stuff[0])

    # _render_rocks(rock_map, height, width)

    seen_rock_sets_cycle_nums = defaultdict(list)
    cycle_size = -1
    r = -1

    for r in range(1_000_000_000):
        _spin_cycle(rock_map, height, width)

        rock_set = frozenset(c for c, r in rock_map.items() if r == ROUND_ROCK)
        seen_rock_sets_cycle_nums[rock_set].append(r)

        if len(seen_rock_sets_cycle_nums[rock_set]) > 1:
            rs = seen_rock_sets_cycle_nums[rock_set]
            print(f"{rs=}")
            cycle_size = max(rs) - min(rs)
            break

    print(f"{r=}")
    print(f"{cycle_size=}")

    while r < 1_000_000_000:
        r += cycle_size
    r -= cycle_size

    for _ in range(r + 1, 1_000_000_000):
        _spin_cycle(rock_map, height, width)

    return _calculate_load(rock_map, height, width)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)
