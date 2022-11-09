from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

def _checksum(value, offset):
    """Returns a checksum of a string value. The checksum is the numeric sum of all digits in the
    provided string value, if the digit at `offset` places away is the same as the digit currently
    being checked."""

    checksum = 0

    for i, digit in enumerate(value):

        # Check the digit `offset` places away (circling back to the front). If the digits match,
        # append the digit value to the checksum.
        if digit == value[(i + offset) % len(value)]:
            checksum += int(digit)

    return checksum


@aoc_output_formatter(2017, 1, 1, 'checksum for offset 1')
def part_one(value):
    return _checksum(value, 1)


@aoc_output_formatter(2017, 1, 2, 'checksum for offset halfway across')
def part_two(value):
    return _checksum(value, int(len(value)/2))

#---------------------------------------------------------------------------------------------------

def run(input_file):

    value = get_input(input_file)[0]

    part_one(value)
    part_two(value)
