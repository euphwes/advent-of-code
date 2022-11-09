from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from itertools import combinations

#---------------------------------------------------------------------------------------------------

def _checksum_via_minmax(input_lines):
    """Returns a checksum of list of lines of integers. The checksum is the sum of the differences
    of the minimum and maximum value on each line. """

    checksum = 0
    for line in input_lines:
        littlest = min(line)
        biggest = max(line)
        checksum += biggest - littlest

    return checksum


def _checksum_via_divisibility(input_lines):
    """Returns a checksum of list of lines of integers. The checksum is the sum of the division
    between the only two numbers on each line which evenly divide each other. """

    checksum = 0
    for line in input_lines:
        for n1, n2 in combinations(line, r=2):
            div_result = max((n1, n2)) / min((n1, n2))
            if div_result == int(div_result):
                checksum += div_result
                break

    return int(checksum)


@aoc_output_formatter(2017, 2, 1, 'checksum via min/max')
def part_one(input_lines):
    return _checksum_via_minmax(input_lines)


@aoc_output_formatter(2017, 2, 2, 'checksum via divisibility')
def part_two(input_lines):
    return _checksum_via_divisibility(input_lines)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    input_lines = get_tokenized_input(input_file, None, int)

    part_one(input_lines)
    part_two(input_lines)
