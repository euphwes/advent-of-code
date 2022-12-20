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


def _run_switcheroos_v2(stuff):

    size = len(stuff)

    og_stuff = copy(stuff)

    og_ix_to_uuid = {i: _small_uuid() for i, _ in enumerate(stuff)}
    uuid_to_og_ix = {v: k for k, v in og_ix_to_uuid.items()}

    stuff = [og_ix_to_uuid[i] for i in range(len(stuff))]

    print("\nInitial")
    print(_decrypt_uuids(stuff, og_stuff, uuid_to_og_ix))
    for og_ix in range(size):
        value = og_stuff[og_ix]
        uuid_value = og_ix_to_uuid[og_ix]

        i = stuff.index(uuid_value)
        target = (i + value) % size

        """
        1, 2, 3, 4, 5
        move 4
        should give
        1, 2, 3, 4, 5
        
        i = 3
        target = (3 + 4) % 5 = 2
        """
        if value == 0:
            pass

        elif value > 0 and target == (i - 1):
            pass

        # """
        # -1, -2, -3
        # move -2
        # should give
        # -1, -2, -3

        # i = 1
        # target = (1 - 2) % 3 = 2
        # """

        elif value < 0 and target == (i + 1):
            pass

        # """
        # 1 3 5 7 9
        # move 5
        # should give
        # 1 3 7 5 9
        # """

        elif target == i:
            if value > 0:
                a, b = stuff[(i + 1) % size], stuff[i]
                stuff[i], stuff[(i + 1) % size] = a, b
            else:
                a, b = stuff[(i - 1) % size], stuff[i]
                stuff[i], stuff[(i - 1) % size] = a, b

        ##### Example cases, positive value #####

        # """
        # 1, 2, 3, 4, 5, 6
        # move 2
        # should give
        # 1, 3, 4, 2, 5, 6

        # (finds value at ix + value, ends up to the right of it)
        # """

        # """
        # 1, 2, 3, 4, 5, 6
        # move 3
        # should give
        # 1, 2, 4, 5, 6, 3 or equivalently 3, 1, 2, 4, 5, 6

        # (finds value at ix + value, ends up to the right of it)
        # """

        # """
        # 1, 2, 3, 4, 5, 6
        # move 1
        # should give
        # 2, 1, 3, 4, 5, 6

        # (finds value at ix + value, ends up to the right of it)
        # """

        # """
        # 5, 4, 3, 2, 1
        # move 2
        # should give
        # 5, 2, 4, 3, 1

        # (finds value at ix + value, ends up to the right of it)
        # """

        elif value > 0:
            # print(f"{i=}")
            # print(f"{target=}")
            value_at_target = stuff[target]
            temp = stuff.pop(i)
            new_target = stuff.index(value_at_target)
            stuff = stuff[: new_target + 1] + [temp] + stuff[new_target + 1 :]

        ##### Example cases, negative value #####

        # """
        # 1, -2, 3, 4, 5, 6
        # move -2
        # should give
        # 1, 3, 4, 5, -2, 6

        # (finds value at ix - value, ends up to the left of it)
        # """

        elif value < 0:
            value_at_target = stuff[target]
            temp = stuff.pop(i)
            new_target = stuff.index(value_at_target)
            stuff = stuff[:new_target] + [temp] + stuff[new_target:]

        print(f"\nSwapping the og value {value} at {og_ix=}, {i=}, {target=}")
        print(_decrypt_uuids(stuff, og_stuff, uuid_to_og_ix))

    return _decrypt_uuids(stuff, og_stuff, uuid_to_og_ix)


def _run_switcheroos(stuff):

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

        # if abs(target - i) == 1:
        #     # CASE the things are adjacent
        #     # swippity swap
        #     stuff[target], stuff[i] = stuff[i], stuff[target]

        # if target == i:
        #     # Went all the way around the circle
        #     pass

        if value > 0 and target == (i - 1):
            """
            1, 2, 3, 4, 5
            move 4
            gives
            1, 2, 3, 4, 5
            """
            pass

        elif value < 0 and target == (i + 1):
            """
            -1, -2, -3
            move -2
            gives
            -1, -2, -3
            """
            pass

        elif target > i:
            # CASE target ix is higher than starting ix

            if True:
                """
                1 2 3 4 5 6
                move 2
                should give
                """

            if value < 0:
                # SUB-CASE value is moving left and wraps around
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
                after = stuff[target:]

                middle = stuff[i:target]
                temp = middle.pop(0)
                middle.append(temp)

                stuff = before + middle + after

            elif value > 0:
                # SUB-CASE value is moving right
                """
                1 2 -2 5 -6 0
                move 2
                should become
                1 -2 5 2 -6 0

                i = 1
                target = (1 + 2) % 6 = 3

                [1] [2, -2, 5] [-6 0]
                * INCLUDE TARGET *
                [1] + (pop(0) and append) + [-6 0]
                [1] + [-2, 5, 2] + [-6 0]
                1, -2, 5, 2, -6, 0
                """

                before = stuff[:i]
                after = stuff[target + 1 :]

                middle = stuff[i : target + 1]
                temp = middle.pop(0)
                middle.append(temp)

                stuff = before + middle + after

        else:
            # CASE target ix is lower than starting ix

            if value < 0:
                # SUB-CASE value is moving left
                """
                1 -3 -2 5 -6 0
                move -2
                should become
                -2 1 -3 5 -6 0

                i = 2
                target = (2 - 2) % 6 = 0
                [] [1 -3 -2] [5 -6 0]
                [] (pop last and prepend) [5 -6 0]
                [] + [-2 1 -3] [5 -6 0]
                -2 1 -3 5 -6 0

                RANGE IS FROM TARGET TO I, include I
                """

                before = stuff[:target]
                after = stuff[i + 1 :]

                middle = stuff[target : i + 1]
                temp = middle.pop(-1)
                middle = [temp] + middle

                stuff = before + middle + after

            elif value > 0:
                # SUB-CASE value is moving right and wraps around
                """
                1 2 -2 4 -6 0
                move 4
                should become
                1 2 4 -2 -6 0

                i = 3
                target = (3 + 4) % 6 = 1

                [1 2] [-2 4] [-6 0]

                RANGE IS FROM TARGET+1 TO I, including I
                """

                before = stuff[: target + 1]
                after = stuff[i + 1 :]

                middle = stuff[target + 1 : i + 1]
                temp = middle.pop(-1)
                middle = [temp] + middle

                stuff = before + middle + after

        # print(f"\nSwapping the og value {value} at {og_ix=}, {i=}, {target=}")

        # print(stuff)
        # print(_decrypt_uuids(stuff, og_stuff, uuid_to_og_ix))

    return _decrypt_uuids(stuff, og_stuff, uuid_to_og_ix)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    stuff = _run_switcheroos_v2(stuff)

    i = stuff.index(0)
    size = len(stuff)

    return (
        stuff[(i + 1000) % size] + stuff[(i + 2000) % size] + stuff[(i + 3000) % size]
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):

    print()
    print(f"Initial")
    stuff = [n * 811589153 for n in stuff]
    print(stuff)

    for n in range(10):
        stuff = _run_switcheroos_v2(stuff)
        print()
        print(f"Round {n+1}")
        print(stuff)

    print()
    i = stuff.index(0)
    size = len(stuff)

    return (
        stuff[(i + 1000) % size] + stuff[(i + 2000) % size] + stuff[(i + 3000) % size]
    )


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = [int(n) for n in get_input(input_file)]
    part_one(stuff)

    # stuff = [int(n) for n in get_input(input_file)]
    # part_two(stuff)
