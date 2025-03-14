from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 3
YEAR = 2015

PART_ONE_DESCRIPTION = "houses with presents"
PART_ONE_ANSWER = 2592

PART_TWO_DESCRIPTION = "houses with presents"
PART_TWO_ANSWER = 2360


# Dict to correlate a direction arrow to a change in (x, y) coordinates
_direction_mods = {
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
    "<": (-1, 0),
}


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    directions = raw_input[0]

    houses = set()
    houses.add((0, 0))

    x, y = 0, 0
    for direction in directions:
        dx, dy = _direction_mods[direction]
        x, y = x + dx, y + dy

        houses.add((x, y))

    return len(houses)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    directions = raw_input[0]

    houses = set()
    houses.add((0, 0))

    # Santa's coordinates
    x, y = 0, 0

    # Robo-Santa's coordinates
    rx, ry = 0, 0

    for i, direction in enumerate(directions):
        dx, dy = _direction_mods[direction]

        # Santa and Robo-Santa take turns moving
        if i % 2 == 0:
            x, y = x + dx, y + dy
            houses.add((x, y))
        else:
            rx, ry = rx + dx, ry + dy
            houses.add((rx, ry))

    return len(houses)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
