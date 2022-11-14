from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

#---------------------------------------------------------------------------------------------------

def _hex_distance(c1, c2):
    """ Returns the distance between two coordinates in a hexagonal grid, with the coordinates
    expressed in cube coordinate format. """

    q1, q2 = c1[0], c2[0]
    r1, r2 = c1[1], c2[1]
    s1, s2 = c1[2], c2[2]

    delta_q, delta_r, delta_s = abs(q1-q2), abs(r1-r2), abs(s1-s2)

    return int((delta_q + delta_r + delta_s) / 2)


def _hex_navigate(starting_coord, direction):
    """ Navigate an endless hexagonal grid by moving a particular direction (N, S, NE, SE, NW, SE)
    from a starting coordinate, and return the resulting coordinate.

    Thanks https://www.redblobgames.com/grids/hexagons/ for the explanations!

    The problem specifies a "flat-topped" hexagonal grid. Let's choose to use the cube coordinate
    format (q, r, s).

    The q axis runs from S to N, with r decreasing and s increasing as you move N.
    The r axis runs from SE to NW, with q decreasing and s increasing as you move NW.
    The s axis runs from SW to NE, with r decreasing and q increasing as you move NE.

    Interesting constraint: sum of (q,r,s) always == 0. """

    q, r, s = starting_coord

    direction_action = {
        'n': lambda: (q, r-1, s+1),
        's': lambda: (q, r+1, s-1),
        'nw': lambda: (q-1, r, s+1),
        'se': lambda: (q+1, r, s-1),
        'ne': lambda: (q+1, r-1, s),
        'sw': lambda: (q-1, r+1, s),
    }

    return direction_action[direction]()


@aoc_output_formatter(2017, 11, 1, 'distance from start')
def part_one(directions):
    coord = (0, 0, 0)
    for direction in directions:
        coord = _hex_navigate(coord, direction)
    return _hex_distance((0, 0, 0), coord)


@aoc_output_formatter(2017, 11, 2, 'furthest distance from start')
def part_two(directions):
    stepwise_distances = list()
    coord = (0, 0, 0)
    for direction in directions:
        coord = _hex_navigate(coord, direction)
        stepwise_distances.append(_hex_distance((0, 0, 0), coord))
    return max(stepwise_distances)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    directions = get_tokenized_input(input_file, ',')[0]

    part_one(directions)
    part_two(directions)
