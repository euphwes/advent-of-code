from math import prod

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 6
YEAR = 2025

PART_ONE_DESCRIPTION = "sum of problem answers"
PART_ONE_ANSWER = 4693419406682

PART_TWO_DESCRIPTION = "sum of problem answers using cephalapod math"
PART_TWO_ANSWER = 9029931401920


def _parse_columns(raw_input: list[str]) -> list[tuple[str, list[int]]]:
    # Prepopulate a list of lists, where each inner list represents a column
    # in the problem input.
    columns: list[list[int]] = [[] for _ in range(len(raw_input[0].split()))]

    # Each line except the final one contains an integer.
    # Iterate 1 integer at a time within each line, and add it to the correct column.
    for line in raw_input[:-1]:
        for i, val in enumerate(line.split()):
            columns[i].append(int(val))

    return [
        (operator, columns[i])
        # The final line is a sequence of operators (either * or +).
        for i, operator in enumerate(raw_input[-1].split())
    ]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(raw_input: list[str]) -> int | str | None:
    return sum(
        sum(column_values) if operator == "+" else prod(column_values)
        for operator, column_values in _parse_columns(raw_input)
    )


def _parse_columns_v2(raw_input: list[str]) -> list[tuple[str, list[int]]]:
    # Prepopulate a list of lists, where each inner list represents a column
    # in the problem input.
    columns: list[list[int]] = [[] for _ in range(len(raw_input[0].split()))]

    # Hold which column we're currently parsing.
    col_ix = 0

    # Each line of the input is exactly the same length.
    for i in range(len(raw_input[0])):
        # If this column of single characters in the input is entirely comprised
        # of spaces, it's the divider in between logical columns of numbers.
        # The next set of characters will belong to the next logical column.
        if all(line[i] == " " for line in raw_input[:-1]):
            col_ix += 1
            continue

        # The number (in cephalapod) is read from top to bottom.
        # Iterate over every character at this index in every line,
        # building up a list of digits, and then convert to an int.
        number = int("".join([line[i] for line in raw_input[:-1]]))

        # Add that number to the values that appear in this column.
        columns[col_ix].append(number)

    return [
        (operator, columns[i])
        # The final line is a sequence of operators (either * or +).
        for i, operator in enumerate(raw_input[-1].split())
    ]


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(raw_input: list[str]) -> int | str | None:
    return sum(
        sum(column_values) if operator == "+" else prod(column_values)
        for operator, column_values in _parse_columns_v2(raw_input)
    )


def run(input_file: str) -> None:
    part_one(get_input(input_file))
    part_two(get_input(input_file))
