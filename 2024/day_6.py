from copy import copy
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 6
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

dir_deltas = {
    0: (1, 0),  # right
    1: (0, 1),  # down
    2: (-1, 0),  # left
    3: (0, -1),  # up
}


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    direction = 3
    loc = -1, -1

    field = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            field[(x, y)] = char
            if char == "^":
                loc = (x, y)
                field[loc] = "."
                loc = (x, y)

    assert loc != (-1, -1)

    x, y = loc
    positions = set()

    while True:
        positions.add((x, y))
        dx, dy = dir_deltas[direction]

        if (front := field.get((x + dx, y + dy), None)) == None:
            break

        if front == "#":
            direction = (direction + 1) % 4
        else:
            x += dx
            y += dy

    return len(positions)


def _does_cycle(start, field_orig, new_obstruction_loc):
    field = copy(field_orig)
    field[new_obstruction_loc] = "#"

    direction = 3

    x, y = start
    positions_and_dirs = set()

    while True:
        if (x, y, direction) in positions_and_dirs:
            return True

        positions_and_dirs.add((x, y, direction))

        dx, dy = dir_deltas[direction]

        if (front := field.get((x + dx, y + dy), None)) == None:
            return False

        if front == "#":
            direction = (direction + 1) % 4
        else:
            x += dx
            y += dy


def _positions_visited(start, field):
    direction = 3
    x, y = start
    positions = set()

    while True:
        positions.add((x, y))
        dx, dy = dir_deltas[direction]

        if (front := field.get((x + dx, y + dy), None)) == None:
            break

        if front == "#":
            direction = (direction + 1) % 4
        else:
            x += dx
            y += dy

    return positions


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    loc = -1, -1

    field = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            field[(x, y)] = char
            if char == "^":
                loc = (x, y)
                field[loc] = "."
                loc = (x, y)

    assert loc != (-1, -1)

    c = 0

    for ob_loc in _positions_visited(loc, field):
        if ob_loc == loc:
            continue
        if _does_cycle(loc, field, ob_loc):
            c += 1

    return c


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)
