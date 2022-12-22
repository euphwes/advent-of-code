from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

DAY = 9
YEAR = 2022

PART_ONE_DESCRIPTION = "positions a 2-knotted rope's tail occupies"
PART_ONE_ANSWER = 6081

PART_TWO_DESCRIPTION = "positions a 10-knotted rope's tail occupies"
PART_TWO_ANSWER = 2487


# Map of direction to (delta_x, delta_y) for coords moving that direction
DIRECTION_DELTA_MAP = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def _are_neighbors(coord1, coord2):
    """Returns if two coordinates are neighbors (directly or diagonally adjacent, or the same
    coordinate)."""

    x, y = coord1
    return any(
        coord2 == (x + dx, y + dy) for dx, dy in nested_iterable([-1, 0, 1], [-1, 0, 1])
    )


def _follow(leading, trailing):
    """Adjusts the coordinates for a trailing knot to ensure it follows the leading knot, and
    returns the new coordinates for the trailing knot. If the two knots are not immediate
    neighbors, the trailing knot moves one space (linearly or diagonally) to become a neighbor
    of the leading knot."""

    # If the two are neighbors, the trailing knot doesn't need to move.
    if _are_neighbors(trailing, leading):
        return trailing

    # Otherwise move the trailing knot to become adjacent to the leading one
    lx, ly = leading
    tx, ty = trailing

    if tx != lx:
        tx += -1 if tx > lx else 1

    if ty != ly:
        ty += -1 if ty > ly else 1

    return (tx, ty)


def _get_tail_positions_of_n_knotted_rope(n, movement_instructions):
    """Simulates the movement of an n-knot rope following the provided movement instructions,
    and returns a set of all unique positions the tail (final knot) occupies at any point."""

    tail_positions = set()

    knot_positions = [(0, 0) for n in range(n)]
    tail_positions.add(knot_positions[-1])

    for line in movement_instructions:
        direction, amount = line.split()

        dx, dy = DIRECTION_DELTA_MAP[direction]
        amount = int(amount)

        for _ in range(amount):
            head_x, head_y = knot_positions[0]
            knot_positions[0] = (head_x + dx, head_y + dy)

            for leading_ix in range(0, n - 1):
                trailing_ix = leading_ix + 1

                leading = knot_positions[leading_ix]
                trailing = knot_positions[trailing_ix]

                knot_positions[trailing_ix] = _follow(leading, trailing)

            tail_positions.add(knot_positions[-1])

    return tail_positions


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(movement_instructions):
    return len(_get_tail_positions_of_n_knotted_rope(2, movement_instructions))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(movement_instructions):
    return len(_get_tail_positions_of_n_knotted_rope(10, movement_instructions))


# ----------------------------------------------------------------------------------------------


def run(input_file):

    movement_instructions = get_input(input_file)

    part_one(movement_instructions)
    part_two(movement_instructions)
