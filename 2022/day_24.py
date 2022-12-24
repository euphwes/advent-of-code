from dataclasses import dataclass
from typing import Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 24
YEAR = 2022

PART_ONE_DESCRIPTION = "Fewest minutes to reach the exit"
PART_ONE_ANSWER = 308

PART_TWO_DESCRIPTION = "Fewest minutes to round-trip and then reach the exit"
PART_TWO_ANSWER = 908


@dataclass(frozen=True)
class Blizzard:
    """Represents a blizzard which has a location and is traveling in a specific direction. Due
    to conservation of blizzard energy, it'll wrap back around to the opposite side at ix=1
    (because ix=0 is the bounding wall) or to the max_x/y position it can occupy."""

    coord: Tuple[int, int]
    dir: str
    max_x: int
    max_y: int

    def next(self):
        # Move the blizzard 1 unit in the specified direction.
        x, y = self.coord
        x, y = {
            "r": (x + 1, y),
            "l": (x - 1, y),
            "u": (x, y - 1),
            "d": (x, y + 1),
        }[self.dir]

        # Wrap the blizzard around if it goes out of bounds.
        if x > self.max_x:
            x = 1
        if x < 1:
            x = self.max_x
        if y < 1:
            y = self.max_y
        if y > self.max_y:
            y = 1

        # Return a new Blizzard instance at the next coordinate.
        return Blizzard(
            coord=(x, y),
            dir=self.dir,
            max_x=self.max_x,
            max_y=self.max_y,
        )


def _find_entrances(starting_map):
    """Find the coords of the entrance and exit along the bounding box."""

    entrance = None
    for i, c in enumerate(starting_map[0]):
        if c == ".":
            entrance = (i, 0)

    exit = None
    for i, c in enumerate(starting_map[-1]):
        if c == ".":
            exit = (i, len(starting_map) - 1)

    if entrance is None or exit is None:
        raise Exception("Can't find either an entrance or exit")

    return entrance, exit


def _parse_blizzard_starts(starting_map, max_x, max_y):
    """Parse the starting map for blizzard info, and return a blizzards map which contains the
    set of blizzards at time t=0."""

    blizzards = dict()
    blizzards[0] = list()

    blizz_dir_map = {
        ">": "r",
        "<": "l",
        "v": "d",
        "^": "u",
    }

    for y, row in enumerate(starting_map):
        for x, cell in enumerate(row):
            if cell in set("#."):
                continue
            blizzards[0].append(
                Blizzard(
                    coord=(x, y),
                    dir=blizz_dir_map[cell],
                    max_x=max_x,
                    max_y=max_y,
                )
            )

    return blizzards


def _get_neighbors_at(coord, enter, exit, t, blizzards, max_x, max_y):
    """Return the possible next positions from the current coordinate at the timestep t, based
    on where the blizzards will be at that time."""

    # Start off assuming that we can visit any adjacent (non-diagonal) grid coordinate, or stay
    # in the same place.
    cx, cy = coord
    candidates = [
        (cx, cy),
        (cx + 1, cy),
        (cx - 1, cy),
        (cx, cy + 1),
        (cx, cy - 1),
    ]

    # Filter out the candidate next coordinates which are outside the bounds.
    bounds_filtered = list()
    for x, y in candidates:
        if x < 1 or x > max_x or y < 1 or y > max_y:
            continue
        bounds_filtered.append((x, y))

    # Get the coordinates of the blizzards at timestep t. If we haven't calculuated where the
    # blizzards are going to be at that time yet, do so now based on their positions at the
    # previous timestep.
    if t not in blizzards.keys():
        blizzards[t] = [blizz.next() for blizz in blizzards[t - 1]]

    blizz_coords = set(blizz.coord for blizz in blizzards[t])

    # Filter out candidate next coordinates where a blizzard will be.
    blizzard_filtered = list()
    for cand_coord in bounds_filtered:
        if cand_coord in blizz_coords:
            continue
        blizzard_filtered.append(cand_coord)

    # Add back in the exit and entrance if they are neighbors because the bounds filter would
    # have removed it above (because the exit and entrances are the only visitable spots on the
    # boundary).
    cx, cy = coord
    if (cx, cy + 1) == exit:
        blizzard_filtered.append(exit)
    elif (cx, cy - 1) == exit:
        blizzard_filtered.append(exit)
    blizzard_filtered.append(enter)

    return blizzard_filtered


def _get_outta_da_cold(start, exit, start_t, blizzards, max_x, max_y):
    """BFS a path through the blizzard from the start coordinate to the exit coordinate,
    starting at time T."""

    queue = list()
    queue.append((start, start_t))

    visited = set()

    while queue:
        current, t = queue.pop(0)
        if current == exit:
            return t

        for neighbor in _get_neighbors_at(
            current, start, exit, t + 1, blizzards, max_x, max_y
        ):
            # "Visited" isn't just a set of coordinates we've visited, it's a set of coordinates
            # at specific timesteps because the surrounding blizzard positions will be different
            next_state = (neighbor, t + 1)
            if next_state in visited:
                continue
            visited.add(next_state)
            queue.append(next_state)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(starting_map):

    entrance, exit = _find_entrances(starting_map)
    max_x = len(starting_map[0]) - 2
    max_y = len(starting_map) - 2

    blizzards = _parse_blizzard_starts(starting_map, max_x, max_y)

    return _get_outta_da_cold(entrance, exit, 0, blizzards, max_x, max_y)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(starting_map, exit_time):

    entrance, exit = _find_entrances(starting_map)
    max_x = len(starting_map[0]) - 2
    max_y = len(starting_map) - 2

    # Since we re-parsed the blizzard info from the input, we have to pre-fill the blizzards at
    # timesteps up through the `exit_time` passed in to part two here from part one previously.
    blizzards = _parse_blizzard_starts(starting_map, max_x, max_y)
    for t in range(1, exit_time + 1):
        blizzards[t] = [blizz.next() for blizz in blizzards[t - 1]]

    # Oh crap, forgot snacks, have to go backwards to the start (starting at time `exit_time`).
    t2 = _get_outta_da_cold(exit, entrance, exit_time, blizzards, max_x, max_y)

    # Now we have snacks, go back to the exit starting from time t2.
    return _get_outta_da_cold(entrance, exit, t2, blizzards, max_x, max_y)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    starting_map = get_input(input_file)

    exit_time = part_one(starting_map)
    part_two(starting_map, exit_time)
