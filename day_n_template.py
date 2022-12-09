from util.decorators import aoc_output_formatter
from util.input import get_input

DAY  = 1
YEAR = 2022

PART_ONE_DESC = ''
PART_TWO_DESC = ''

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESC, assert_answer=None)
def part_one(stuff):
    pass


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESC, assert_answer=None)
def part_two(stuff):
    pass

#---------------------------------------------------------------------------------------------------

def run(input_file):

    stuff = get_input(input_file)

    part_one(stuff)
    part_two(stuff)
