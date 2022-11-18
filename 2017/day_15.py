from util.decorators import aoc_output_formatter
from util.input import get_input

#---------------------------------------------------------------------------------------------------

DEFAULT_ALWAYS_TRUE = lambda _: True

def _generator(initial_value, factor, condition=DEFAULT_ALWAYS_TRUE):
    """ Builds a generatpr which is seeded with an initial value, and then continuously multiples
    the previous value by a provided factor, takes the remainder of that value and a divisor, and
    yields that result if the provided condition is true. """

    previous_value = initial_value

    while True:
        previous_value = (previous_value * factor) % 2147483647
        if condition(previous_value):
            yield previous_value


def _judge(generator_a, generator_b, num_iterations):
    """ The judge compares the output of both generators over the specified number of iterations,
    returning the number of times the lowest 16 bits of the generated values match. """

    # We want to compare the lowest 16 bits, so let's build a bitmask.
    bitmask = int('1111111111111111', base=2)

    count_matches = 0
    for _ in range(num_iterations):
        if (next(generator_a) & bitmask) == (next(generator_b) & bitmask):
            count_matches += 1

    return count_matches


@aoc_output_formatter(2017, 15, 1, "judge's initial score")
def part_one(gen_a_start, gen_b_start):

    gen_a = _generator(gen_a_start, factor=16807)
    gen_b = _generator(gen_b_start, factor=48271)

    return _judge(gen_a, gen_b, 40_000_000)


@aoc_output_formatter(2017, 15, 2, "judge's score with new logic")
def part_two(gen_a_start, gen_b_start):

    def _divisible_by_(n):
        return lambda x: x % n == 0

    gen_a = _generator(gen_a_start, factor=16807, condition=_divisible_by_(4))
    gen_b = _generator(gen_b_start, factor=48271, condition=_divisible_by_(8))

    return _judge(gen_a, gen_b, 5_000_000)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    gen_a_start, gen_b_start = 699, 124

    part_one(gen_a_start, gen_b_start)
    part_two(gen_a_start, gen_b_start)
