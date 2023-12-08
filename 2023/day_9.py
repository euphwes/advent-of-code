from util.decorators import aoc_output_formatter
from util.input import get_input

from itertools import pairwise

DAY = 9
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of next value in each sequence"
PART_ONE_ANSWER = 1938800261

PART_TWO_DESCRIPTION = "sum of prior value in each sequence"
PART_TWO_ANSWER = 1112


def _extrapolate(sequence):
    """Extrapolates the next integer in a given integer sequence."""

    # Maintain a history of sequences, each one is a list of the differences between consecutive
    # pairs in the sequence before. Keep going until the latest is a list of constant values.
    sequences = [sequence]
    while len(set(sequence)) > 1:
        sequence = [b - a for a, b in pairwise(sequence)]
        sequences.append(sequence)

    # The next value in the original sequence is the sum of the last numbers in each of the
    # derived (pairwise diff) sequences and the last value in the original.
    return sum(sequence[-1] for sequence in sequences)


def _get_int_sequences(raw_sequences):
    """Extract a sequence of integers from each line of the puzzle input, and return a list of
    lists containing those sequences."""

    return [[int(x) for x in line.split()] for line in raw_sequences]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_sequences):
    sequences = _get_int_sequences(raw_sequences)
    return sum(_extrapolate(sequence) for sequence in sequences)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_sequences):
    sequences = [sequence[::-1] for sequence in _get_int_sequences(raw_sequences)]
    return sum(_extrapolate(sequence) for sequence in sequences)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    raw_sequences = get_input(input_file)
    part_one(raw_sequences)
    part_two(raw_sequences)
