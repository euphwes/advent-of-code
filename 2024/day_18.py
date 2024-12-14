from heapq import heappop, heappush

from util.algs import manhattan_distance
from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 18
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

X_SIZE = 71
Y_SIZE = 71


def _neighbors(coord, grid):
    neighbors = list()

    cx, cy = coord
    for neighbor_coord in [(cx, cy + 1), (cx, cy - 1), (cx + 1, cy), (cx - 1, cy)]:
        if neighbor_coord not in grid:
            continue
        if grid[neighbor_coord] == "#":
            continue
        neighbors.append(neighbor_coord)

    return neighbors


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = {(x, y): "." for x in range(X_SIZE) for y in range(Y_SIZE)}

    for line in raw_input[:1024]:
        x, y = (int(n) for n in line.split(","))
        grid[(x, y)] = "#"

    start = (0, 0)
    end = (X_SIZE - 1, Y_SIZE - 1)

    # state is (steps_so_far, manhattan_distance_to_end, curr_position)

    queue = []
    heappush(queue, (0, manhattan_distance(start, end), start))

    visited = set()

    while queue:
        steps, _, curr_pos = heappop(queue)
        if curr_pos in visited:
            continue

        visited.add(curr_pos)

        if curr_pos == end:
            return steps

        for neighbor in _neighbors(curr_pos, grid):
            if neighbor in visited:
                continue
            heappush(queue, (steps + 1, manhattan_distance(neighbor, end), neighbor))

    raise ValueError("No path found")


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    og_grid = {(x, y): "." for x in range(X_SIZE) for y in range(Y_SIZE)}

    for limit in int_stream(1000):
        grid = og_grid.copy()

        for line in raw_input[:limit]:
            x, y = (int(n) for n in line.split(","))
            grid[(x, y)] = "#"

        start = (0, 0)
        end = (X_SIZE - 1, Y_SIZE - 1)

        # state is (steps_so_far, manhattan_distance_to_end, curr_position)

        queue = []
        heappush(queue, (0, manhattan_distance(start, end), start))

        visited = set()

        did_find = False
        while queue:
            steps, _, curr_pos = heappop(queue)
            if curr_pos in visited:
                continue

            visited.add(curr_pos)

            if curr_pos == end:
                did_find = True
                break

            for neighbor in _neighbors(curr_pos, grid):
                if neighbor in visited:
                    continue
                heappush(queue, (steps + 1, manhattan_distance(neighbor, end), neighbor))

        if not did_find:
            return raw_input[:limit][-1]

    raise ValueError("No answer found")


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
