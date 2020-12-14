from util.decorators import aoc_output_formatter
from util.input import get_input

from itertools import combinations

#---------------------------------------------------------------------------------------------------

def __check_value_against_preamble(value, preamble):
    """ Returns true if the provided value can be expressed as the sum of any two numbers in the
    provided preamble. Returns false otherwise. """

    for a, b in combinations(preamble, 2):
        if a + b == value:
            return True

    return False

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 9, 1, "first value which doesn't match preamble")
def part_one(input_lines):
    preamble = input_lines[:25]
    message = input_lines[25:]

    for i, value in enumerate(input_lines[25:]):
        if not __check_value_against_preamble(value, input_lines[i:25+i]):
            return value


@aoc_output_formatter(2020, 9, 2, 'encryption weakness')
def part_two(input_lines):
    for i, value in enumerate(input_lines[25:]):
        if not __check_value_against_preamble(value, input_lines[i:25+i]):
            target_value = value

    for n in range(2, len(input_lines)):
        for i in range(0, len(input_lines)-n+1):
            contiguous_values = input_lines[i:i+n]
            if sum(contiguous_values) == target_value:
                return min(contiguous_values) + max(contiguous_values)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    part_one([int(n) for n in get_input(input_file)])
    part_two([int(n) for n in get_input(input_file)])
