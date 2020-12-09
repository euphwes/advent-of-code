from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def __parse_seat_coordinates(line):
    """ Determines seat coordinates (which row and column) by parsing a line representing a boarding
    pass, which reduces the seat coordinate possibilities using binary partioning. """

    # ex: FFBBFBFLLL
    possible_rows = list(range(128))
    possible_cols = list(range(8))

    for char in line[:7]:
        div_point = int(len(possible_rows)/2)
        if char == 'F':
            possible_rows = possible_rows[:div_point]
        else:
            possible_rows = possible_rows[div_point:]

    for char in line[7:]:
        div_point = int(len(possible_cols)/2)
        if char == 'L':
            possible_cols = possible_cols[:div_point]
        else:
            possible_cols = possible_cols[div_point:]

    return possible_rows[0], possible_cols[0]

# Calculate the seat ID based on row and column
__seat_id = lambda row, column: (row * 8) + column

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 5, 1, 'highest seat ID')
def part_one(input_lines):
    seat_coords = [__parse_seat_coordinates(line) for line in input_lines]
    seat_ids    = [__seat_id(row, col) for row, col in seat_coords]
    return max(seat_ids)


@aoc_output_formatter(2020, 5, 2, 'your seat ID')
def part_two(input_lines):
    seat_coords = [__parse_seat_coordinates(line) for line in input_lines]
    seat_ids    = set([__seat_id(row, col) for row, col in seat_coords])

    for i in range(128*8):
        if i not in seat_ids and i+1 in seat_ids and i-1 in seat_ids:
            return i

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))
