from dataclasses import dataclass
from heapq import heappop, heappush
from string import ascii_lowercase, ascii_uppercase
from typing import Self

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 18
YEAR = 2019

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None

Coord = tuple[int, int]


@dataclass
class KeySearchState:
    x: int
    y: int
    steps: int

    @property
    def coord(self) -> Coord:
        return self.x, self.y

    def __lt__(self, other: Self) -> bool:
        return self.steps < other.steps


@dataclass
class KeyOrderSearchState:
    steps: int
    keys_owned: list[str]

    def __lt__(self, other: Self) -> bool:
        return self.steps < other.steps

    @property
    def key_set(self) -> frozenset[str]:
        return frozenset(self.keys_owned)


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


def _distance_to_keys_accessible(
    start: Coord,
    keys_owned: list[str],
    grid: dict[Coord, str],
    # TODO: try removing these two params and recalculating each time,
    # see if it affects performance
    key_coordinates: dict[str, Coord],
    door_coordinates: dict[str, Coord],
) -> dict[str, int]:
    """Return a dict of accessible keys and their distances from the current position.

    Based on the keys we currently have, some doors are unlocked/passable. From our current
    position, return a dict of accessible keys that we don't currently have, and their distance
    from our current position.
    """

    # "Unlock" doors with the current keys by turning those doors into open spaces.
    # Also replace the "key spaces" for keys we already have, with open spaces,
    # as an easy way for us to know that keys we find during the BFS are not yet owned.
    unlocked_grid = dict(grid)
    for key in keys_owned:
        unlocked_grid[key_coordinates[key]] = SPACE
        unlocked_grid[door_coordinates[key.upper()]] = SPACE

    # BFS walk the whole grid, and note which keys are accessible now that doors
    # have been unlocked, and the distance to those keys.
    found_keys: dict[str, int] = {}

    queue: list[KeySearchState] = [
        KeySearchState(
            x=start[0],
            y=start[1],
            steps=0,
        ),
    ]
    visited: set[Coord] = set()

    while queue:
        curr_state = queue.pop(0)
        if curr_state.coord in visited:
            continue

        visited.add(curr_state.coord)

        if (char_at_coord := unlocked_grid[curr_state.coord]) in KEYS:
            found_keys[char_at_coord] = curr_state.steps

        x, y = curr_state.coord
        for nx, ny in [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]:
            if unlocked_grid[(nx, ny)] in WALLS:
                continue
            queue.append(
                KeySearchState(
                    x=nx,
                    y=ny,
                    steps=curr_state.steps + 1,
                ),
            )

    return found_keys


def _shortest_path_to_all_keys(grid: dict[Coord, str]) -> int:
    key_coordinates: dict[str, Coord] = {}
    door_coordinates: dict[str, Coord] = {}
    start_position: Coord | None = None

    for k, v in grid.items():
        if v in KEYS:
            key_coordinates[v] = k
        elif v in DOORS:
            door_coordinates[v] = k
        elif v == START:
            start_position = k

    assert start_position is not None

    # We're going to BFS search a route from key to key, building up a set of keys that we're
    # collecting in order, until we have all the keys. We'll use a heap sorted by total steps,
    # so the first state we arrive in with all keys should be the shortest path there.

    queue: list[KeyOrderSearchState] = []
    heappush(
        queue,
        KeyOrderSearchState(
            steps=0,
            keys_owned=[],
        ),
    )

    # TODO can we implement __eq__ and/or __hash__ on the KeyOrderSearchState?
    visited: set[frozenset[str]] = set()

    while queue:
        state = heappop(queue)

        if state.key_set in visited:
            continue

        visited.add(state.key_set)

    next_key_choices = _distance_to_keys_accessible(
        start=(40, 40),
        grid=grid,
        keys_owned=[],
        key_coordinates=key_coordinates,
        door_coordinates=door_coordinates,
    )


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    grid = _parse_grid(raw_input)

    return _shortest_path_to_all_keys(grid)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    pass


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
