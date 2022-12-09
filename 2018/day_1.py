from util.decorators import aoc_output_formatter
from util.input import get_input

DAY  = 1
YEAR = 2018

PART_ONE_DESC = 'resulting frequency'
PART_TWO_DESC = 'first frequency reached twice'

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESC, assert_answer=420)
def part_one(frequency_changes):
    return sum(frequency_changes)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESC, assert_answer=227)
def part_two(frequency_changes):

    frequency = 0
    seen_frequencies = set()

    while True:
        for n in frequency_changes:
            frequency += n
            if frequency in seen_frequencies:
                return frequency
            else:
                seen_frequencies.add(frequency)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    frequency_changes = list(map(int, get_input(input_file)))

    part_one(frequency_changes)
    part_two(frequency_changes)
