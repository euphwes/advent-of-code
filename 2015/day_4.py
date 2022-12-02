from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

from hashlib import md5

#---------------------------------------------------------------------------------------------------

def __brute_force(key, target):
    """ Brute-force the lowest value of `n` for which the md5 hash of `secret_key{n}` starts with
    the specified target value. """

    md5_startswith_target = lambda k: md5(k).hexdigest().startswith(target)

    for n in int_stream():
        if md5_startswith_target((key + str(n)).encode()):
            return n

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 4, 1, 'answer', assert_answer=346386)
def part_one(key):
    return __brute_force(key, '00000')


@aoc_output_formatter(2015, 4, 2, 'answer', assert_answer=9958218)
def part_two(key):
    return __brute_force(key, '000000')

#---------------------------------------------------------------------------------------------------

def run(input_file):

    key = get_input(input_file)[0]

    part_one(key)
    part_two(key)
