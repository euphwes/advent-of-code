from heapq import heappop, heappush

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

    if curr_direction == "E" and grid.get((cx + 1, cy), "#") != "#":
        neighbors.append(((cx + 1, cy), "E"))
    if curr_direction == "W" and grid.get((cx - 1, cy), "#") != "#":
        neighbors.append(((cx - 1, cy), "W"))
    if curr_direction == "N" and grid.get((cx, cy - 1), "#") != "#":
        neighbors.append(((cx, cy - 1), "N"))
    if curr_direction == "S" and grid.get((cx, cy + 1), "#") != "#":
        neighbors.append(((cx, cy + 1), "S"))

    if curr_direction in "EW":
        neighbors.append(((cx, cy), "N"))
        neighbors.append(((cx, cy), "S"))
    if curr_direction in "NS":
        neighbors.append(((cx, cy), "W"))
        neighbors.append(((cx, cy), "E"))

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
    heappush(queue, (0, start, "E"))

    while queue:
        cost, curr, curr_dir = heappop(queue)
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
                raise ValueError(f"Invalid state: {curr=}, {curr_dir=}, {ncoord=}, {ndir=}")


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

    # state is (cost up to this point, coord, curr_direction, path_to_this_point)
    # path_to_this_point is list of (cost, coord, direction)

    visited = set()
    queue = []
    heappush(queue, (0, start, "E", [(0, start, "E")]))

    solutions = []

    while queue:
        cost, curr, curr_dir, path = heappop(queue)
        visited.add((curr, curr_dir))
        if curr == end:
            solutions.append((cost, path))
            continue

        for ncoord, ndir in _neighbors(curr, grid, curr_dir):
            if (ncoord, ndir) in visited:
                continue

            # if ncoord in set(x[1] for x in path):
            #     continue

            # new_path = path.copy() + [(cost, ncoord, ndir)]

            if ncoord == curr and ndir != curr_dir:
                heappush(
                    queue,
                    (cost + 1000, ncoord, ndir, path.copy() + [(cost + 1000, ncoord, ndir)]),
                )
            elif ncoord != curr and ndir == curr_dir:
                heappush(
                    queue,
                    ((cost + 1, ncoord, ndir, path.copy() + [(cost + 1, ncoord, ndir)])),
                )
            else:
                raise ValueError(f"Invalid state: {curr=}, {curr_dir=}, {ncoord=}, {ndir=}")

    best_cost = min(solutions, key=lambda x: x[0])[0]

    distinct_cells = set()

    for cost, path in solutions:
        if cost == best_cost:
            for _, coord, _ in path:
                distinct_cells.add(coord)

    return len(distinct_cells)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
