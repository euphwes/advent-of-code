from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 23
YEAR = 2022

# TODO make this faster later!
# TODO can we only consider elves which have moved in the last N rounds?
# Things are probably fairly static in the middle of the pack of elves after a while.

PART_ONE_DESCRIPTION = "count of empty tiles in smallest rectangle holding all elves"
PART_ONE_ANSWER = 4181

PART_TWO_DESCRIPTION = "which round is the first where no elves move"
PART_TWO_ANSWER = 973


@dataclass
class MovementRule:
    dirs_to_check: List[Tuple[int, int]]
    to_move: Tuple[int, int]


DELTA_N = (0, -1)
DELTA_NE = (1, -1)
DELTA_NW = (-1, -1)

DELTA_E = (1, 0)
DELTA_W = (-1, 0)

DELTA_S = (0, 1)
DELTA_SE = (1, 1)
DELTA_SW = (-1, 1)

ALL_DELTAS = [
    DELTA_N,
    DELTA_NE,
    DELTA_E,
    DELTA_SE,
    DELTA_S,
    DELTA_SW,
    DELTA_W,
    DELTA_NW,
]


def _starting_rules():
    return [
        MovementRule(
            dirs_to_check=[DELTA_N, DELTA_NE, DELTA_NW],
            to_move=DELTA_N,
        ),
        MovementRule(
            dirs_to_check=[DELTA_S, DELTA_SE, DELTA_SW],
            to_move=DELTA_S,
        ),
        MovementRule(
            dirs_to_check=[DELTA_W, DELTA_NW, DELTA_SW],
            to_move=DELTA_W,
        ),
        MovementRule(
            dirs_to_check=[DELTA_E, DELTA_NE, DELTA_SE],
            to_move=DELTA_E,
        ),
    ]


@dataclass
class Elf:
    id: int
    x: int
    y: int
    rules: List[MovementRule]
    just_moved: bool

    @property
    def coord(self):
        return (self.x, self.y)

    @property
    def rotated_rules(self):
        return self.rules[1:] + self.rules[0:1]

    def wait(self):
        return Elf(
            id=self.id,
            x=self.x,
            y=self.y,
            rules=self.rotated_rules,
            just_moved=False,
        )

    def next(self, current_elf_locations):
        """Figures out where this elf is moving next (if anywhere at all, and returns a new Elf
        dataclass instance representing an elf at that location."""

        # First check if the elf has any neighbors. If there are no neighbors, the elf doesn't
        # need to move.
        has_no_neighbors = True
        for delta in ALL_DELTAS:
            dx, dy = delta
            nx = self.x + dx
            ny = self.y + dy
            if (nx, ny) in current_elf_locations:
                has_no_neighbors = False
                break

        if has_no_neighbors:
            return self.wait()

        # Next, check each of the movement rules in order. If there are no elves in the
        # specified direction, propose moving that direction.
        for rule in self.rules:
            has_no_neighbors_in_dir = True
            for delta in rule.dirs_to_check:
                dx, dy = delta
                nx = self.x + dx
                ny = self.y + dy
                if (nx, ny) in current_elf_locations:
                    has_no_neighbors_in_dir = False
                    break
            if has_no_neighbors_in_dir:
                to_move = rule.to_move
                dx, dy = to_move
                return Elf(
                    id=self.id,
                    x=self.x + dx,
                    y=self.y + dy,
                    rules=self.rotated_rules,
                    just_moved=True,
                )

        # Otherwise the elf doesn't have anywhere to move, just stay put.
        return self.wait()


def _get_elf_positions(raw_input):
    """Parse the raw problem input and extract the starting positions of all the elves,
    assigning each of them an ID for tracking later and then returning a dict of elf ID to the
    Elf instance."""

    elves = dict()

    elf_id = 0
    for y, row in enumerate(raw_input):
        for x, cell in enumerate(row):
            if cell != "#":
                continue
            elves[elf_id] = Elf(
                id=elf_id,
                x=x,
                y=y,
                rules=_starting_rules(),
                just_moved=False,
            )
            elf_id += 1

    return elves


def _move_elves(elves: Dict):
    """Move each elf to their new location based on their current location, the location of the
    nearby elves around them, and their ruleset."""

    # Get the proposed next location for each elf, and then group them by their proposed coords.
    elves_coords_set = [elf.coord for elf in elves.values()]
    proposed_next_elves = [elf.next(elves_coords_set) for elf in elves.values()]

    proposed_next_by_coord = defaultdict(list)
    for proposed_next_elf in proposed_next_elves:
        proposed_next_by_coord[proposed_next_elf.coord].append(proposed_next_elf)

    # Start a dictionary holding elf ID to that elf's next location. Only include proposed moves
    # where that elf is the only one who proposed moving to that next location.
    actual_next_elves = dict()
    for prop_elves in proposed_next_by_coord.values():
        if len(prop_elves) == 1:
            elf = prop_elves[0]
            actual_next_elves[elf.id] = elf

    # Figure out which elves did not actually move, because they proposed moving to the same
    # coord as another elf. Keep them in the same spot.
    moved_elves = set(actual_next_elves.keys())
    remaining_elves = set(elves.keys()) - moved_elves

    for elf_id in remaining_elves:
        actual_next_elves[elf_id] = elves[elf_id].wait()

    # Figure out if the whole group stayed put.
    whole_group_did_not_move = True
    for elf in actual_next_elves.values():
        if elf.just_moved:
            whole_group_did_not_move = False
            break

    return actual_next_elves, whole_group_did_not_move


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(starting_elf_grid):

    elves = _get_elf_positions(starting_elf_grid)

    for _ in range(10):
        elves, _ = _move_elves(elves)

    raw_coords = [(elf.x, elf.y) for elf in elves.values()]

    min_x = min(x for x, _ in raw_coords)
    max_x = max(x for x, _ in raw_coords)
    min_y = min(y for _, y in raw_coords)
    max_y = max(y for _, y in raw_coords)

    return (((max_x + 1) - min_x) * ((max_y + 1) - min_y)) - len(elves)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(starting_elf_grid):
    elves = _get_elf_positions(starting_elf_grid)

    for i in int_stream(1):
        elves, did_not_move = _move_elves(elves)
        if did_not_move:
            return i


# ----------------------------------------------------------------------------------------------


def run(input_file):

    starting_elf_grid = get_input(input_file)

    part_one(starting_elf_grid)
    part_two(starting_elf_grid)
