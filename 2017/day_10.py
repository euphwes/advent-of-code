from util.decorators import aoc_output_formatter
from util.input import get_input, get_tokenized_input

from functools import reduce

#---------------------------------------------------------------------------------------------------

def _rotate(sequence, steps):
    """ Rotates a sequence by N steps, wrapping elements back to the beginning. """

    steps = steps % len(sequence)
    return sequence[-steps:] + sequence[:-steps]


def _knot_hash(bytes_to_hash, iterations=1):
    """ Performs `iterations` of Knot Hash on the provided input bytes and returns the result. """

    skip_size = 0
    current_pos = 0
    hashed = list(range(0, 256))

    for _ in range(iterations):
        for byte_value in bytes_to_hash:
            # Rather than attempting to reverse a chunk of the hashed values in a circular list
            # manner, rotate the hashed bytes by `current_pos` so we're always reversing the
            # chunk at the beginning, and then rotate the hashed values back.
            hashed = _rotate(hashed, -1 * current_pos)
            hashed = list(reversed(hashed[:byte_value])) + hashed[byte_value:]
            hashed = _rotate(hashed, current_pos)

            current_pos += (byte_value + skip_size) % 256
            skip_size += 1

    return hashed


def _build_dense_hash(sparse_hash):
    """ Returns a dense hash from a given sparse hash.

    The sparse hash is always 256 bytes long. Each byte of the dense hash is calculated by
    performing bitwise XOR operations on the 16-byte chunks of the sparse hash.

    The final result is represented as a hexadecimal string. """

    _xor = lambda x, y: x ^ y
    _hex = lambda byte: hex(byte)[2:].zfill(2)

    dense_hash = list()
    for _ in range(16):
        dense_hash.append(reduce(_xor, sparse_hash[:16]))
        sparse_hash = sparse_hash[16:]

    return ''.join(map(_hex, dense_hash))


@aoc_output_formatter(2017, 10, 1, 'product of first 2 bytes of 1-iteration knot hash on input')
def part_one(input_integers):
    hashed = _knot_hash(input_integers, iterations=1)
    return hashed[0] * hashed[1]


@aoc_output_formatter(2017, 10, 2, 'hex representation of 64-iteration knot hash on input')
def part_two(input_str):
    input_bytes = [ord(c) for c in input_str] + [17, 31, 73, 47, 23]
    sparse_hash = _knot_hash(input_bytes, iterations=64)

    return _build_dense_hash(sparse_hash)

#---------------------------------------------------------------------------------------------------

def run(input_file):

    input_as_ints = get_tokenized_input(input_file, ',', int)[0]
    part_one(input_as_ints)

    input_as_str = get_input(input_file)[0]
    part_two(input_as_str)
