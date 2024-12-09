from collections import defaultdict
from itertools import combinations
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 8
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    signal_map = dict()
    antinode_map = dict()
    signal_positions = defaultdict(list)

    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            antinode_map[(x, y)] = False

            if char != ".":
                signal_map[(x, y)] = char
                signal_positions[char].append((x, y))

    for signal, positions in signal_positions.items():
        for p1, p2 in combinations(positions, 2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            ac1 = ((p1[0] - dx), (p1[1] - dy))
            ac2 = ((p2[0] + dx), (p2[1] + dy))

            if ac1 in antinode_map.keys():
                antinode_map[ac1] = True

            if ac2 in antinode_map.keys():
                antinode_map[ac2] = True

    return sum(1 for v in antinode_map.values() if v)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    signal_map = dict()
    antinode_map = dict()
    signal_positions = defaultdict(list)

    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            antinode_map[(x, y)] = False

            if char != ".":
                antinode_map[(x, y)] = True
                signal_map[(x, y)] = char
                signal_positions[char].append((x, y))

    for signal, positions in signal_positions.items():
        for p1, p2 in combinations(positions, 2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            # going left
            for i in int_stream(1):
                ac = ((p1[0] - (i * dx)), (p1[1] - (i * dy)))
                if ac in antinode_map.keys():
                    antinode_map[ac] = True
                else:
                    break

            # going right
            for i in int_stream(1):
                ac = ((p2[0] + (i * dx)), (p2[1] + (i * dy)))
                if ac in antinode_map.keys():
                    antinode_map[ac] = True
                else:
                    break

    return sum(1 for v in antinode_map.values() if v)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)

    stuff = get_input(input_file)
    part_two(stuff)
