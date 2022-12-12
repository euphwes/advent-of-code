from util.decorators import aoc_output_formatter
from util.input import get_input_grid_map

from string import ascii_lowercase

DAY  = 12
YEAR = 2022

PART_ONE_DESCRIPTION = 'fewest steps required to reach summit from starting position'
PART_ONE_ANSWER = 447

PART_TWO_DESCRIPTION = 'fewest steps required to reach summit from any lowest position'
PART_TWO_ANSWER = 446

#---------------------------------------------------------------------------------------------------

height_map = {char: i for i, char in enumerate(ascii_lowercase)}
height_map['E'] = height_map['z']
height_map['S'] = height_map['a']


def _neighbors(coord, grid, is_valid_neighbor):
    """ Returns a list of neighbor coordinates which are reachable from the provided coordinate. """

    neighbors = list()

    cx, cy = coord
    for neighbor_coord in [(cx, cy+1), (cx, cy-1), (cx+1, cy), (cx-1, cy)]:
        if neighbor_coord not in grid:
            continue

        # If the candidate neighbor is within the allowed height range then add it to the list
        # of accessible neighbors.
        if is_valid_neighbor(coord, neighbor_coord):
            neighbors.append(neighbor_coord)

    return neighbors


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(grid):

    # Find the coordinate of the start position S
    for start_coord, char in grid.items():
        if char == 'S':
            break

    # Find the coordinate of the end position E
    for end_coord, char in grid.items():
        if char == 'E':
            break

    # A neighbor is valid if it is at most 1 height unit higher than the current coordinate.
    is_valid_neighbor = lambda c, n: height_map[grid[n]] <= height_map[grid[c]] + 1

    # Basic breadth-first search until we reach the target position.
    visited = set()

    queue = list()
    queue.append((start_coord, 0))

    while queue:
        current_coord, steps = queue.pop(0)
        if current_coord == end_coord:
            return steps

        for neighbor in _neighbors(current_coord, grid, is_valid_neighbor):
            if neighbor in visited:
                continue
            else:
                # Add the neighbor we're about to enqueue to the visited set here, instead of above
                # where we actually visit it, because it doesn't change the BFS functionality and
                # it prevents us from having to do another "have we visisted this yet" check above.
                #
                # This is because we can enqueue the same neighbor coordinate multiple times before
                # visiting it if there are multiple paths to reach it in short order.
                visited.add(neighbor)
                queue.append((neighbor, steps+1))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(grid):

    # Find the coordinate of the start position E
    for start_coord, char in grid.items():
        if char == 'E':
            break

    # Because we're searching from the summit to the first accessible lowest elevation area,
    # a neighbor is valid if it is at most 1 height unit lower than the current coordinate.
    # (basically just invert the conditions of the search above).
    is_valid_neighbor = lambda c, n: height_map[grid[n]] >= height_map[grid[c]] - 1

    # Basic breadth-first search until we reach the target position.
    visited = set()

    queue = list()
    queue.append((start_coord, 0))

    while queue:
        current_coord, steps = queue.pop(0)
        if height_map[grid[current_coord]] == 0:
            return steps

        for neighbor in _neighbors(current_coord, grid, is_valid_neighbor):
            if neighbor in visited:
                continue
            else:
                # Add the neighbor we're about to enqueue to the visited set here, instead of above
                # where we actually visit it, because it doesn't change the BFS functionality and
                # it prevents us from having to do another "have we visisted this yet" check above.
                #
                # This is because we can enqueue the same neighbor coordinate multiple times before
                # visiting it if there are multiple paths to reach it in short order.
                visited.add(neighbor)
                queue.append((neighbor, steps+1))

#---------------------------------------------------------------------------------------------------

def run(input_file):

    grid = get_input_grid_map(input_file)

    part_one(grid)
    part_two(grid)
