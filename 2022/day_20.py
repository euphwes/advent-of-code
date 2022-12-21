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


def _get_grove_coords_sum(numbers):
    """Returns the sum of the coordinates of the grove; the 1000th, 2000th, and 3000th numbers
    which follow the value 0 in the list of numbers."""

    i = numbers.index(0)
    size = len(numbers)

    return (
        numbers[(i + 1000) % size]
        + numbers[(i + 2000) % size]
        + numbers[(i + 3000) % size]
    )


def _translate_numbers(numbers):
    """The mixing process requires us to move numbers around in a list, but when that list
    contains duplicate numbers, we need to be able to uniquely identify them. This process
    assigns a "mini uuid" to each of the distinct numbers in the list. Then it returns the
    "translated" list of mini uuids, an unaltered copy of the original numbers so we can figure
    out which uuid corresponds to which unique number, and a mapping of index (of the original
    unaltered list) to the new uuid, and the reverse mapping for conversion back later.

    Ex;
    [1, 1, 2, 1, 3] becomes ['A', 'B', 'C', 'D', 'E']
    and
    ix_to_uuid: {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
    }

    This allows us to shuffle [1, 1, 2, 1, 3] around in that order by finding the uuid which
    represents the unique number at the specified index in the original ordered numbers."""

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
    """Returns the (now-shuffled) list of numbers by mapping the UUIDs back to the numbers they
    represent."""

    return [original_ordered_values[uuid_to_original_ix[uuid]] for uuid in numbers]


def _run_switcheroo(numbers, iterations=1, is_part_two=False):
    """Shuffle the provided set of numbers using the rules described in 2022 Day 20."""

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

            # Retrieve the original number at this index, and the uuid used to represent it.
            og_value = og_ordered_numbers[og_value_ix]
            uuid_value = ix_to_uuid[og_value_ix]

            # If the value is negative, the element is moving left.
            is_moving_left = og_value < 0

            # For a circular list of size N, N-1 swaps in any direction gives the same list.
            # Take original value (which specifies the number of swaps) mod (size of list - 1)
            # to get the smallest possible number of swaps that would yield the same list.
            og_value = og_value % (size - 1)
            if is_moving_left:
                while og_value >= 0:
                    og_value -= size - 1

            if og_value == 0:
                continue

            # Find the index of the element that's moving.
            i = translated.index(uuid_value)

            # And swap left or right (depending on sign of the og value), `og_value` times.
            for n in range(abs(og_value)):
                if is_moving_left:
                    a, b = translated[i % size], translated[(i - 1) % size]
                    translated[i % size], translated[(i - 1) % size] = b, a
                    i = (i - 1) % size

                else:
                    a, b = translated[i % size], translated[(i + 1) % size]
                    translated[i % size], translated[(i + 1) % size] = b, a
                    i = (i + 1) % size

    # Translate back to numbers and return.
    return _translate_uuids(translated, og_ordered_numbers, uuid_to_ix)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(numbers):

    numbers = _run_switcheroo(numbers, iterations=1, is_part_two=False)
    return _get_grove_coords_sum(numbers)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(numbers):

    numbers = _run_switcheroo(numbers, iterations=10, is_part_two=True)
    return _get_grove_coords_sum(numbers)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    numbers = [int(n) for n in get_input(input_file)]
    part_one(numbers)

    numbers = [int(n) for n in get_input(input_file)]
    part_two(numbers)
