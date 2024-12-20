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


# -=============================================


def _get_all_coords_at_manhattan_distance(coord, grid, distance):
    candidates = set()

    sensor_x, sensor_y = coord

    # Start immediately right of the sensor, `distance` units away.
    y = sensor_y
    x = sensor_x + distance

    # Move diagonally up and left until we are directly above the sensor (still `distance` units
    # away), yielding every coordinate along the way.
    while x > sensor_x:
        candidates.add((x, y))
        x -= 1
        y -= 1

    candidates.add((x, y))

    # Move diagonally down and left until we are directly to the left of the sensor (still
    # `distance` units away), yielding every coordinate along the way.
    while y < sensor_y:
        candidates.add((x, y))
        x -= 1
        y += 1

    candidates.add((x, y))

    # Move diagonally down and right until we are directly below the sensor (still `distance`
    # units away), yielding every coordinate along the way.
    while x < sensor_x:
        candidates.add((x, y))
        x += 1
        y += 1

    candidates.add((x, y))

    # Move diagonally up and right until we are directly to the right the sensor (still
    # `distance` units away), yielding every coordinate along the way.
    while y > sensor_y:
        candidates.add((x, y))
        x += 1
        y -= 1

    candidates.add((x, y))

    return [coord for coord in candidates if coord in grid]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
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

    cheat_starts = set()
    for coord, char in maze.items():
        if char == "#":
            cheat_starts.add(coord)

    CHEAT_LEN = 20
    cheats = []
    for cheat_start in cheat_starts:
        for cheat_end in _get_all_coords_at_manhattan_distance(
            cheat_start,
            maze,
            CHEAT_LEN - 1,
        ):
            cheats.append((cheat_start, cheat_end))

    time_savings = defaultdict(set)

    for cheat in cheats:
        cheat_start, cheat_end = cheat
        cheat_best_cost = None

        maze_copy = maze.copy()

        for x in range(cheat_start[0], cheat_end[0] + 1):
            for y in range(cheat_start[1], cheat_end[1] + 1):
                maze_copy[(x, y)] = "."

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

    for savings, coords in time_savings.items():
        print(f"Savings: {savings}, num cheats: {len(coords)}")

    num_options_gte_100 = sum(
        len(coords) for savings, coords in time_savings.items() if savings >= 100
    )
    return num_options_gte_100


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
