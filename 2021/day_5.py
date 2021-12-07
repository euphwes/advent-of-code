from collections import defaultdict, namedtuple

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import bidirectional_range

#---------------------------------------------------------------------------------------------------

Point = namedtuple('Point', ['x', 'y'])


def _is_non_diagonal(line):
    """ Returns true if the provided line is not diagonal. """
    p1, p2 = line
    return p1.x == p2.x or p1.y == p2.y


def  _enumerate_diagonal(p1, p2):
    """ A generator which enumerates all of the points in a diagonal line. """

    x_on_diag = bidirectional_range(p1.x, p2.x, inclusive=True)
    y_on_diag = bidirectional_range(p1.y, p2.y, inclusive=True)

    for x, y in zip(x_on_diag, y_on_diag):
        yield x, y


def _enumerate_points(p1, p2):
    """ A generator which enumerates all of the points in a line. """

    # Defer to the diagonal line generator for that case...
    if not _is_non_diagonal((p1, p2)):
        yield from _enumerate_diagonal(p1, p2)

    # ...otherwsise just enumerate all the points on the straight line.
    else:
        for x in bidirectional_range(p1.x, p2.x, inclusive=True):
            for y in bidirectional_range(p1.y, p2.y, inclusive=True):
                yield (x, y)


def _evaluate_number_points_visited_multiple_times(line_points):
    """ I think the verbose function is pretty clear. """

    # Iterate all points in all lines, counting the number of times each points is crossed by a line
    visit_count = defaultdict(int)
    for p1, p2 in line_points:
        for point in _enumerate_points(p1, p2):
            visit_count[point] += 1

    # Return the number of points which have been visited 2 or more times by lines
    return sum(1 for _, visit_count in visit_count.items() if visit_count >= 2)


@aoc_output_formatter(2021, 5, 1, 'number of overlapped points without diagonals')
def part_one(line_points):
    # Filter to have only non-diagonal lines
    no_diagonals = [line for line in line_points if _is_non_diagonal(line)]
    return _evaluate_number_points_visited_multiple_times(no_diagonals)


@aoc_output_formatter(2021, 5, 2, 'number of overlapped points for all lines')
def part_two(line_points):
    return _evaluate_number_points_visited_multiple_times(line_points)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    raw = get_input(input_file)
    line_points = list()

    for line in raw:
        a, b = line.split(' -> ')

        ax, ay = a.split(',')
        point_a = Point(x=int(ax), y=int(ay))

        bx, by = b.split(',')
        point_b = Point(x=int(bx), y=int(by))

        line_points.append((point_a, point_b))

    part_one(line_points)
    part_two(line_points)
