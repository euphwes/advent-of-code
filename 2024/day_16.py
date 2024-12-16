from heapq import heappush, heappop
from itertools import pairwise
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 16
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _neighbors(coord, grid, curr_direction):
    neighbors = list()

    cx, cy = coord

    if curr_direction == 'E' and grid.get((cx + 1, cy), '#') != "#":
        neighbors.append(((cx + 1, cy), 'E'))
    if curr_direction == 'W' and grid.get((cx - 1, cy), '#') != "#":
        neighbors.append(((cx - 1, cy), 'W'))
    if curr_direction == 'N' and grid.get((cx, cy - 1), '#') != "#":
        neighbors.append(((cx, cy - 1), 'N'))
    if curr_direction == 'S' and grid.get((cx, cy + 1), '#') != "#":
        neighbors.append(((cx, cy + 1), 'S'))

    if curr_direction in 'EW':
        neighbors.append(((cx, cy), 'N'))
        neighbors.append(((cx, cy), 'S'))
    if curr_direction in 'NS':
        neighbors.append(((cx, cy), 'W'))
        neighbors.append(((cx, cy), 'E'))

    return neighbors



@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = dict()
    start = None
    end = None
    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)

    assert start is not None
    assert end is not None

    # --------

    # state is (cost up to this point, coord, curr_direction)

    visited = set()
    queue = []
    heappush(queue, (0, start, 'E'))

    while queue:
        cost, curr, curr_dir  = heappop(queue)
        visited.add((curr, curr_dir))
        if curr == end:
            return cost

        for ncoord, ndir in _neighbors(curr, grid, curr_dir):
            if (ncoord, ndir) in visited:
                continue
            if ncoord == curr and ndir != curr_dir:
                heappush(queue, (cost + 1000, ncoord, ndir))
            elif ncoord != curr and ndir == curr_dir:
                heappush(queue, ((cost + 1, ncoord, ndir)))
            else:
                raise ValueError(f'Invalid state: {curr=}, {curr_dir=}, {ncoord=}, {ndir=}')



@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    grid = dict()
    start = None
    end = None
    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            grid[(x, y)] = char
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)

    assert start is not None
    assert end is not None

    # --------

    # state is (cost up to this point, coord, curr_direction)

    visited = set()
    queue = []
    heappush(queue, (0, start, 'E'))

    best_cost = None

    while queue:
        cost, curr, curr_dir  = heappop(queue)
        visited.add((curr, curr_dir))
        if curr == end:
            best_cost = cost
            break

        for ncoord, ndir in _neighbors(curr, grid, curr_dir):
            if (ncoord, ndir) in visited:
                continue
            if ncoord == curr and ndir != curr_dir:
                heappush(queue, (cost + 1000, ncoord, ndir))
            elif ncoord != curr and ndir == curr_dir:
                heappush(queue, ((cost + 1, ncoord, ndir)))
            else:
                raise ValueError(f'Invalid state: {curr=}, {curr_dir=}, {ncoord=}, {ndir=}')

    assert best_cost is not None
    print(f'Best cost: {best_cost}')

    # ---------------

    del visited

    # dfs to find all paths leading to the end
    def _walk(coord, curr_direction, visited):
        if (coord, curr_direction) in visited:
            return []

        visited.add((coord, curr_direction))

        if coord == end:
            return [[(coord, curr_direction)]]

        possible_paths = list()

        for ncoord, ndir in _neighbors(coord, grid, curr_direction):
            for path in _walk(ncoord, ndir, visited):
                possible_paths.append([(coord, curr_direction)] + path)

        return possible_paths


    all_paths = _walk(start, 'E', set())
    print(f'Found {len(all_paths)} paths')

    def _get_score(path):
        score = 0
        for c1, c2 in pairwise(path):
            if c1[0] == c2[0]:
                score += 1
            else:
                score += 1000
        print(f'Path: {path} has score {score}')
        return score

    cells_on_best_paths = set()

    for path in all_paths:
        if _get_score(path) == best_cost:
            print(f'HIT found another path with score {best_cost}')
            for cell in path:
                cells_on_best_paths.add(cell)

    return len(cells_on_best_paths)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
