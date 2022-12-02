from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

from math import sqrt, ceil

#---------------------------------------------------------------------------------------------------

def __get_all_divisors_of(n, lazy_elves=False):
    if n == 1:
        return [1]

    if n == 2:
        return [1, 2]

    divisors = set()
    for i in range(1, int(ceil(sqrt(n)))+1):
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


def __get_presents_for_house(n):
    return 10 * sum(__get_all_divisors_of(n))


def __get_presents_for_house_with_lazy_elves(n):
    return 11 * sum(__get_all_divisors_of(n, lazy_elves=True))

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 20, 1, 'first house to get the target present count', assert_answer=786240)
def part_one(target_present_count):
    for n in int_stream():
        if __get_presents_for_house(n) >= target_present_count:
            return n


@aoc_output_formatter(2015, 20, 2, 'first house to get the target present count with lazy elves', assert_answer=831600)
def part_two(target_present_count):
    for n in int_stream():
        if __get_presents_for_house_with_lazy_elves(n) >= target_present_count:
            return n

#---------------------------------------------------------------------------------------------------

def run(input_file):

    target_present_count = int(get_input(input_file)[0])

    part_one(target_present_count)
    part_two(target_present_count)
