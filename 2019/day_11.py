from collections import defaultdict
from typing import Literal

from util.decorators import aoc_output_formatter
from util.input import get_input

from .intcode import InputNotAvailableException, IntcodeComputer

DAY = 11
YEAR = 2019

PART_ONE_DESCRIPTION = "Number tiles painted when robot starts on black"
PART_ONE_ANSWER = 1894

PART_TWO_DESCRIPTION = "Registration painted on the hull by the robot"
PART_TWO_ANSWER = "See output printed above"


Coord = tuple[int, int]

BLACK = " "
WHITE = "█"
type Color = Literal[" ", "█"]

# Input to the program based on the color of the tile
INPUT_MAP: dict[Color, int] = {
    BLACK: 0,
    WHITE: 1,
}

# First output from the program indicates what color to paint
COLOR_OUTPUT_MAP: dict[int, Color] = {
    0: BLACK,
    1: WHITE,
}

# Next output from the program indicates what direction to turn
TURN_OUTPUT_MAP = {
    0: -1,  # left 90 degrees
    1: 1,  # right 90 degrees
}


def copy(program: list[int]) -> list[int]:
    return list(program)


def _paint_hull(hull_colors: dict[Coord, Color], program: list[int]) -> set[Coord]:
    robot_coord = (0, 0)
    robot_facing = 0

    coords_painted: set[Coord] = set()

    complete = False
    computer = IntcodeComputer()

    while not complete:
        try:
            # Continue running the program, with input based on the
            # current hull paint color under the robot.
            computer.execute(
                copy(program),
                program_input=[INPUT_MAP[hull_colors[robot_coord]]],
            )

            # If we reach this point, the robot doesn't want any more
            # input and we're done.
            complete = True
        except InputNotAvailableException:
            # The robot is done evaluating the current position,
            # and should output exactly two values.
            outputs = [
                computer.get_output(),
                computer.get_output(),
            ]
            assert not computer.has_output()  # noqa: S101

            # Paint the current position based on the first output value.
            paint_color = COLOR_OUTPUT_MAP[outputs[0]]
            hull_colors[robot_coord] = paint_color
            coords_painted.add(robot_coord)

            # Turn the robot left or right depending on the second output value,
            # and advance forward one position.
            robot_facing = (robot_facing + TURN_OUTPUT_MAP[outputs[1]]) % 4

            rx, ry = robot_coord
            if robot_facing == 0:
                ry -= 1
            elif robot_facing == 2:
                ry += 1
            elif robot_facing == 1:
                rx += 1
            else:
                rx -= 1

            robot_coord = (rx, ry)

    return coords_painted


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    program = [int(x) for x in raw_input[0].split(",")]
    hull_colors: dict[Coord, Color] = defaultdict(lambda: BLACK)

    coords_painted = _paint_hull(hull_colors, program)
    return len(coords_painted)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    program = [int(x) for x in raw_input[0].split(",")]

    hull_colors: dict[Coord, Color] = defaultdict(lambda: BLACK)
    hull_colors[(0, 0)] = WHITE

    _paint_hull(hull_colors, program)

    min_x = min([x for x, _ in hull_colors]) - 1
    max_x = max([x for x, _ in hull_colors]) + 1
    min_y = min([y for _, y in hull_colors]) - 1
    max_y = max([y for _, y in hull_colors]) + 1

    for y in range(min_y, max_y + 1):
        print(  # noqa: T201
            "".join(
                [hull_colors[(x, y)] for x in range(min_x, max_x + 1)],
            ),
        )

    return "See output printed above"


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
