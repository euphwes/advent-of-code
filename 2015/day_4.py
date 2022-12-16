from hashlib import md5

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 4
YEAR = 2015

PART_ONE_DESCRIPTION = "lowest positive int which produces a hash with 5 leading zeroes"
PART_ONE_ANSWER = 346386

PART_TWO_DESCRIPTION = "lowest positive int which produces a hash with 6 leading zeroes"
PART_TWO_ANSWER = 9958218


def __brute_force(key, target):
    """Brute-force the lowest value of `n` for which the md5 hash of `secret_key{n}` starts with
    the specified target value."""

    md5_startswith_target = lambda k: md5(k).hexdigest().startswith(target)

    for n in int_stream():
        if md5_startswith_target((key + str(n)).encode()):
            return n


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(key):
    return __brute_force(key, "00000")


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(key):
    return __brute_force(key, "000000")


# ----------------------------------------------------------------------------------------------


def run(input_file):

    key = get_input(input_file)[0]

    part_one(key)
    part_two(key)
