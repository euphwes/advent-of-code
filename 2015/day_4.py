from hashlib import md5

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import int_stream

DAY = 4
YEAR = 2015

PART_ONE_DESCRIPTION = "lowest n which produces a hash with 5 leading zeroes"
PART_ONE_ANSWER = 346386

PART_TWO_DESCRIPTION = "lowest n which produces a hash with 6 leading zeroes"
PART_TWO_ANSWER = 9958218


def _brute_force_n(key: str, target: str) -> int:
    """Return "n" for the given key and target value.

    N is the lowest value integer for which the md5 hash of `secret_key{n}` starts with the
    target value.
    """

    def _md5_startswith_target(candidate_n: int) -> bool:
        salted_key = f"{key}{candidate_n}"
        return md5(salted_key.encode()).hexdigest().startswith(target)

    n = -1
    for candidate_n in int_stream():
        if _md5_startswith_target(candidate_n):
            n = candidate_n
            break

    return n


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    key = raw_input[0]
    return _brute_force_n(key, "00000")


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    key = raw_input[0]
    return _brute_force_n(key, "000000")


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
