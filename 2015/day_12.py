from json import loads

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 12
YEAR = 2015

PART_ONE_DESCRIPTION = "Accounting doc sum"
PART_ONE_ANSWER = 119433

PART_TWO_DESCRIPTION = "Accounting doc sum, ignoring red objects"
PART_TWO_ANSWER = 68466


document_component = dict | str | int | list


def _evaluate_document_sum(
    document: document_component,
    *,
    ignore_red: bool = False,
) -> int:
    """Parse a JSON document and returns the sum of all numerical values in it."""

    # A string is always zero-valued.
    if isinstance(document, str):
        return 0

    # Just return the integer itself, if it's an integer.
    if isinstance(document, int):
        return document

    # If we're inspecting an object, sum all of its values.
    if isinstance(document, dict):
        if ignore_red and "red" in document.values():
            return 0
        return sum(
            _evaluate_document_sum(item, ignore_red=ignore_red) for item in document.values()
        )

    # If we're inspecting a list, sum of all its values.
    if isinstance(document, list):
        return sum(_evaluate_document_sum(item, ignore_red=ignore_red) for item in document)

    return 0


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    document = loads(raw_input[0])
    return _evaluate_document_sum(document, ignore_red=False)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    document = loads(raw_input[0])
    return _evaluate_document_sum(document, ignore_red=True)


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
