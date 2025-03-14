import re
from math import prod

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 3
YEAR = 2024

PART_ONE_DESCRIPTION = "sum of all multiplication instructions"
PART_ONE_ANSWER = 191183308

PART_TWO_DESCRIPTION = "sum of all enabled multiplication instructions"
PART_TWO_ANSWER = 92082041


def _evaluate_mul(raw_instruction: str) -> int:
    """Evaluate a raw "mul(n, m)" instruction, returning n*m."""

    return prod(int(n) for n in raw_instruction[4:-1].split(","))


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return sum(
        _evaluate_mul(match)
        for line in raw_input
        # Extract matches of "mul(n, m)" in each line of the input
        for match in re.findall(r"mul\(\d{1,3}\,\d{1,3}\)", line)
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    n = 0

    enabled = True
    for line in raw_input:
        # Extract matches of "mul(n, m)", "do()", and "don't()"
        for match in re.findall(r"mul\(\d{1,3}\,\d{1,3}\)|do\(\)|don't\(\)", line):
            # If the match is "do()", enable any following multiplication matches
            if match == "do()":
                enabled = True
                continue

            # If the match is "don't()", disable any following multiplication matches
            if match == "don't()":
                enabled = False
                continue

            # Only sum the product of a "mul(n, m)" match if multiplication is enabled
            n += _evaluate_mul(match) if enabled else 0

    return n


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
