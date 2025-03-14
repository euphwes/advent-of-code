from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2015

PART_ONE_DESCRIPTION = "floor"
PART_ONE_ANSWER = 138

PART_TWO_DESCRIPTION = "index of instruction where Santa enters the basement"
PART_TWO_ANSWER = 1771


def paren_map(char: str) -> int:
    return 1 if char == "(" else -1


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return sum([paren_map(char) for char in raw_input[0]])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    floor_instructions = raw_input[0]

    index = 0
    floor = 0
    for i, val in enumerate([paren_map(char) for char in floor_instructions]):
        index = i
        floor += val

        if floor < 0:
            break

    return index + 1


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
