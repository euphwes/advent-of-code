from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 17
YEAR = 2015

PART_ONE_DESCRIPTION = "ways to make 150 liters eggnog"
PART_ONE_ANSWER = 1304

PART_TWO_DESCRIPTION = "ways to make 150 liters eggnog in minimum containers"
PART_TWO_ANSWER = 18


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(containers):

    count = 0
    for n in range(1, len(containers) + 1):
        count += sum(1 for p in combinations(containers, n) if sum(p) == 150)

    return count


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(containers):

    for n in range(1, len(containers) + 1):
        count_for_size = sum(1 for p in combinations(containers, n) if sum(p) == 150)
        if count_for_size > 0:
            return count_for_size


# ----------------------------------------------------------------------------------------------


def run(input_file):

    containers = [int(n) for n in get_input(input_file)]

    part_one(containers)
    part_two(containers)
