from util.decorators import aoc_output_formatter
from util.input import get_input

DAY  = 1
YEAR = 2018

PART_ONE_DESCRIPTION = 'resulting frequency'
PART_ONE_ANSWER = 420

PART_TWO_DESCRIPTION = 'first frequency reached twice'
PART_TWO_ANSWER = 227

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(frequency_changes):
    return sum(frequency_changes)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
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
