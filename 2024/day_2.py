from itertools import pairwise

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 2
YEAR = 2024

PART_ONE_DESCRIPTION = "number of safe levels"
PART_ONE_ANSWER = 334

PART_TWO_DESCRIPTION = "number of truly safe levels"
PART_TWO_ANSWER = 400


def is_safe(report: list[int]) -> bool:
    """Determine if a report is safe.

    "Safe" is when the levels in a report are:
        * all decreasng, or all increasing
        * two adjacent levels differ by at least 1 and at most 3
    """

    diffs = []
    for n1, n2 in pairwise(report):
        diffs.append(n1 - n2)
        diff = abs(n1 - n2)
        if not (diff >= 1 and diff <= 3):
            return False

    return all(x > 0 for x in diffs) or all(x < 0 for x in diffs)


def is_truly_safe(report: list[int]) -> bool:
    """Determine if a report is safe.

    "Safe" is when a report is safe as determined by is_safe above, or if the removal of any
    single level in the report leads to that level being safe.
    """

    if is_safe(report):
        return True

    for i in range(len(report)):
        test = report[:i] + report[i + 1 :]
        if is_safe(test):
            return True

    return False


def _parse_reports(raw_input: list[str]) -> list[list[int]]:
    """Parse the raw input into a list of "reports", where each report is a list of integers."""

    return [[int(x) for x in line.split()] for line in raw_input]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return sum(1 for report in _parse_reports(raw_input) if is_safe(report))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    return sum(1 for report in _parse_reports(raw_input) if is_truly_safe(report))


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
