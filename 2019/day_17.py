from collections.abc import Generator

from util.decorators import aoc_output_formatter
from util.input import get_input

from .intcode import InputNotAvailableException, IntcodeComputer

DAY = 17
YEAR = 2019

PART_ONE_DESCRIPTION = "sum of alignment params for scaffold intersections"
PART_ONE_ANSWER = 8928

PART_TWO_DESCRIPTION = "total dust collected by robot"
PART_TWO_ANSWER = 880360


Coord = tuple[int, int]

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
        #     print(chr(char), end="")
        # print("\n===============\n")

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


def _provide_input() -> Generator[int]:
    newline = 10

    # ######################################
    # Solution, done by hand against the map
    # because I felt like doing it that way
    # ######################################
    #
    # A: L,6,R,12,L,6
    # B: R,12,L,10,L,4,L,6
    # C: L,10,L,10,L,4,L,6
    #
    # main routine
    # A,B,A,B,A,C,B,C,A,C

    main_movement_routine = "A,B,A,B,A,C,B,C,A,C"
    routine_a = "L,6,R,12,L,6"
    routine_b = "R,12,L,10,L,4,L,6"
    routine_c = "L,10,L,10,L,4,L,6"

    yield from (ord(d) for d in main_movement_routine)
    yield newline

    yield from (ord(d) for d in routine_a)
    yield newline

    yield from (ord(d) for d in routine_b)
    yield newline

    yield from (ord(d) for d in routine_c)
    yield newline

    yield ord("n")  # no live video feed
    yield newline


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    # Set the program to "run mode"
    program = [int(x) for x in raw_input[0].split(",")]
    program[0] = 2

    # A lot of this output is just the initial state of the map, in ascii codes.
    # Discard all of it and just return the very final output value from the
    # program which is the dust collected.
    all_output = []
    for output_list in _run(program, _provide_input()):
        all_output.extend(output_list)
    return all_output[-1]


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))

    # Total movement solution, written manually by hand-tracing the map from part 1
    #
    # L,6,R,12,L,6,R,12,L,10,L,4,L,6,L,6,R,12,L,6,R,12,L,10,L,4,L,6,L,6,R,12,L,6,L,10,L,10,L,4,L,6,R,12,L,10,L,4,L,6,L,10,L,10,L,4,L,6,L,6,R,12,L,6,L,10,L,10,L,4,L,6
    #
    # If...
    # A: L,6,R,12,L,6
    #
    # Replace A
    # A,R,12,L,10,L,4,L,6,A,R,12,L,10,L,4,L,6,A,L,10,L,10,L,4,L,6,R,12,L,10,L,4,L,6,L,10,L,10,L,4,L,6,A,L,10,L,10,L,4,L,6
    #
    # Take out A and see what's left
    # R,12,L,10,L,4,L,6,R,12,L,10,L,4,L,6,L,10,L,10,L,4,L,6,R,12,L,10,L,4,L,6,L,10,L,10,L,4,L,6,L,10,L,10,L,4,L,6
    #
    # B: R,12,L,10,L,4,L,6
    #
    # Replace B
    # B,B,L,10,L,10,L,4,L,6,B,L,10,L,10,L,4,L,6,L,10,L,10,L,4,L,6
    #
    # Take out B and see what's left
    # L,10,L,10,L,4,L,6,L,10,L,10,L,4,L,6,L,10,L,10,L,4,L,6
    #
    # C: L,10,L,10,L,4,L,6
    #
    # ########################
    # Solution
    # ########################
    #
    # A: L,6,R,12,L,6
    # B: R,12,L,10,L,4,L,6
    # C: L,10,L,10,L,4,L,6
    #
    # main routine becomes
    # A,B,A,B,A,C,B,C,A,C
