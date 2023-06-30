from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 16
YEAR = 2016

PART_ONE_DESCRIPTION = "checksum for small disk"
PART_ONE_ANSWER = "10100011010101011"

PART_TWO_DESCRIPTION = "checksum for big disk"
PART_TWO_ANSWER = "01010001101011001"


def _build_data_to_length(data, min_length):
    """Using the scheme described in the problem description, continuing building up the data until
    the data reaches the minimum length. Return the data."""

    swap = lambda d: "0" if d == "1" else "1"

    while len(data) < min_length:
        reverse_copy = reversed(data)
        swapped = "".join([swap(d) for d in reverse_copy])
        data = data + "0" + swapped

    return data[:min_length]


def _checksum(data):
    """Return the checksum for the provided data."""

    checksum = []
    for n in range(0, len(data), 2):
        test = data[n : n + 2]
        checksum.append("1" if test in {"00", "11"} else "0")

    checksum = "".join(checksum)
    return _checksum(checksum) if len(checksum) % 2 == 0 else checksum


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(data, min_length):
    return _checksum(_build_data_to_length(data, min_length))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(data, min_length):
    return _checksum(_build_data_to_length(data, min_length))


# ----------------------------------------------------------------------------------------------


def run(input_file):
    data = get_input(input_file)[0]

    part_one(data[:], 272)
    part_two(data[:], 35651584)
