from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 4
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    n = 0

    charmap = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            charmap[(x, y)] = char

    dir_deltas = [
        (1, 0),  # right
        (-1, 0),  # left
        (0, -1),  # up
        (0, 1),  # down
        (1, 1),  # DR
        (1, -1),  # UR
        (-1, 1),  # DL
        (-1, -1),  # UL
    ]

    for coord, char in charmap.items():
        if char != "X":
            continue
        x, y = coord
        for dx, dy in dir_deltas:
            (c2, c3, c4) = (
                charmap.get((x + dx, y + dy), ""),
                charmap.get((x + 2 * dx, y + 2 * dy), ""),
                charmap.get((x + 3 * dx, y + 3 * dy), ""),
            )
            if (c2, c3, c4) == ("M", "A", "S"):
                n += 1

    return n


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    n = 0

    charmap = dict()
    for y, line in enumerate(stuff):
        for x, char in enumerate(line):
            charmap[(x, y)] = char

    dir_deltas_pairs = [
        # [
        #     [
        #         (1, 0),  # right
        #         (-1, 0),  # left
        #     ],
        #     [
        #         (0, -1),  # up
        #         (0, 1),  # down
        #     ],
        # ],
        [
            [
                (1, 1),  # DR
                (-1, -1),  # UL
            ],
            [
                (-1, 1),  # DL
                (1, -1),  # UR
            ],
        ],
    ]

    for coord, char in charmap.items():
        if char != "A":
            continue

        x, y = coord
        for p1, p2 in dir_deltas_pairs:
            d1, d2 = p1
            d3, d4 = p2
            d1x, d1y = d1
            d2x, d2y = d2
            d3x, d3y = d3
            d4x, d4y = d4

            one_dir = charmap.get((x + d1x, y + d1y), "") + charmap.get(
                (x + d2x, y + d2y), ""
            )
            other_dir = charmap.get((x + d3x, y + d3y), "") + charmap.get(
                (x + d4x, y + d4y), ""
            )

            if one_dir in ("SM", "MS") and other_dir in ("SM", "MS"):
                n += 1

    return n


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    # 2504 right
    part_one(stuff)

    stuff = get_input(input_file)
    # 1946 too high
    part_two(stuff)
