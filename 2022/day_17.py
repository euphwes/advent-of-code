from collections import defaultdict
from email.policy import default

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 17
YEAR = 2022

PART_ONE_DESCRIPTION = "height after 2022 blocks"
PART_ONE_ANSWER = 3179

PART_TWO_DESCRIPTION = "height after 1 trillion blocks"
PART_TWO_ANSWER = 1567723342929

ONE_TRILLION = 1_000_000_000_000

GUST_RIGHT = ">"
GUST_LEFT = "<"

AIR_SPACE = "."

# Rock patterns defined with the chamber in mind -- that it's 7 wide units wide, and that the
# rocks appear in the chamber with its left-most edge 2 units away from the left wall.

HORIZONTAL_BLOCK = [
    list("..####."),
]

PLUS_BLOCK = [
    list("...#..."),
    list("..###.."),
    list("...#..."),
]

L_BLOCK = [
    list("....#.."),
    list("....#.."),
    list("..###.."),
]

VERTICAL_BLOCK = [
    list("..#...."),
    list("..#...."),
    list("..#...."),
    list("..#...."),
]

SQUARE_BLOCK = [
    list("..##..."),
    list("..##..."),
]


def block_generator():
    while True:
        yield from enumerate(
            [HORIZONTAL_BLOCK, PLUS_BLOCK, L_BLOCK, VERTICAL_BLOCK, SQUARE_BLOCK]
        )


def _rotate(sequence, steps):
    """Rotates a sequence by N steps, wrapping elements back to the beginning. A positive step
    value rotates to the right.

    Ex:
    _rotate('--A--', 1)
    gives
    '---A-'

    _rotate('ABCDE', -2)
    gives
    'CDEAB'
    """

    steps = steps % len(sequence)
    return sequence[-steps:] + sequence[:-steps]


def _empty_row():
    return list(".......")


class CannotOccupySameSpaceException(Exception):
    pass


