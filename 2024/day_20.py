from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 20
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


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


def _is_cheatable_wall(coord, grid):
    """Returns true if the provided coord is a wall which is framed by open
    space on either left and right, or above and below.
    """

    x, y = coord
    if grid[(x, y)] != "#":
        return False

    if grid.get((x - 1, y), "#") != "#" and grid.get((x + 1, y), "#") != "#":
        return True
    if grid.get((x, y - 1), "#") != "#" and grid.get((x, y + 1), "#") != "#":
        return True

    return False


def _parse_maze(raw_input: list[str]) -> dict[tuple[int, int], str]:
    maze = {}
    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            maze[(x, y)] = char
    return maze


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    maze = _parse_maze(raw_input)
    start = next(coord for coord, char in maze.items() if char == "S")
    end = next(coord for coord, char in maze.items() if char == "E")

    best_cost = None

    # queue state is (cost, coord)
    queue = [(0, start)]
    visited = set()

    while queue:
        cost, coord = queue.pop(0)

        if coord in visited:
            continue
        visited.add(coord)

        if coord == end:
            best_cost = cost
            break

        for neighbor in _neighbors(coord, maze):
            if neighbor in visited:
                continue
            queue.append((cost + 1, neighbor))

    assert best_cost is not None

    cheatable_wall_coords = [coord for coord in maze if _is_cheatable_wall(coord, maze)]
    time_savings = defaultdict(set)

    for cheat in cheatable_wall_coords:
        cheat_best_cost = None

        maze_copy = maze.copy()
        maze_copy[cheat] = "."

        queue = [(0, start)]
        visited = set()

        while queue:
            cost, coord = queue.pop(0)

            if coord in visited:
                continue
            visited.add(coord)

            if coord == end:
                cheat_best_cost = cost
                break

            for neighbor in _neighbors(coord, maze_copy):
                if neighbor in visited:
                    continue
                queue.append((cost + 1, neighbor))

        assert cheat_best_cost is not None
        time_savings[best_cost - cheat_best_cost].add(cheat)

    num_options_gte_100 = sum(
        len(coords) for savings, coords in time_savings.items() if savings >= 100
    )
    return num_options_gte_100


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    pass


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
