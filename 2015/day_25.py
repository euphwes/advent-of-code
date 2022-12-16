from util.decorators import aoc_output_formatter
from util.iter import int_stream

DAY = 25
YEAR = 2015

PART_ONE_DESCRIPTION = "code at target coordinates"
PART_ONE_ANSWER = 2650453


def _diagonal_coords_stream():
    """Yields the coordinates of a cartesian grid, where the coordinates of the integers 1, 2,
    3, 4, etc... (in that order) are returned as shown in this grid below:

       |  1   2   3   4   5   6
    ---+---+---+---+---+---+---+
     1 |  1   3   6  10  15  21
     2 |  2   5   9  14  20
     3 |  4   8  13  19
     4 |  7  12  18
     5 | 11  17
     6 | 16

    So coordinates are yielded in this order:
    (1, 1),   # digit 1
    (1, 2),   # digit 2
    (2, 1),   # digit 3
    (3, 1),   # digit 4
    (2, 2),   # digit 5
    (3, 1)    # digit 6

    and so on."""

    for target_sum in int_stream(2):
        for y in int_stream(1, target_sum - 1):
            yield (target_sum - y, y)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(target_x, target_y):

    # At (1, 1) the code starts at this value
    code = 20151125

    # Each time we move to a new coordinate in the stream, update the code following the rules
    # provided in the problem input, until we reach the target coordinate, then return the code.
    for x, y in _diagonal_coords_stream():
        if (x, y) == (target_x, target_y):
            return code
        code = (code * 252533) % 33554393


# ----------------------------------------------------------------------------------------------


def run(input_file):

    # from the puzzle input
    part_one(2978, 3083)
