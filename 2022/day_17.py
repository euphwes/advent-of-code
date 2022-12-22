from collections import defaultdict

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 17
YEAR = 2022

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


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
        self.width = 7

        self.n_blocks_resting = 0
        self.latest_gi = None

        self.resting_rows = defaultdict(_empty_row)
        self.falling_rows = defaultdict(_empty_row)

        # populate bottom resting_row with empty row to make later stuff easier
        self.resting_rows[0] = _empty_row()

    def __str__(self):
        printed_rows = list()
        printed_rows.append("+-------+")

        max_height = max(
            (
                max(self.resting_rows.keys()),
                max(self.falling_rows.keys()) if self.falling_rows else 0,
            )
        )

        for i in range(max_height + 1):
            resting = self.resting_rows[i]
            falling = self.falling_rows[i]
            combined = self._combine(resting, falling)

            printed_rows.append(f"|{''.join(combined)}|")
        return "\n".join(reversed(printed_rows))

    def _trim_chamber(self):
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
        combined = list()
        for r, f in zip(resting, falling):
            if r == AIR_SPACE and f == AIR_SPACE:
                combined.append(AIR_SPACE)
            elif r != AIR_SPACE and f != AIR_SPACE:
                raise CannotOccupySameSpaceException()
            elif r != AIR_SPACE:
                combined.append("#")
            elif f != AIR_SPACE:
                combined.append("@")
            else:
                raise ValueError("one of the 4 above cases should have matched")
        return combined

    def _apply_gravity(self):
        """Attempt to make the falling rock fall down a unit."""

        # print("Falling")

        min_occupied_ix = 9999999999999999
        for i, falling_row in reversed(self.falling_rows.items()):
            if all(c == AIR_SPACE for c in falling_row):
                continue
            min_occupied_ix = i

        if min_occupied_ix == 0:
            raise CannotOccupySameSpaceException()

        for i, falling_row in self.falling_rows.items():
            self._combine(self.resting_rows[i - 1], falling_row)

        new_falling_rows = defaultdict(_empty_row)
        for i, falling_row in self.falling_rows.items():
            new_falling_rows[i - 1] = falling_row
        self.falling_rows = new_falling_rows

    def _apply_gust(self, gust):
        """Apply a gust of wind to the rock and maybe move it left or right."""

        # print(f"Gust {gust}")

        # First just see if the rock would hit the wall of the chanber.
        if gust == GUST_RIGHT:
            # If gusting right and the rightmost element of any line is not empty air, then we
            # can't go any further right.
            if any(row[-1] != AIR_SPACE for row in self.falling_rows.values()):
                return

        else:
            # If gusting left and the left element of any line is not empty air, then we
            # can't go any further left.
            if any(row[0] != AIR_SPACE for row in self.falling_rows.values()):
                return

        if gust == GUST_LEFT:
            try:
                for i, falling_row in self.falling_rows.items():
                    self._combine(self.resting_rows[i], _rotate(falling_row, -1))
                for i in self.falling_rows.keys():
                    self.falling_rows[i] = _rotate(self.falling_rows[i], -1)
                return
            except CannotOccupySameSpaceException:
                return
        else:
            try:
                for i, falling_row in self.falling_rows.items():
                    self._combine(self.resting_rows[i], _rotate(falling_row, 1))
                for i in self.falling_rows.keys():
                    self.falling_rows[i] = _rotate(self.falling_rows[i], 1)
                return
            except CannotOccupySameSpaceException:
                return

        # If we don't have any remaining vertical space, then we overlap horizontally with some
        # already-resting rock in the chamber. Get the overlap mapping.

    def simulate_falling_rock(self, rock_pattern, wind_gusts):

        # setup

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

        try:
            # print(self)
            while True:
                gi, gust = next(wind_gusts)
                self.latest_gi = gi

                self._apply_gust(gust)
                # print(self)

                self._apply_gravity()
                # print(self)
        except CannotOccupySameSpaceException:
            for i in self.falling_rows.keys():
                self.resting_rows[i] = self._combine(
                    self.resting_rows[i],
                    self.falling_rows[i],
                )
            self.falling_rows = defaultdict(_empty_row)
            self._trim_chamber()
            self.n_blocks_resting += 1
            # print(self)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(wind_gusts):
    def wind_generator():
        while True:
            yield from enumerate(wind_gusts)

    def block_generator():
        while True:
            yield from enumerate(
                [HORIZONTAL_BLOCK, PLUS_BLOCK, L_BLOCK, VERTICAL_BLOCK, SQUARE_BLOCK]
            )

    endless_wind = wind_generator()

    chamber = RockChamber()

    for _, block in block_generator():
        chamber.simulate_falling_rock(block, endless_wind)
        if chamber.n_blocks_resting == 2022:
            break

    # print(chamber)
    return max(chamber.resting_rows.keys()) + 1


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(wind_gusts):
    wind_gusts_size = len(wind_gusts)

    def wind_generator():
        while True:
            yield from enumerate(wind_gusts)

    def block_generator():
        while True:
            yield from enumerate(
                [HORIZONTAL_BLOCK, PLUS_BLOCK, L_BLOCK, VERTICAL_BLOCK, SQUARE_BLOCK]
            )

    chamber = RockChamber()

    block_gen = block_generator()
    endless_wind = wind_generator()

    is_first_run = True
    bi = None

    while True:

        # TODO trim all but the top N layers of the chamber? and track height separately

        # check if block_count % 10000000 or whatever == 0
        # check that highest row would block a horizontal block when it fell like the chamber
        # bottom did

        # print((bi, chamber.latest_gi))

        # if (bi, chamber.latest_gi) == (0, 0):
        #     print()
        #     print("omg")
        #     print(f"Blocks: {chamber.n_blocks_resting}")
        #     return

        if chamber.n_blocks_resting % 5000 == 0:
            print()
            print((bi, chamber.latest_gi))
            print(f"Blocks: {chamber.n_blocks_resting}")

        if (bi, chamber.latest_gi) == (4, wind_gusts_size - 1):
            print()
            print(f"ixs back to start at n blocks = {chamber.n_blocks_resting}")
            return

        if not is_first_run and (bi, chamber.latest_gi) == (4, wind_gusts_size - 1):
            try:
                most_recent_row_ix = max(chamber.resting_rows.keys())
                most_recent_row = chamber.resting_rows[most_recent_row_ix]
                print(most_recent_row)

                if 1000000000000 % chamber.n_blocks_resting == 0:
                    chamber._combine(most_recent_row, HORIZONTAL_BLOCK[0])
            except CannotOccupySameSpaceException:
                mult = 1000000000000 // chamber.n_blocks_resting
                return mult * (max(chamber.resting_rows.keys()) + 1)

        bi, block = next(block_gen)
        chamber.simulate_falling_rock(block, endless_wind)

        is_first_run = False


# ----------------------------------------------------------------------------------------------


def run(input_file):

    wind_gusts = get_input(input_file)[0]

    part_one(wind_gusts)
    # part_two(wind_gusts)
