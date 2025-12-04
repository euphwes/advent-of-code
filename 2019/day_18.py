from string import ascii_lowercase, ascii_uppercase

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 18
YEAR = 2019

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

Coord = tuple[int, int]

START = "@"

# Walls, and locked doors, are not traversible
DOORS = ascii_uppercase
WALLS = DOORS + "#"

# You can walk on/through open space, and the spaces where keys are.
KEYS = ascii_lowercase
SPACE = "."
SPACES = KEYS + SPACE + START


def _parse_grid(raw_input: list[str]) -> dict[Coord, str]:
    grid = {}

    for y, line in enumerate(raw_input):
        for x, char in enumerate(line):
            grid[(x, y)] = char

    return grid


def _find_new_keys_accessible_with_keys(
    owned_keys: set[str],
    key_coordinates: dict[str, Coord],
    door_coordinates: dict[str, Coord],
    grid: dict[Coord, str],
) -> set[str]:
    # "Unlock" doors with the current keys by turning those doors into open spaces.
    # Also replace the "key spaces" for keys we already have, with open spaces.
    # This will simplify the "accessible new key" logic later.
    unlocked_grid = dict(grid)
    for key in owned_keys:
        unlocked_grid[key_coordinates[key]] = SPACE
        unlocked_grid[door_coordinates[key.upper()]] = SPACE

    # BFS walk the whole grid, and note which keys are accessible now that doors
    # have been unlocked.
    found_keys = set()

    # Start is at (40,40)
    # TODO: accept this as param to function
    queue: list[Coord] = [(40, 40)]
    visited: set[Coord] = set()

    while queue:
        x, y = queue.pop(0)

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if unlocked_grid[(x, y)] in KEYS:
            found_keys.add(unlocked_grid[(x, y)])

        for neighbor in [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]:
            if unlocked_grid[neighbor] in WALLS:
                continue
            queue.append(neighbor)

    return found_keys


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)
    keys_owned = set()

    key_coordinates: dict[str, Coord] = {}
    door_coordinates: dict[str, Coord] = {}

    for k, v in grid.items():
        if v in KEYS:
            key_coordinates[v] = k
        elif v in DOORS:
            door_coordinates[v] = k

    print(
        _find_new_keys_accessible_with_keys(
            owned_keys=keys_owned,
            key_coordinates=key_coordinates,
            door_coordinates=door_coordinates,
            grid=grid,
        ),
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    pass


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
