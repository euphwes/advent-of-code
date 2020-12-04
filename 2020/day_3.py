from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def __traverse_terrain(terrain, slope):
    """ Traverse the terrain provided, starting at the top-left corner and moving at the slope
    provided. Each row of the terrain repeats the same pattern of trees and open space. Returns
    the number of trees you hit along the way. """

    x, y = 0, 0
    num_rows = len(terrain)
    pattern_length = len(terrain[0])
    num_trees = 0

    right, down = slope

    while True:
        x = (x + right) % pattern_length
        y = y + down
        if y >= num_rows:
            break

        if terrain[y][x] == '#':
            num_trees += 1

    return num_trees

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 3, 1, 'number of trees')
def part_one(terrain):
    return __traverse_terrain(terrain, (3, 1))


@aoc_output_formatter(2020, 3, 2, 'multiplied trees across all slopes')
def part_two(terrain):
    trees_mult_result = 1
    for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        trees_mult_result *= __traverse_terrain(terrain, slope)
    return trees_mult_result

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one(get_input(input_file))
    part_two(get_input(input_file))
