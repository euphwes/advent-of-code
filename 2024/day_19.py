from functools import cache

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 19
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _parse_towel_patterns(raw_input: list[str]) -> frozenset[str]:
    empty_line_ix = raw_input.index("")
    towel_patterns = set()
    for line in raw_input[:empty_line_ix]:
        towel_patterns.update([pat.strip() for pat in line.split(",")])
    return frozenset(towel_patterns)


def _parse_designs(raw_input: list[str]) -> frozenset[str]:
    empty_line_ix = raw_input.index("")
    return frozenset(raw_input[empty_line_ix + 1 :])


@cache
def _is_valid_design(design: str, towel_patterns: frozenset[str]) -> bool:
    if design in towel_patterns:
        return True

    for i in range(1, len(design)):
        if _is_valid_design(design[:i], towel_patterns) and _is_valid_design(
            design[i:],
            towel_patterns,
        ):
            return True

    return False


@cache
def _ways_to_make_design(
    design: str,
    towel_patterns: frozenset[str],
) -> int:
    # print(f'ways_to_make_design("{design}")')
    if not _is_valid_design(design, towel_patterns):
        return 0

    combos = 0
    if design in towel_patterns:
        combos += 1

    for i in range(1, len(design)):
        left = design[:i]
        right = design[i:]

        if left not in towel_patterns:
            continue

        combos += _ways_to_make_design(right, towel_patterns)

    return combos


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    towel_patterns = _parse_towel_patterns(raw_input)
    designs = _parse_designs(raw_input)
    return sum(1 for design in designs if _is_valid_design(design, towel_patterns))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    towel_patterns = _parse_towel_patterns(raw_input)
    designs = _parse_designs(raw_input)

    return sum(_ways_to_make_design(design, towel_patterns) for design in designs)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
