from copy import copy
from os import remove
from uuid import uuid4

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 20
YEAR = 2022

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _small_uuid():
    return str(uuid4())[:8]


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    size = len(stuff)
    og_stuff = list(copy(stuff))

    og_ix_to_uuid = {i: _small_uuid() for i, _ in enumerate(og_stuff)}
    uuid_to_og_ix = {v: k for k, v in og_ix_to_uuid.items()}

    stuff = [og_ix_to_uuid[i] for i in range(len(stuff))]

    for og_value_ix in range(len(stuff)):

        og_value = og_stuff[og_value_ix]
        if og_value == 0:
            continue

        uuid_value = og_ix_to_uuid[og_value_ix]

        is_moving_left = og_value < 0
        is_moving_right = not is_moving_left

        i = stuff.index(uuid_value)
        for n in range(abs(og_value)):
            if is_moving_left:
                a, b = stuff[i % size], stuff[(i - 1) % size]
                stuff[i % size], stuff[(i - 1) % size] = b, a
                i = (i - 1) % size

            else:
                a, b = stuff[i % size], stuff[(i + 1) % size]
                stuff[i % size], stuff[(i + 1) % size] = b, a
                i = (i + 1) % size

        # print(f"\nmoved {og_value}\n")
        # print(stuff)

    stuff = [og_stuff[uuid_to_og_ix[uuid]] for uuid in stuff]
    i = stuff.index(0)

    # ? 14165 wrong swaps
    # not 13972, 15077, -5345, -11007, 23161, 473
    # print(stuff)
    return (
        stuff[(i + 1000) % size] + stuff[(i + 2000) % size] + stuff[(i + 3000) % size]
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    print(len(stuff))
    stuff = [n * 811589153 for n in stuff]
    print(len(stuff))

    size = len(stuff)
    og_stuff = list(copy(stuff))
    print(len(og_stuff))

    og_ix_to_uuid = {i: _small_uuid() for i, _ in enumerate(og_stuff)}
    uuid_to_og_ix = {v: k for k, v in og_ix_to_uuid.items()}
    print(len(og_ix_to_uuid.items()))
    print(len(uuid_to_og_ix.items()))

    stuff = [og_ix_to_uuid[i] for i in range(len(stuff))]
    print(len(stuff))

    for _ in range(10):
        for og_value_ix in range(len(stuff)):

            og_value = og_stuff[og_value_ix]
            if og_value == 0:
                continue

            uuid_value = og_ix_to_uuid[og_value_ix]

            is_moving_left = og_value < 0
            is_moving_right = not is_moving_left

            i = stuff.index(uuid_value)
            for n in range(abs(og_value)):
                if is_moving_left:
                    a, b = stuff[i % size], stuff[(i - 1) % size]
                    stuff[i % size], stuff[(i - 1) % size] = b, a
                    i = (i - 1) % size

                else:
                    a, b = stuff[i % size], stuff[(i + 1) % size]
                    stuff[i % size], stuff[(i + 1) % size] = b, a
                    i = (i + 1) % size

    stuff = [og_stuff[uuid_to_og_ix[uuid]] for uuid in stuff]
    i = stuff.index(0)

    # ? 14165 wrong swaps
    # not 13972, 15077, -5345, -11007, 23161, 473
    # print(stuff)
    return (
        stuff[(i + 1000) % size] + stuff[(i + 2000) % size] + stuff[(i + 3000) % size]
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = [int(n) for n in get_input(input_file)]
    part_one(stuff)

    # stuff = [int(n) for n in get_input(input_file)]
    # part_two(stuff)
