from itertools import combinations

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 5
YEAR = 2025

PART_ONE_DESCRIPTION = "number of available fresh ingredients"
PART_ONE_ANSWER = 613

PART_TWO_DESCRIPTION = "total of fresh ingredients according to database"
PART_TWO_ANSWER = 336495597913098


Range = tuple[int, int]


def _parse_ranges(raw_input: list[str]) -> list[Range]:
    empty_ix = raw_input.index("")

    ranges = []
    for line in raw_input[:empty_ix]:
        a, b = line.split("-")
        ranges.append((int(a), int(b)))
    return ranges


def _parse_ingredients(raw_input: list[str]) -> list[int]:
    empty_ix = raw_input.index("")
    return [int(line) for line in raw_input[empty_ix + 1 :]]


def _merge_ranges(range1: Range, range2: Range) -> Range | None:
    """Merge and return two ranges if they overlap, otherwise return None."""

    start1, end1 = range1
    start2, end2 = range2

    if end1 < start2 or end2 < start1:
        return None

    return (min([start1, start2]), max([end1, end2]))


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    ranges = _parse_ranges(raw_input)
    ingredients = _parse_ingredients(raw_input)

    return len(
        [
            ingredient
            for ingredient in ingredients
            if any(start <= ingredient <= end for start, end in ranges)
        ],
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    ranges = _parse_ranges(raw_input)

    new_range: Range | None = None
    to_remove: list[Range] = []

    while True:
        # For every combo of ranges in the list, see if they can be
        # merged because they overlap.
        for range1, range2 in combinations(ranges, 2):
            # If this combo can be merged, remember the new range as well
            # as the original ones which constituted the combined range.
            if combined_range := _merge_ranges(range1, range2):
                new_range = combined_range
                to_remove = [range1, range2]
                break

        if new_range:
            # If we merged two ranges, recreate the list of ranges
            # with the new combined one, omitting the two source ones,
            # and including everything else.
            ranges = [
                new_range,
                *[r for r in ranges if r not in to_remove],
            ]
            to_remove = []
            new_range = None
        else:
            # If we didn't find any ranges to merge, we're done.
            break

    return sum(
        end - start + 1  # the size of the range (inclusive)
        for start, end in ranges
    )


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