class RockChamber:
    def __init__(self):
        self.height = 0

        self.n_blocks_resting = 0
        self.latest_gi = None

        self.resting_rows = defaultdict(_empty_row)
        self.falling_rows = defaultdict(_empty_row)

        # Ppopulate bottom resting_row with empty row so we can assume later we always have at
        # least one row.
        self.resting_rows[0] = _empty_row()

    def _trim_chamber(self):
        """Trim the chamber by removing empty air rows above the highest row containing a
        resting rock."""

        to_del = list()

        i = max(self.resting_rows.keys())
        while True:
            if all(c == AIR_SPACE for c in self.resting_rows[i]):
                to_del.append(i)
                i -= 1
                continue
            break

        for i in to_del:
            del self.resting_rows[i]

    def _combine(self, resting, falling):
        """Accept a rows representing a single horizontal layer of a resting rock and of a
        falling rock, and combine them into single row if possible. Otherwise if impossible
        because falling and resting rocks would occupy the same space, raise a
        CannotOccupySameSpaceException for control flow."""

        combined = list()
        for r, f in zip(resting, falling):
            if r == AIR_SPACE and f == AIR_SPACE:
                combined.append(AIR_SPACE)
            elif r != AIR_SPACE and f != AIR_SPACE:
                raise CannotOccupySameSpaceException()
            elif r != AIR_SPACE or f != AIR_SPACE:
                combined.append("#")
            else:
                raise ValueError("One of the 3 above cases should have matched")
        return combined

    def _apply_gravity(self):
        """Makes a falling rock move down by one unit, unless it cannot because it would enter a
        space occupied by a resting rock."""

        # First check if the falling rock has reached the very bottom row (ix=0), meaning it
        # reached the chamber floor. This would be the very first falling rock. If yes, raise
        # CannotOccupySameSpaceException to have the rock come to rest.
        if min(self.falling_rows.keys()) == 0:
            raise CannotOccupySameSpaceException()

        # Otherwise, attempt a _combine for each falling row on the resting row beneath it. If
        # any cannot move downwards, we'll raise CannotOccupySameSpaceException (from inside
        # _combine) to indicate the rock is coming to rest.
        for i, falling_row in self.falling_rows.items():
            self._combine(self.resting_rows[i - 1], falling_row)

        # No collisions, move all the falling rock rows down one unit.
        new_falling_rows = defaultdict(_empty_row)
        for i, falling_row in self.falling_rows.items():
            new_falling_rows[i - 1] = falling_row
        self.falling_rows = new_falling_rows

    def _apply_gust(self, gust):
        """Apply a gust of wind to the rock and maybe move it left or right."""

        # First just see if the rock would hit the wall of the chamber. If moving left, make
        # sure the leftmost occupied rock is not at column 0. If moving right, make sure the
        # rightmost occupied rock is not at the highest column index (accessed via -1).
        x_to_check = -1 if gust == GUST_RIGHT else 0
        if any(row[x_to_check] != AIR_SPACE for row in self.falling_rows.values()):
            return

        # Then check if moving each falling rock row left or right would cause it to collide
        # with a resting rock row at the same height.
        dx = -1 if gust == GUST_LEFT else 1
        try:
            # First try to see if it's possible to move each row.
            for i, falling_row in self.falling_rows.items():
                self._combine(self.resting_rows[i], _rotate(falling_row, dx))

            # If we reach here, it's possible (otherwise exception would've been raised). Now we
            # actually commit the change for each moved row.
            for i in self.falling_rows.keys():
                self.falling_rows[i] = _rotate(self.falling_rows[i], dx)
            return
        except CannotOccupySameSpaceException:
            return

    def simulate_falling_rock(self, rock_pattern, wind_gusts):
        """Simulate a falling block by alternating blasting it with wind and then having it fall
        down a unit, until the block comes to rest."""

        # A new falling block comes into existence 3 spaces above the highest resting block.
        self.falling_rows = defaultdict(_empty_row)
        max_height = max(self.resting_rows.keys())
        if self.n_blocks_resting == 0:
            self.resting_rows[max_height + 1] = _empty_row()
            self.resting_rows[max_height + 2] = _empty_row()

            for i, falling_row in enumerate(reversed(rock_pattern)):
                self.falling_rows[max_height + 3 + i] = falling_row
        else:
            self.resting_rows[max_height + 1] = _empty_row()
            self.resting_rows[max_height + 2] = _empty_row()
            self.resting_rows[max_height + 3] = _empty_row()

            for i, falling_row in enumerate(reversed(rock_pattern)):
                self.falling_rows[max_height + 4 + i] = falling_row

        # Continue alternating wind and gravity until the falling block would occupy the same
        # space as a resting block...
        try:
            while True:
                gi, gust = next(wind_gusts)
                self.latest_gi = gi

                self._apply_gust(gust)
                self._apply_gravity()

        # ... then bring the falling block to rest.
        except CannotOccupySameSpaceException:
            # Combine the falling and resting block rows.
            for i in self.falling_rows.keys():
                self.resting_rows[i] = self._combine(
                    self.resting_rows[i],
                    self.falling_rows[i],
                )
            # Trim the chamber of excess empty air space at the top, calculate new current
            # height and add one block to the resting blocks count.
            self._trim_chamber()
            self.height = max(self.resting_rows.keys()) + 1
            self.n_blocks_resting += 1


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(wind_gusts):

    chamber = RockChamber()

    def wind_generator():
        while True:
            yield from enumerate(wind_gusts)

    endless_wind = wind_generator()

    for _, block in block_generator():
        chamber.simulate_falling_rock(block, endless_wind)
        if chamber.n_blocks_resting == 2022:
            break

    return chamber.height


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(wind_gusts):

    chamber = RockChamber()
    wind_gusts_size = len(wind_gusts)

    def wind_generator():
        while True:
            yield from enumerate(wind_gusts)

    endless_wind = wind_generator()
    block_gen = block_generator()

    seen_states = defaultdict(list)

    bi = None
    while True:

        if chamber.latest_gi == wind_gusts_size - 1:

            bigi_key = (chamber.latest_gi, bi)
            seen_states[bigi_key].append((chamber.n_blocks_resting, chamber.height))

            # We've identified a cycle if we're back to the same next wind gust and block.
            # Find the delta of blocks and height in between the last two times we saw this
            # state and fast-forward as close to we can to 1 trillion blocks, then let the rest
            # of the simulation finish out.
            if len(seen_states[bigi_key]) == 2:
                s1 = seen_states[bigi_key].pop(-1)
                s2 = seen_states[bigi_key].pop(-1)

                delta_blocks = s1[0] - s2[0]
                delta_height = s1[1] - s2[1]

                remaining = ONE_TRILLION - chamber.n_blocks_resting
                multiplier = remaining // delta_blocks

                chamber.n_blocks_resting += multiplier * delta_blocks
                new_resting_rows = defaultdict(_empty_row)
                for i, row in chamber.resting_rows.items():
                    new_resting_rows[i + (multiplier * delta_height)] = row
                chamber.resting_rows = new_resting_rows

        bi, block = next(block_gen)
        chamber.simulate_falling_rock(block, endless_wind)

        if chamber.n_blocks_resting == ONE_TRILLION:
            return chamber.height


# ----------------------------------------------------------------------------------------------


def run(input_file):

    wind_gusts = get_input(input_file)[0]

    part_one(wind_gusts)
    part_two(wind_gusts)
