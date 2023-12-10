from util.decorators import aoc_output_formatter
from util.input import get_input

from typing import List, Tuple


DAY = 10
YEAR = 2023

PART_ONE_DESCRIPTION = "distance of the furthest snake body part from the start"
PART_ONE_ANSWER = 6778

PART_TWO_DESCRIPTION = "number of tiles enclosed by the snake loop"
PART_TWO_ANSWER = 433


def _find_start(snake_map):
    """Return the (x, y) coordinate of the "start" of the snake loop, marked by "S"."""

    for y, line in enumerate(snake_map):
        for x, char in enumerate(line):
            if char == "S":
                return (x, y)
    raise ValueError()


def _connects_north(x, y, snake_map):
    """Returns whether the provided (x, y) connects to the tile to the north of it."""

    try:
        return snake_map[y][x] in "|LJ"
    except KeyError:
        return False


def _connects_south(x, y, snake_map):
    """Returns whether the provided (x, y) connects to the tile to the south of it."""

    try:
        return snake_map[y][x] in "|7F"
    except KeyError:
        return False


def _connects_west(x, y, snake_map):
    """Returns whether the provided (x, y) connects to the tile to the west of it."""

    try:
        return snake_map[y][x] in "-J7S"
    except KeyError:
        return False


def _connects_east(x, y, snake_map):
    """Returns whether the provided (x, y) connects to the tile to the east of it."""

    try:
        return snake_map[y][x] in "-FLS"
    except KeyError:
        return False


def _neighbors(x, y, snake_map):
    """From a given (x, y) coord on the snake's body loop, return a list of all the (x, y)
    coordinates which connect to this one."""

    neighbors = list()

    # For each cardinal direction, check if the body segment at this position connects that
    # direction. If it does, add the (x, y) coord in that direction to the list of neighbors.
    if _connects_north(x, y, snake_map):
        neighbors.append((x, y - 1))

    if _connects_south(x, y, snake_map):
        neighbors.append((x, y + 1))

    if _connects_east(x, y, snake_map):
        neighbors.append((x + 1, y))

    if _connects_west(x, y, snake_map):
        neighbors.append((x - 1, y))

    return neighbors


def _get_snake_body_segment_distances(snake_map):
    """Finds the start point of the snake's body, and then builds and returns a map of all the
    coords on that snake's body, and the distance from the start that body segment is.
    """

    (sx, sy) = _find_start(snake_map)

    visited = set()
    distance_map = dict()

    distance_map[(sx, sy)] = 0
    queue: List[Tuple[int, Tuple[int, int]]] = [(0, (sx, sy))]

    while queue:
        steps, coord = queue.pop(0)
        cx, cy = coord
        visited.add((cx, cy))
        distance_map[coord] = steps

        for neighbor in _neighbors(cx, cy, snake_map):
            if neighbor not in visited:
                queue.append((steps + 1, neighbor))

    return distance_map


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(snake_map):
    body_segment_distances = _get_snake_body_segment_distances(snake_map).values()
    return max(body_segment_distances)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(snake_map):
    distance_map = _get_snake_body_segment_distances(snake_map)
    coords_on_loop = set(distance_map.keys())

    num_cells_enclosed = 0

    # We're going to scan each line of the whole input, left to right.
    # We start on the outside of the snake's enclosed area, but whenever we cross a vertical
    # pipe, we know we're inside, and when we cross another pipe, we know we're back outside.
    # Sometimes we end up ON a horizontal stretch of pipe, so we keep track of the joints
    # starting and ending that stretch. If the horizontal stretch ends with elbows pointing
    # opposite directions, topologically it's basically the same thing as a vertical pipe, and
    # so then we toggle whether we're inside or outside the snake's body.
    ALWAYS_FLIP = set("|")
    HORIZONTAL_PIPES = set("-S")  # only for my input, not all
    FLIP_PAIRS = set([frozenset("L7"), frozenset("FJ")])

    for y, line in enumerate(snake_map):
        is_inside = False
        horiz_line_stack = list()

        for x, char in enumerate(line):
            if (x, y) in coords_on_loop:
                if char in ALWAYS_FLIP:
                    is_inside = not is_inside
                elif char in HORIZONTAL_PIPES:
                    continue
                else:
                    if not horiz_line_stack:
                        horiz_line_stack.append(char)
                    else:
                        other_char = horiz_line_stack.pop()
                        pair = frozenset(f"{char}{other_char}")
                        if pair in FLIP_PAIRS:
                            is_inside = not is_inside
            else:
                # If we know we're currently enclosed in the snake's body, and the current tile
                # doesn't belong to the snake itself, then this tile is enclosed by the snake.
                if is_inside:
                    num_cells_enclosed += 1

    return num_cells_enclosed


# ----------------------------------------------------------------------------------------------


def run(input_file):
    snake_map = get_input(input_file)
    part_one(snake_map)
    part_two(snake_map)
