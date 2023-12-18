from itertools import pairwise
from typing import List, Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.algs import manhattan_distance

DAY = 18
YEAR = 2023

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = 70026

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = 68548301037382


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    vertices = list()

    cx, cy = 0, 0
    vertices: List[Tuple[int, int]] = [(0, 0)]

    for line in stuff:
        direction, count, _ = line.split()
        count = int(count)

        if direction == "R":
            cx += count
        elif direction == "L":
            cx -= count
        elif direction == "U":
            cy -= count
        elif direction == "D":
            cy += count
        vertices.append((cx, cy))

    # shoelace theorem
    total = 0
    for p1, p2 in pairwise(vertices):
        x1, y1 = p1
        x2, y2 = p2
        deteriminant = (x1 * y2) - (x2 * y1)
        total += deteriminant

    return int(
        (total / 2)
        + (sum(manhattan_distance(p1, p2) for p1, p2 in pairwise(vertices)) / 2)
        + 1
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    vertices = list()

    cx, cy = 0, 0
    vertices: List[Tuple[int, int]] = [(0, 0)]

    for line in stuff:
        _, _, color = line.split()
        # count = int(count)
        color = color[2:-1]

        direction = dict(zip("0123", "RDLU"))[color[-1]]
        count = int(color[:-1], base=16)
        # print(direction, count)

        if direction == "R":
            cx += count
        elif direction == "L":
            cx -= count
        elif direction == "U":
            cy -= count
        elif direction == "D":
            cy += count

        vertices.append((cx, cy))

    # shoelace theorem
    total = 0
    for p1, p2 in pairwise(vertices):
        x1, y1 = p1
        x2, y2 = p2
        deteriminant = (x1 * y2) - (x2 * y1)
        total += deteriminant

    return int(
        (total / 2)
        + (sum(manhattan_distance(p1, p2) for p1, p2 in pairwise(vertices)) / 2)
        + 1
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    part_one(stuff)
    part_two(stuff)
