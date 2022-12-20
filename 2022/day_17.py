from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 17
YEAR = 2022

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


AIR_SPACE = "."

# Rock patterns defined with the chamber in mind -- that it's 7 wide units wide, and that the
# rocks appear in the chamber with its left-most edge 2 units away from the left wall.

HORIZONTAL_BLOCK = [
    list("..@@@@."),
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


class RockChamber:
    def __init__(self):
        self.width = 7

        # Holds the rows of the chamber such that each row in the list corresponds to the next
        # row higher up in the chamber.
        #
        # Ex: self.rows = [
        #     '..####.',
        #     '...##..',
        #     '...##..',
        #     '....###',
        # ]
        #
        # Looks like this if you print the chamber
        #
        #     |....###|
        #     |...##..|
        #     |...##..|
        #     |..####.|
        #     +-------+
        self.rows = list()

    def simulate_falling_rock(self, rock_pattern, wind_gusts_gen):

        # Add 3 rows of empty airspace between the falling rock and the top row of the chamber
        rock_to_chamber_airspace = 3
        for _ in range(rock_to_chamber_airspace):
            self.rows.append(list("......."))

        while True:
            gust = next(wind_gusts_gen)

    def __str__(self):
        printed_rows = list()
        printed_rows.append("\n")
        printed_rows.append("+-------+")
        for row in self.rows:
            printed_rows.append(f"|{row}|")
        printed_rows.append("\n")
        return "\n".join(printed_rows)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(wind_gusts):
    chamber = RockChamber()
    print(chamber)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(wind_gusts):
    pass


# ----------------------------------------------------------------------------------------------


def run(input_file):

    wind_gusts = get_input(input_file)[0]

    part_one(wind_gusts)
    part_two(wind_gusts)
