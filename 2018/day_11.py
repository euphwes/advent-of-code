from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream, nested_iterable

DAY = 11
YEAR = 2018

PART_ONE_DESCRIPTION = "x,y identifier of the 3x3 square with highest combined power"
PART_ONE_ANSWER = "33,45"

PART_TWO_DESCRIPTION = "x,y,n identifier of the nxn square with highest combined power"
PART_TWO_ANSWER = "233,116,15"


def _get_power_level_at(x, y, serial_number):
    """Get the power level for a fuel cell at a given coordinate for a grid with the given
    serial number."""

    rack_id = x + 10

    power = rack_id * y
    power += serial_number
    power *= rack_id

    hundreds_digit = str(power).rjust(3, "0")[-3]
    return int(hundreds_digit) - 5


def _build_fuel_cell_grid(serial_number):
    """Build and return a fuel cell grid for a given serial number."""

    return {
        (x, y): _get_power_level_at(x, y, serial_number)
        for x, y in nested_iterable(range(1, 301), range(1, 301))
    }


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(serial_number):
    fuel_grid = _build_fuel_cell_grid(serial_number)

    max_combined_power = 0
    best_coord = (0, 0)

    for x, y in nested_iterable(range(1, 299), range(1, 299)):
        combined_power = 0
        for dx, dy in nested_iterable((0, 1, 2), (0, 1, 2)):
            combined_power += fuel_grid[(x + dx, y + dy)]

        if combined_power > max_combined_power:
            max_combined_power = combined_power
            best_coord = (x, y)

    return f"{best_coord[0]},{best_coord[1]}"


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(serial_number):
    fuel_grid = _build_fuel_cell_grid(serial_number)

    max_combined_power = 0
    best_coord = (0, 0)
    best_size = 0

    for x, y in nested_iterable(range(1, 301), range(1, 301)):

        # For each starting top-left corner coordinate, we're going to keep increasing the size
        # by 1 unit and then checking the combined power after each size increase. Just the one
        # starting coordinate counts as size=1.
        combined_power = fuel_grid[(x, y)]

        # For each larger size, starting at this coordinate...
        for size in int_stream(2):
            try:
                # From the top-left corner, go right by size-1 to get to the top-right corner,
                # in the new column which is added by this size. Hold temp coordinates which
                # we'll iterate over and add to the combined power.
                temp_x = x + size - 1
                temp_y = y

                # Go down the new column to the bottom-right corner, adding to combined power.
                for dy in range(size):
                    coord_y = temp_y + dy
                    combined_power += fuel_grid[(temp_x, coord_y)]

                temp_y = temp_y + size - 1

                # Go left all the way along new row to bottom-left corner, adding to power.
                for dx in range(1, size):
                    coord_x = temp_x - dx
                    combined_power += fuel_grid[(coord_x, temp_y)]

                if combined_power >= max_combined_power:
                    max_combined_power = combined_power
                    best_coord = (x, y)
                    best_size = size

                # It's not mathematically proven or anything, but seems like a reasonable
                # heuristic to identify when to stop checking squares starting at a particular
                # coordinate. If we've hit some threshold size and the combined power is still
                # negative, we're probably not likely to be the ultimate winner if we keep
                # getting larger. `size > 4` gives me the right answer for my input but setting
                # it to something arbitrarily larger feels less like cheating.
                if size > 10 and combined_power < 0:
                    break

            except KeyError:
                break

    return f"{best_coord[0]},{best_coord[1]},{best_size}"


# ----------------------------------------------------------------------------------------------


def run(input_file):

    serial_number = int(get_input(input_file)[0])
    part_one(serial_number)
    part_two(serial_number)
