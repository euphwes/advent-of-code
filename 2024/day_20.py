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
    distance_to_coord = dict()

    # queue state is (cost, coord)
    queue = [(0, start)]
    visited = set()

    while queue:
        cost, coord = queue.pop(0)

        if coord in visited:
            continue
        visited.add(coord)
        distance_to_coord[coord] = cost

        if coord == end:
            best_cost = cost
            break

        for neighbor in _neighbors(coord, maze):
            if neighbor in visited:
                continue
            queue.append((cost + 1, neighbor))

    assert best_cost is not None
    # print(f"Best cost: {best_cost}")

    cheat_starts = set()
    for coord, char in maze.items():
        if char in "E#":
            continue
        cheat_starts.add(coord)

    cheats = []
    for cheat_start in cheat_starts:
        for cheat_end in _get_all_coords_at_manhattan_distance(
            cheat_start,
            maze,
            2,
        ):
            cheats.append((cheat_start, cheat_end, 2))

    time_savings = defaultdict(set)

    for cheat in cheats:
        cheat_start, cheat_end, cheat_delta = cheat

        og_cheat_start_to_finish = distance_to_coord[cheat_end] - distance_to_coord[cheat_start]
        if og_cheat_start_to_finish < 0:
            # we're going backwards on the track, it's not really a cheat
            continue

        if (savings := og_cheat_start_to_finish - cheat_delta) > 0:
            time_savings[savings].add(cheat)

    # iterate over, ordered by increasing savings
    # sorted_savings = [s for s in sorted(time_savings.keys())]
    # for s in sorted_savings:
    #     print(f"There are {len(time_savings[s])} cheats that save {s} picoseconds")

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

    return [coord for coord in candidates if coord in grid and grid[coord] != "#"]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    maze = _parse_maze(raw_input)
    start = next(coord for coord, char in maze.items() if char == "S")
    end = next(coord for coord, char in maze.items() if char == "E")

    best_cost = None
    distance_to_coord = dict()

    # queue state is (cost, coord)
    queue = [(0, start)]
    visited = set()

    while queue:
        cost, coord = queue.pop(0)

        if coord in visited:
            continue
        visited.add(coord)
        distance_to_coord[coord] = cost

        if coord == end:
            best_cost = cost
            break

        for neighbor in _neighbors(coord, maze):
            if neighbor in visited:
                continue
            queue.append((cost + 1, neighbor))

    assert best_cost is not None
    # print(f"Best cost: {best_cost}")

    cheat_starts = set()
    for coord, char in maze.items():
        if char in "E#":
            continue
        cheat_starts.add(coord)

    cheats = []
    for cheat_start in cheat_starts:
        for clen in range(2, 20 + 1):
            for cheat_end in _get_all_coords_at_manhattan_distance(
                cheat_start,
                maze,
                clen,
            ):
                cheats.append((cheat_start, cheat_end, clen))

    time_savings = defaultdict(set)

    for cheat in cheats:
        cheat_start, cheat_end, cheat_delta = cheat

        og_cheat_start_to_finish = distance_to_coord[cheat_end] - distance_to_coord[cheat_start]
        if og_cheat_start_to_finish < 0:
            # we're going backwards on the track, it's not really a cheat
            continue

        if (savings := og_cheat_start_to_finish - cheat_delta) > 0:
            time_savings[savings].add(cheat)

    # iterate over, ordered by increasing savings
    # sorted_savings = [s for s in sorted(time_savings.keys())]
    # for s in sorted_savings:
    #     print(f"There are {len(time_savings[s])} cheats that save {s} picoseconds")

    num_options_gte_100 = sum(
        len(coords) for savings, coords in time_savings.items() if savings >= 100
    )
    return num_options_gte_100


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
