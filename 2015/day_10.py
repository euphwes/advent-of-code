from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

from itertools import permutations

#---------------------------------------------------------------------------------------------------

def __run_length_encode(s):
    """ Run-length encodes the provided string, and returns the result. """

    buffer = list()
    current_char = None

    for i, char in enumerate(s):
        if char == current_char:
            count += 1
        else:
            if i > 0:
                buffer.append(str(count))
                buffer.append(current_char)
            count = 1
            current_char = char

    buffer.append(str(count))
    buffer.append(current_char)

    return ''.join(buffer)

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2015, 10, 1, 'length after 40 RLEs', assert_answer=492982)
def part_one(s, n):
    for _ in range(n):
        s = __run_length_encode(s)
    return len(s)


@aoc_output_formatter(2015, 10, 2, 'length after 50 RLEs', assert_answer=6989950)
def part_two(s, n):
    for _ in range(n):
        s = __run_length_encode(s)
    return len(s)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    input = "1321131112"

    part_one(input, 40)
    part_two(input, 50)
