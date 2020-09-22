from util.decorators import aoc_output_formatter
from util.input import get_input

from hashlib import md5

#---------------------------------------------------------------------------------------------------

def __brute_force(key, target):
    """ Brute-force the lowest value of `n` for which the md5 hash of `secret_key{n}` starts with
    the specified target value. """

    n = 1
    while True:
        if md5((key + str(n)).encode()).hexdigest().startswith(target):
            return n
        n += 1

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 4, 1, 'answer')
def part_one(key):
    return __brute_force(key, '00000')


@aoc_output_formatter(2015, 4, 2, 'answer')
def part_two(key):
    return __brute_force(key, '000000')

#---------------------------------------------------------------------------------------------------

def run(input_file):

    key = get_input(input_file)[0]

    part_one(key)
    part_two(key)
