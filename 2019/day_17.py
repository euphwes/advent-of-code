from collections.abc import Generator

from util.decorators import aoc_output_formatter
from util.input import get_input

from .intcode import InputNotAvailableException, IntcodeComputer

DAY = 17
YEAR = 2019

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


Coord = tuple[int, int]

SPACE = "."
SCAFFOLD = "#"


def _run(program: list[int]) -> Generator[list[int]]:
    computer = IntcodeComputer()
    while True:
        try:
            computer.execute(program, program_input=None)
            break
        except InputNotAvailableException:
            yield computer.get_all_output()

    yield computer.get_all_output()


def _get_field(program: list[int]) -> dict[Coord, str]:
    field: dict[Coord, str] = {}

    x = 0
    y = 0

    for output_list in _run(program):
        for char in output_list:
            if char != 10:
                field[(x, y)] = chr(char)
                x += 1
            else:
                x = 0
                y += 1

    return field


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    program = [int(x) for x in raw_input[0].split(",")]
    field = _get_field(program)

    intersections: set[Coord] = set()
    for c, char in field.items():
        cx, cy = c
        if char == SCAFFOLD and all(
            field.get((nx, ny)) == SCAFFOLD
            for nx, ny in [
                (cx - 1, cy),
                (cx + 1, cy),
                (cx, cy + 1),
                (cx, cy - 1),
            ]
        ):
            intersections.add(c)

    return sum(x * y for x, y in intersections)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    pass


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
