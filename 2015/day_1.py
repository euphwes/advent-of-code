from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2015

PART_ONE_DESCRIPTION = "floor"
PART_ONE_ANSWER = 138

PART_TWO_DESCRIPTION = "index of instruction where Santa enters the basement"
PART_TWO_ANSWER = 1771

paren_map = lambda char: 1 if char == "(" else -1


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(floor_instructions):
    return sum([paren_map(char) for char in floor_instructions])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(floor_instructions):
    floor = 0
    for i, val in enumerate([paren_map(char) for char in floor_instructions]):
        floor += val
        if floor < 0:
            return i + 1


# ----------------------------------------------------------------------------------------------


def run(input_file):

    floor_instructions = get_input(input_file)[0]

    part_one(floor_instructions)
    part_two(floor_instructions)
