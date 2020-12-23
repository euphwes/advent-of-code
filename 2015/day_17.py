from util.decorators import aoc_output_formatter
from util.input import get_input

from itertools import combinations

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 17, 1, "ways to fill containers to make 150 liters eggnog")
def part_one(containers):

    count = 0
    for n in range(1, len(containers)+1):
        count += sum(1 for p in combinations(containers, n) if sum(p) == 150)

    return count


@aoc_output_formatter(2015, 17, 2, "ways to fill minimal containers to make 150 liters eggnog")
def part_two(containers):

    for n in range(1, len(containers)+1):
        count_for_size = sum(1 for p in combinations(containers, n) if sum(p) == 150)
        if count_for_size > 0:
            return count_for_size

#---------------------------------------------------------------------------------------------------

def run(input_file):

    containers = [int(n) for n in get_input(input_file)]

    part_one(containers)
    part_two(containers)
