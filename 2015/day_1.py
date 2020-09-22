from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

paren_map = lambda char: 1 if char == '(' else -1

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 1, 1, 'floor')
def part_one(floor_instructions):
    return sum([paren_map(char) for char in floor_instructions])


@aoc_output_formatter(2015, 1, 2, 'basement index')
def part_two(floor_instructions):
    floor = 0
    for i, val in enumerate([paren_map(char) for char in floor_instructions]):
        floor += val
        if floor < 0:
            return i + 1

#---------------------------------------------------------------------------------------------------

def run(input_file):

    floor_instructions = get_input(input_file)[0]

    part_one(floor_instructions)
    part_two(floor_instructions)
