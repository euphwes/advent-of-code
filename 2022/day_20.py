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


def _decrypt_uuids(stuff, og_stuff, uuid_to_og_ix):
    return [og_stuff[uuid_to_og_ix[uuid]] for uuid in stuff]


def _run_switcheroos_v3(stuff):

    size = len(stuff)

    # raw values copy from stuff
    og_stuff = copy(stuff)

    og_ix_to_uuid = {i: _small_uuid() for i, _ in enumerate(stuff)}
    uuid_to_og_ix = {v: k for k, v in og_ix_to_uuid.items()}

    stuff = [og_ix_to_uuid[i] for i in range(len(stuff))]

    # print(stuff)
    for og_ix in range(size):
        value = og_stuff[og_ix]

        if value == 0:
            continue

        uuid_value = og_ix_to_uuid[og_ix]

        i = stuff.index(uuid_value)
        target = (i + value) % size

        if target > i:
            """
            1 -3 -2 5 -6 0
            move -3
            should become
            1 -2 5 -3 -6 0

            i = 1
            target = (1 - 3) % 6 = 4

            1 [-3 -2 5] -6 0
            [1] + (pop(0) and append) + [-6, 0]
            [1] + [-2 5 -3] + [-6 0]
            1 -2 5 -3 6 0
            """
            before = stuff[:i]
            after = stuff[target + 1 :]
            sublist = stuff[i : target + 1]
            temp = sublist.pop(0)
            sublist.append(temp)
            stuff = before + sublist + after

        else:
            """
            1 2 -2 5 -3 0
            move -3
            should become
            1 -3 2 -2 5 0

            i = 4
            target = 4 -3 = 1

            1 [2 -2 5 -3] 0
            [1] + (pop from end and prepend)   + [0]
            [1] + [-3 2 -2 5] + [0]
            1 -3 2 -2 5 0
            """
            before = stuff[:target]
            after = stuff[i + 1 :]
            sublist = stuff[target : i + 1]
            temp = sublist.pop(-1)
            sublist = [temp] + sublist
            stuff = before + sublist + after

        # print(f"\nSwapping the og value {value} at {og_ix=}, {i=}, {target=}")

        # print(stuff)
        # print(_decrypt_uuids(stuff, og_stuff, uuid_to_og_ix))

    # print(stuff)
    return stuff, uuid_to_og_ix


def _run_switcheroos_v2(stuff):

    size = len(stuff)

    # raw values copy from stuff
    og_stuff = copy(stuff)

    og_ix_to_uuid = {i: _small_uuid() for i, _ in enumerate(stuff)}
    uuid_to_og_ix = {v: k for k, v in og_ix_to_uuid.items()}

    stuff = [og_ix_to_uuid[i] for i in range(len(stuff))]

    # print(stuff)
    for og_ix in range(size):
        value = og_stuff[og_ix]

        if value == 0:
            continue

        uuid_value = og_ix_to_uuid[og_ix]

        i = stuff.index(uuid_value)
        target = (i + value) % size

        # print(f"\nSwapping the og value {value} at {og_ix=}, {i=}, {target=}")

        if target == 0:
            temp = stuff.pop(i)
            stuff = [temp] + stuff
        elif target == size - 1:
            temp = stuff.pop(i)
            stuff.append(temp)
        else:

            if target > i:
                # print("\ndoing greater than than")
                # print("before")
                # print(stuff)
                """
                1 -3 -2 5 -6 0
                move -3
                should become
                1 -2 5 -3 -6 0

                i = 1
                target = (1 - 3) % 6 = 4
                target -=1 (because we pop the value) --> target = 3

                1 -2 5 -6 0   (popped value)

                [1, -2, 5] + [-3] + [6, 0]

                """

                temp = stuff.pop(i)
                target -= 1
                if value < 0:
                    target -= 1
                # if value > 0:
                #     target += 1
                stuff = (
                    stuff[: (target + 1) % size] + [temp] + stuff[(target + 1) % size :]
                )
                # print("after")
                # print(stuff)
            else:
                # print()
                # print("\ndoing smaller than than")
                # print("before")
                # print(stuff)
                """
                1 2 -2 5 -6 0
                move 2
                should become
                1 -2 5 2 -6 0

                i = 1
                target = (1 + 2) % 6 = 3

                1 -2 5 -6 0  (popped value)
                don't need to change target

                [1 -2 5] + [2] + [-6 0]

                """
                temp = stuff.pop(i)
                if value > 0:
                    target += 1
                # if value < 0:
                #     target -= 1
                stuff = stuff[: (target) % size] + [temp] + stuff[(target) % size :]
                # print("after")
                # print(stuff)
        # print(stuff)
        # print(_decrypt_uuids(stuff, og_stuff, uuid_to_og_ix))

    # print(stuff)
    return stuff, uuid_to_og_ix


def _run_switcheroos(stuff):
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

        i = stuff.index(uuid_value)
        for n in range(abs(og_value)):
            if is_moving_left:
                # i = stuff.index(uuid_value)
                a, b = stuff[i % size], stuff[(i - 1) % size]
                stuff[i % size], stuff[(i - 1) % size] = b, a
                i = (i - 1) % size

            else:
                # i = stuff.index(uuid_value)
                a, b = stuff[i % size], stuff[(i + 1) % size]
                stuff[i % size], stuff[(i + 1) % size] = b, a
                i = (i + 1) % size

    return stuff, uuid_to_og_ix


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    size = len(stuff)
    og_stuff = copy(stuff)

    stuff, uuid_to_og_ix = _run_switcheroos_v3(stuff)

    stuff = [og_stuff[uuid_to_og_ix[uuid]] for uuid in stuff]
    # print(stuff)
    i = stuff.index(0)

    return (
        stuff[(i + 1000) % size] + stuff[(i + 2000) % size] + stuff[(i + 3000) % size]
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    size = len(stuff)
    og_stuff = copy(stuff)

    decrypted_stuff = [n * 811589153 for n in stuff]

    for _ in range(10):
        decrypted_stuff, uuid_to_og_ix = _run_switcheroos(decrypted_stuff)

    decrypted_stuff = [og_stuff[uuid_to_og_ix[uuid]] for uuid in decrypted_stuff]
    i = decrypted_stuff.index(0)

    # not 5377589727778
    return (
        decrypted_stuff[(i + 1000) % size]
        + decrypted_stuff[(i + 2000) % size]
        + decrypted_stuff[(i + 3000) % size]
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = [int(n) for n in get_input(input_file)]
    part_one(stuff)

    # stuff = [int(n) for n in get_input(input_file)]
    # part_two(stuff)
