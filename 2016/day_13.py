from functools import lru_cache

from util.decorators import aoc_output_formatter

DAY = 13
YEAR = 2016

PART_ONE_DESCRIPTION = "minimum steps to reach target position"
PART_ONE_ANSWER = 90

PART_TWO_DESCRIPTION = "number of locations that can be reached within 50 steps"
PART_TWO_ANSWER = 135


@lru_cache
def _is_a_wall(coords):
    """Returns if the provided coordinate is occupied by a wall."""

    x, y = coords
    test_value = x * x + 3 * x + 2 * x * y + y + y * y + 1352
    binary_value = bin(test_value)[2:]
    ones_count = sum(1 for digit in binary_value if digit == "1")

    return ones_count % 2 == 1


@lru_cache
def _get_adjacent_open_spaces(coords):
    """Returns a list of coordinates adjacent to the provided coordinates, provided they are
    open space and not walls."""

    x, y = coords

    # All adjacent (non-diagonal) coordinates
    next_spaces = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    # Remove coordinates with negative values
    valid_spaces = [(nx, ny) for nx, ny in next_spaces if nx >= 0 and ny >= 0]

    # Remove coordinates that are occupied by walls
    open_spaces = [space for space in valid_spaces if not _is_a_wall(space)]

    return open_spaces


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one():
    # Breadth-first search of the grid
    visited = set()
    coord_queue = list()

    coord_queue.append(((1, 1), 0))

    while coord_queue:
        current, depth = coord_queue.pop(0)
        visited.add(current)

        # Target location is (31,39). If we're there, return the depth of the BFS search, which
        # is the minimum number of steps required to get there.
        if current == (31, 39):
            return depth

        for next_coord in _get_adjacent_open_spaces(current):
            if next_coord in visited:
                continue
            coord_queue.append((next_coord, depth + 1))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two():
    # Breadth-first search of the grid
    visited = set()
    coord_queue = list()

    coord_queue.append(((1, 1), 0))

    while coord_queue:
        current, depth = coord_queue.pop(0)

        # We only want to search to a depth of 50.
        if depth == 51:
            break

        # Store every cell visited so we can count them.
        visited.add(current)

        for next_coord in _get_adjacent_open_spaces(current):
            if next_coord in visited:
                continue
            coord_queue.append((next_coord, depth + 1))

    return len(visited)


# ----------------------------------------------------------------------------------------------


def run(_):
    part_one()
    part_two()
