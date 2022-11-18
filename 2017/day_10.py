from util.decorators import aoc_output_formatter
from util.input import get_input, get_tokenized_input
from .common_2017 import knot_hash, build_dense_hex_hash

#---------------------------------------------------------------------------------------------------

@aoc_output_formatter(2017, 10, 1, 'product of first 2 bytes of 1-iteration knot hash on input')
def part_one(input_integers):
    hashed = knot_hash(input_integers, iterations=1)
    return hashed[0] * hashed[1]


@aoc_output_formatter(2017, 10, 2, 'hex representation of 64-iteration knot hash on input')
def part_two(input_str):
    input_bytes = [ord(c) for c in input_str] + [17, 31, 73, 47, 23]
    sparse_hash = knot_hash(input_bytes, iterations=64)

    return build_dense_hex_hash(sparse_hash)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    input_as_ints = get_tokenized_input(input_file, ',', int)[0]
    part_one(input_as_ints)

    input_as_str = get_input(input_file)[0]
    part_two(input_as_str)
