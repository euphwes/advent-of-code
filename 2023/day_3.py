from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import nested_iterable
from string import digits
from math import prod
from collections import defaultdict

DAY = 3
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of all of the part numbers in the engine schematic"
PART_ONE_ANSWER = 527364

PART_TWO_DESCRIPTION = "sum of all of the gear ratios in the engine schematic"
PART_TWO_ANSWER = 79026871


def _is_adjacent_to_symbol(x, y, engine_schematic):
    """Returns if any coordinate adjacent to the provided (x,y) coordinate contains a symbol,
    i.e. a non-digit and non-period character."""

    for dx, dy in nested_iterable([-1, 0, 1], [-1, 0, 1]):
        try:
            neigh_char = engine_schematic[y + dy][x + dx]
            if neigh_char not in digits and neigh_char != ".":
                return True
        except:
            pass

    return False


def _get_part_numbers_and_coords(engine_schematic):
    """Returns a dictionary of part numbers to a list of the coordinates their digits occupy
    in the engine schematic. A part number is any number that's adjacent to a symbol (that's
    not a period)."""

    number_coords = list()

    # Iterate the engine schematic line by line, left to right, recording the sets of
    # consecutive coordinates that contain numbers
    #
    # ..123....
    # .........
    #
    # would yield [(2, 0), (3, 0), (4, 0)] corresponding to the coordinates that "123" covers
    for y in range(len(engine_schematic)):
        curr_num = ""
        coords = list()
        for x in range(len(engine_schematic[0])):
            char = engine_schematic[y][x]
            if char in digits:
                curr_num += char
                coords.append((x, y))
            else:
                if curr_num:
                    number_coords.append(coords)
                    coords = list()
                    curr_num = ""
        if curr_num:
            number_coords.append(coords)
            coords = list()
            curr_num = ""

    number_coords_of_parts = defaultdict(list)

    # For every set of coordinates that correspond to a number, iterate over those coordinates
    # and see if any of them are adjacent to a "symbol" (any non-digit, non-period character).
    # If they are, that number is a "part number".
    for coords_set in number_coords:
        if any(_is_adjacent_to_symbol(x, y, engine_schematic) for x, y in coords_set):
            chars = ""
            for x, y in coords_set:
                chars += engine_schematic[y][x]

            # There are duplicate part numbers across the schematic, but we need to remember
            # each part's distinct set of coordinates. If we've already seen a part number,
            # keep prepending 0 to the front (so the integer value remains the same) but it's
            # a distinct string.
            while chars in number_coords_of_parts.keys():
                chars = f"0{chars}"

            number_coords_of_parts[chars] = coords_set
            continue

    return number_coords_of_parts


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(engine_schematic):
    part_nums = _get_part_numbers_and_coords(engine_schematic).keys()
    return sum([int(n) for n in part_nums])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(engine_schematic):
    part_nums_to_coords = _get_part_numbers_and_coords(engine_schematic)

    def _get_partnums_adj(target_x, target_y):
        """Return a list of part nums which are adjacent to the provided target coordinate."""
        part_nums = list()
        for part_num, part_num_coords in part_nums_to_coords.items():
            for dx, dy in nested_iterable([-1, 0, 1], [-1, 0, 1]):
                if (target_x + dx, target_y + dy) in part_num_coords:
                    part_nums.append(int(part_num))
                    break
        return part_nums

    gear_ratios = list()

    # Iterate over only the symbols in the engine schematic
    for x, y in nested_iterable(
        range(len(engine_schematic[0])),
        range(len(engine_schematic)),
    ):
        char = engine_schematic[y][x]
        if char in digits or char == ".":
            continue

        # Get all the part numbers adjacent to the symbol.
        # If the number of adjacent parts is exactly two, they form a gear.
        # The gear ratio is the product of the two part numbers.
        part_nums = _get_partnums_adj(x, y)
        if len(part_nums) == 2:
            gear_ratios.append(prod(part_nums))

    return sum(gear_ratios)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    engine_schematic = get_input(input_file)

    part_one(engine_schematic)
    part_two(engine_schematic)
