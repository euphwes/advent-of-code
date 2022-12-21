from copy import copy
from uuid import uuid4

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 20
YEAR = 2022

PART_ONE_DESCRIPTION = "Sum of the coordinates of the grove"
PART_ONE_ANSWER = 1591

PART_TWO_DESCRIPTION = "Correct sum of the coordinates of the grove"
PART_TWO_ANSWER = 14579387544492


def _mini_uuid():
    return str(uuid4())[:8]


def _translate_numbers(numbers):
    original_ordered_numbers = copy(numbers)

    ix_to_uuid = {i: _mini_uuid() for i, _ in enumerate(numbers)}
    uuid_to_ix = {v: k for k, v in ix_to_uuid.items()}

    return (
        [ix_to_uuid[i] for i in range(len(numbers))],
        ix_to_uuid,
        uuid_to_ix,
        original_ordered_numbers,
    )


def _translate_uuids(numbers, original_ordered_values, uuid_to_original_ix):
    return [original_ordered_values[uuid_to_original_ix[uuid]] for uuid in numbers]


def _run_switcheroo(numbers, iterations=1, is_part_two=False):
    if is_part_two:
        numbers = [n * 811589153 for n in numbers]
    (
        translated,
        ix_to_uuid,
        uuid_to_ix,
        og_ordered_numbers,
    ) = _translate_numbers(numbers)

    size = len(translated)

    for _ in range(iterations):
        for og_value_ix in range(len(translated)):

            og_value = og_ordered_numbers[og_value_ix]
            if og_value == 0:
                continue

            uuid_value = ix_to_uuid[og_value_ix]

            is_moving_left = og_value < 0

            og_value = og_value % (size - 1)
            if is_moving_left:
                while og_value >= 0:
                    og_value -= size - 1

            i = translated.index(uuid_value)
            for n in range(abs(og_value)):
                if is_moving_left:
                    a, b = translated[i % size], translated[(i - 1) % size]
                    translated[i % size], translated[(i - 1) % size] = b, a
                    i = (i - 1) % size

                else:
                    a, b = translated[i % size], translated[(i + 1) % size]
                    translated[i % size], translated[(i + 1) % size] = b, a
                    i = (i + 1) % size

    return _translate_uuids(translated, og_ordered_numbers, uuid_to_ix)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(numbers):

    numbers = _run_switcheroo(numbers, iterations=1, is_part_two=False)
    i = numbers.index(0)

    return (
        numbers[(i + 1000) % len(numbers)]
        + numbers[(i + 2000) % len(numbers)]
        + numbers[(i + 3000) % len(numbers)]
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(numbers):

    numbers = _run_switcheroo(numbers, iterations=10, is_part_two=True)
    i = numbers.index(0)

    return (
        numbers[(i + 1000) % len(numbers)]
        + numbers[(i + 2000) % len(numbers)]
        + numbers[(i + 3000) % len(numbers)]
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = [int(n) for n in get_input(input_file)]
    part_one(stuff)

    stuff = [int(n) for n in get_input(input_file)]
    part_two(stuff)
