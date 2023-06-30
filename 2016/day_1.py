from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

DAY = 1
YEAR = 2016

PART_ONE_DESCRIPTION = "distance to Easter Bunny HQ"
PART_ONE_ANSWER = 246

PART_TWO_DESCRIPTION = "distance to Easter Bunny HQ real location"
PART_TWO_ANSWER = 124


def _follow_path(instructions):
    """Iterate over the instructions, yielding a coordinate pair for each city block visited."""

    # Directions: 0, 1, 2, 3 = N, E, S, W
    x, y = 0, 0
    direction = 0

    yield (x, y)

    for step in instructions:
        turn = step[0]
        direction = (direction + (1 if turn == "R" else -1)) % 4

        distance = int(step[1:])
        for _ in range(distance):
            if direction == 0:
                y += 1
            elif direction == 1:
                x += 1
            elif direction == 2:
                y -= 1
            else:
                x -= 1

            yield (x, y)


def _manahattan_distance(coords):
    x, y = coords
    return abs(x) + abs(y)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(instructions):
    coords = (0, 0)
    for coords in _follow_path(instructions):
        pass
    return _manahattan_distance(coords)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(instructions):
    locations = set()
    for coords in _follow_path(instructions):
        if coords in locations:
            return _manahattan_distance(coords)
        locations.add(coords)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    instructions = get_tokenized_input(input_file, ", ")[0]

    part_one(instructions)
    part_two(instructions)
