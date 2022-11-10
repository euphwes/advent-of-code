from util.algs import manhattan_distance
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable

#---------------------------------------------------------------------------------------------------

def _spiral():
    """ Produces a spiral of increasing integers, starting with a value of 1 at (0, 0), following
    this pattern:

    17  16  15  14  13
    18   5   4   3  12
    19   6   1   2  11
    20   7   8   9  10
    21  22  23---> ...

    This generator yields tuples of (value, coordinate_of_value).
    Ex: the first 10 iterations are...

    (1,  ( 0,  0))
    (2,  ( 1,  0))
    (3,  ( 1, -1))
    (4,  ( 0, -1))
    (5,  (-1, -1))
    (6,  (-1,  0))
    (7,  (-1,  1))
    (8,  ( 0,  1))
    (9,  ( 1,  1))
    (10, ( 2,  1))
    """

    # The spiral expands in this order; right, up, left, down, right again, etc
    # Start off moving right.
    directions = 'ruld'
    directions_ix = 0

    # While moving r, u, l, d, r, u, l, d, etc, we start moving right 1 step, then up 1 step,
    # then left 2 steps, then down 2 steps, then right 3 steps, etc. Every *other* direction change,
    # we increase the number of steps in that direction by 1. Start off moving 1 step at a time
    # in each direction.
    direction_steps = 1
    do_increase_distance = True

    # Start the spiral with a value of 1 at (0, 0)
    counter = 1
    x_coord, y_coord = 0, 0

    while True:
        for _ in range(direction_steps):
            yield counter, (x_coord, y_coord)

            counter += 1

            direction = directions[directions_ix % 4]
            if direction == 'r':
                x_coord += 1
            elif direction == 'u':
                y_coord -= 1
            elif direction == 'l':
                x_coord -= 1
            else:
                y_coord += 1

        directions_ix += 1

        do_increase_distance = not do_increase_distance
        if do_increase_distance:
            direction_steps += 1


def _get_sum_of_neighbors(target_coord, spiral_coord_value_map):
    """ Returns the sum of all cells neighboring the provided coordinate so far in the spiral. """

    neighbor_sum = 0

    tx, ty = target_coord
    for nx, ny in nested_iterable((tx-1, tx, tx+1), (ty-1, ty, ty+1)):
        if (nx, ny) == (tx, ty) or (nx, ny) not in spiral_coord_value_map:
            continue
        neighbor_sum += spiral_coord_value_map[(nx, ny)]

    return neighbor_sum


@aoc_output_formatter(2017, 3, 1, 'manhattan distance from access port to cell containing input value')
def part_one(input_value):
    for spiral_value, coord in _spiral():
        if spiral_value == input_value:
            return manhattan_distance((0, 0), coord)


@aoc_output_formatter(2017, 3, 2, 'first value in summing spiral larger than input value')
def part_two(value):
    # Hold a map of coordinates to the summed values in the spiral
    spiral_coord_value_map = dict()

    for _, coord in _spiral():

        # Disregard the value provided by the generator, and instead set the value as the sum of
        # all populated neighbors so far.
        neighbor_sum = _get_sum_of_neighbors(coord, spiral_coord_value_map)

        # Special case, the very first cell will have a sum of 0, so instead set it to 1.
        if neighbor_sum == 0:
            neighbor_sum = 1

        # Set the value for this cell into the map for this coordinate
        spiral_coord_value_map[coord] = neighbor_sum

        if neighbor_sum > value:
            return neighbor_sum

#---------------------------------------------------------------------------------------------------

def run(input_file):

    value = int(get_input(input_file)[0])

    part_one(value)
    part_two(value)
