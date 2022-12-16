from dataclasses import dataclass
from hashlib import md5
from typing import Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 17
YEAR = 2016

PART_ONE_DESCRIPTION = "shortest path to reach the vault"
PART_ONE_ANSWER = "RRRLDRDUDD"

PART_TWO_DESCRIPTION = "length of the longest path that reaches the vaalt"
PART_TWO_ANSWER = 706

_md5 = lambda x: md5(x.encode()).hexdigest()


@dataclass
class StateGraphNode:
    coord: Tuple[int, int]
    path: str


# Hash characters which indicate the associated door is unlocked
OPEN_CHARS = set("bcdef")


def _get_options(coord, passcode, path):
    """A generator which yields neighboring cells whose doors are unlocked, when arriving at the
    provided coordinate via the specified path. Yields tuple of (neighbor_coord, direction).
    """

    x, y = coord
    hash = _md5(passcode + path)[:4]

    neighbors = [
        ("U", (x - 1, y)),
        ("D", (x + 1, y)),
        ("L", (x, y - 1)),
        ("R", (x, y + 1)),
    ]

    for i, neighbor in enumerate(neighbors):
        direction, next_coord = neighbor
        nx, ny = next_coord

        # Skip invalid coords that are out of bounds of the 4x4 grid
        if nx < 0 or ny < 0 or nx > 3 or ny > 3:
            continue

        # If the door to the neighbor is open, based on the hash from the passcode + path, yield
        # a tuple of this neighbor and the direction taken to get there.
        if hash[i] in OPEN_CHARS:
            yield next_coord, direction


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(passcode):
    state_queue = list()
    state_queue.append(StateGraphNode(coord=(0, 0), path=""))

    while state_queue:
        curr_state = state_queue.pop(0)

        if curr_state.coord == (3, 3):
            return curr_state.path

        for neighbor, direction in _get_options(
            curr_state.coord, passcode, curr_state.path
        ):
            state_queue.append(
                StateGraphNode(coord=neighbor, path=curr_state.path + direction)
            )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(passcode):
    path_lengths = list()

    def _dfs(node):
        if node.coord == (3, 3):
            path_lengths.append(len(node.path))
            return

        for neighbor, direction in _get_options(node.coord, passcode, node.path):
            _dfs(StateGraphNode(coord=neighbor, path=node.path + direction))

    start = StateGraphNode(coord=(0, 0), path="")
    _dfs(start)

    return max(path_lengths)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    passcode = get_input(input_file)[0]

    part_one(passcode)
    part_two(passcode)
