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


def _run(program: list[int], prog_input: Generator[int] | None = None) -> Generator[list[int]]:
    computer = IntcodeComputer()
    while True:
        try:
            computer.execute(
                program,
                program_input=[next(prog_input)] if prog_input else None,
            )
            break
        except InputNotAvailableException:
            yield computer.get_all_output()

    yield computer.get_all_output()


def _get_field(
    program: list[int],
    prog_input: Generator[int] | None = None,
) -> dict[Coord, str]:
    for output_list in _run(program, prog_input):
        field: dict[Coord, str] = {}
        x = 0
        y = 0
        for char in output_list:
            if char != 10:
                field[(x, y)] = chr(char)
                x += 1
            else:
                x = 0
                y += 1
            print(chr(char), end="")
        print("\n===============\n")

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


def _provide_input(*, video_feed_on: bool = False) -> Generator[int]:
    newline = 10

    main_movement_routine = "A,B,C,A,B,C,A,B,C,A"
    routine_a = "L,9,R,9,L,9,R,9,L,9"
    routine_b = "R,9,R,9,L,9,L,9,L,9"
    routine_c = "L,9,L,9,R,9,R,9,R,9"

    yield from (ord(d) for d in main_movement_routine)
    yield newline

    yield from (ord(d) for d in routine_a)
    yield newline

    yield from (ord(d) for d in routine_b)
    yield newline

    yield from (ord(d) for d in routine_c)
    yield newline

    yield ord("y") if video_feed_on else ord("n")
    yield newline


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    # program = [int(x) for x in raw_input[0].split(",")]
    # field = _get_field(program)

    # Set the program to "run mode"
    program = [int(x) for x in raw_input[0].split(",")]
    assert program[0] == 1
    program[0] = 2

    _get_field(program, prog_input=_provide_input())


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    # part_two(get_input(input_file))

    # P2 complete movement without being broken up into routines yet
    #
    # L,6,R,12
    # L,6,R,12
    #
    # L,10,L,4,L,6
    #
    # L,6,R,12
    # L,6,R,12
    #
    # L,10,L,4,L,6    * bottom/left of top loop, definitely correct to here
    #
    # L,6,R,12
    #
    # L,6,L,10,L,10,L,4
    #
    # L,6,R,12
    #
    # L,10,L,4,L,6
    #
    # L,10
    #
    # L,10,L,4,L,6
    #
    # L,6,R,12
    #
    # L,6
    #
    # L,10
    #
    # L,10,L,4,L,6
    #
    # ##################
    #
    #
    # ## Scratch below for routines ##
    #
    # A: L,6,R,12
    # B:
    # C: L,10,L,4,L,6
