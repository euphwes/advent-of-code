from math import ceil, sqrt

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 20
YEAR = 2015

PART_ONE_DESCRIPTION = "first house to get the target present count"
PART_ONE_ANSWER = 786240

PART_TWO_DESCRIPTION = "first house to get the target present count with lazy elves"
PART_TWO_ANSWER = 831600


def _get_all_divisors_of(n, lazy_elves=False):
    if n == 1:
        return [1]

    if n == 2:
        return [1, 2]

    divisors = set()
    for i in range(1, int(ceil(sqrt(n))) + 1):
        if n % i == 0:
            if lazy_elves:
                if n < (50 * i):
                    divisors.add(i)
                if n < (50 * (n / i)):
                    divisors.add(n / i)
            else:
                divisors.add(i)
                divisors.add(n / i)

    return list(divisors)


def _get_presents_for_house(n):
    return 10 * sum(_get_all_divisors_of(n))


def _get_presents_for_house_with_lazy_elves(n):
    return 11 * sum(_get_all_divisors_of(n, lazy_elves=True))


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(target_present_count):
    for n in int_stream():
        if _get_presents_for_house(n) >= target_present_count:
            return n


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(target_present_count):
    for n in int_stream():
        if _get_presents_for_house_with_lazy_elves(n) >= target_present_count:
            return n


# ----------------------------------------------------------------------------------------------


def run(input_file):

    target_present_count = int(get_input(input_file)[0])

    part_one(target_present_count)
    part_two(target_present_count)
