from collections.abc import Callable, Generator

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 2
YEAR = 2025

PART_ONE_DESCRIPTION = "sum of invalid IDs"
PART_ONE_ANSWER = 28846518423

PART_TWO_DESCRIPTION = "sum of invalid IDs based on correct rule"
PART_TWO_ANSWER = 31578210022


def _parse_pairs(raw_input: list[str]) -> Generator[tuple[int, int]]:
    """Parse pairs of integers from the problem input."""

    for line in raw_input[0].split(","):
        h1, h2 = (int(n) for n in line.split("-"))
        yield (h1, h2)


def _is_invalid(n: int) -> bool:
    """Return if a number is invalid.

    Invalid numbers consist of any set of digits that repeats exactly twice.
    """

    digits = str(n)

    # The number can't be invalid if it's not an even number
    # of digits long.
    if len(digits) % 2 != 0:
        return False

    # The number is invalid if the first half of the digits
    # is repeated exactly in the second half.
    half_ix = len(digits) // 2
    return digits[:half_ix] == digits[half_ix:]


def _is_invalid_v2(n: int) -> bool:
    """Return if a number is invalid, based on the correct.

    Invalid numbers consist of any set of digits that repeats any number of times.
    """

    digits = str(n)

    # If the number consists of just 1 distinct digit, it's invalid
    # (as long as the number is more than just 1 digit long).
    if len(digits) != 1 and len(set(digits)) == 1:
        return True

    # For each possible size of repeating digit patterns, break off chunks
    # of digits of that size from the original number and ensure there's only
    # 1 pattern represented.
    #
    # Ex: 123123123, size=3:
    # breaks into 123, 123, 123 so it's invalid.
    #
    # Ex: 12345555, size=5:
    # breaks into 1234, 5555 so it's not repeating. It's valid.
    for size in range(2, len(digits) // 2 + 1):
        if len(digits) % size != 0:
            continue

        patterns = set()
        digits_copy = list(digits)

        while digits_copy:
            patterns.add(tuple(digits_copy[:size]))
            digits_copy = digits_copy[size:]

        if len(patterns) == 1:
            return True

    return False


def _sum_invalid_ids(raw_input: list[str], invalid_checker: Callable[[int], bool]) -> int:
    """Return the sum of all invalid IDs in the ranges specified in the problem input.

    Determines validity using the "invalid_checker" function provided which accepts
    an integer and returns True if that integer is invalid.
    """

    return sum(
        candidate_id
        for lower_bound, upper_bound in _parse_pairs(raw_input)
        for candidate_id in range(lower_bound, upper_bound + 1)
        if invalid_checker(candidate_id)
    )


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return _sum_invalid_ids(raw_input, _is_invalid)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    return _sum_invalid_ids(raw_input, _is_invalid_v2)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
