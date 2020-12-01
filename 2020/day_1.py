from util.decorators import aoc_output_formatter
from util.input import get_input

from itertools import combinations

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2020, 1, 1, 'product of 2 entries summing to 2020')
def part_one(entries):
    for a, b in combinations(entries, 2):
        if a + b == 2020:
            return a * b


@aoc_output_formatter(2020, 1, 2, 'product of 3 entries summing to 2020')
def part_two(entries):
    for a, b, c in combinations(entries, 3):
        if a + b + c == 2020:
            return a * b * c

#---------------------------------------------------------------------------------------------------

def run(input_file):

    entries = [int(line) for line in get_input(input_file)]

    part_one(entries)
    part_two(entries)
