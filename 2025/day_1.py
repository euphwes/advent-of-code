from collections.abc import Generator

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2025

PART_ONE_DESCRIPTION = "number of times pointing at 0 after rotation"
PART_ONE_ANSWER = 1165

PART_TWO_DESCRIPTION = "number of times passing through or landing on 0"
PART_TWO_ANSWER = 6496


def _get_turns(raw_input: list[str]) -> Generator[int]:
    for line in raw_input:
        direction = line[0]
        value = int(line[1:])
        yield value if direction == "R" else (value * -1)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    dial = 50
    num_zeros = 0

    for value in _get_turns(raw_input):
        dial = (dial + value) % 100
        if dial == 0:
            num_zeros += 1

    return num_zeros


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    dial = 50
    num_zeros = 0

    for value in _get_turns(raw_input):
        neg = value < 0
        for _ in range(abs(value)):
            dial = (dial + (-1 if neg else 1)) % 100
            if dial == 0:
                num_zeros += 1

    return num_zeros


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
