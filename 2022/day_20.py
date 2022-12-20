from copy import copy
from os import remove

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 20
YEAR = 2022

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one_archive(stuff):
    original_order = copy(stuff)
    size = len(stuff)

    print(stuff)
    for og_value in original_order:
        if og_value == 0:
            print("\nnot moving 0")
            print(stuff)
            continue

        i = stuff.index(og_value)
        target = (i + og_value) % size
        value_at_target = stuff[target % size]
        print()
        print(f"moving {og_value} to target ix {target} where {value_at_target} is")

        stuff.pop(i)
        new_target = stuff.index(value_at_target)
        # print(f"new target is {new_target}")

        if new_target == 0:
            stuff = [og_value] + stuff
        elif new_target == size - 2:
            stuff = stuff + [og_value]
        else:
            before, after = stuff[:new_target], stuff[new_target:]
            # print(f"before piece: {before}")
            # print(f"after piece: {after}")
            stuff = before + [og_value] + after

        """
        1, -3, 2, 3, -2, 0, 4

        -3 moves between -2 and 0:
        
        1, 2, 3, -2, -3, 0, 4


        i = 1
        target = 1 - 3 = -2   (which is value 0, should go there)
        -2 + 7 = 5

        pop i = 1 (removing -3)
        1, 2, 3, -2, 0, 4

        new_target = 4
        [1, 2, 3, -2] + [-3] + [0, 4]
        """

        # if og_value > 0:
        #     for _ in range(og_value):
        #         stuff[i % size], stuff[(i + 1) % size] = (
        #             stuff[(i + 1) % size],
        #             stuff[i % size],
        #         )
        #         i += 1
        # else:
        #     for _ in range(abs(og_value)):
        #         stuff[i % size], stuff[(i - 1) % size] = (
        #             stuff[(i - 1) % size],
        #             stuff[i % size],
        #         )
        #         i -= 1

        print()
        print(stuff)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):

    # print()
    # print(stuff)

    size = len(stuff)

    for og_value in list(copy(stuff)):

        if og_value == 0:
            # print("\nnot moving 0\n")
            # print(stuff)
            continue

        i = stuff.index(og_value)
        target = (i + og_value + size) % size
        value_at_target = stuff[target]
        # print()
        # print(f"found {og_value} at {i=}, moving to {target=} where {value_at_target=}")

        if target > i:
            # swap to the right
            num_swaps = abs(i - target)
            if og_value < 0:
                num_swaps -= 1
            for _ in range(num_swaps):
                a, b = stuff[i % size], stuff[(i + 1) % size]
                stuff[i % size], stuff[(i + 1) % size] = b, a

                i += 1
                i = i % size

            test = stuff.index(og_value)
            if test == size - 1:
                stuff.pop(-1)
                stuff = [og_value] + stuff

        else:
            # swap to the left
            num_swaps = abs(i - target)
            if og_value > 0:
                num_swaps -= 1
            for _ in range(num_swaps):
                a, b = stuff[i % size], stuff[(i - 1) % size]
                stuff[i % size], stuff[(i - 1) % size] = b, a

                i -= 1
                i = i % size

            test = stuff.index(og_value)
            if test == 0:
                stuff.pop(0)
                stuff.append(og_value)

        # print()
        # print(stuff)

    i = stuff.index(0)

    # not 13972, 15077
    # print(stuff)
    return (
        stuff[(i + 1000) % size] + stuff[(i + 2000) % size] + stuff[(i + 3000) % size]
    )


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    pass


# ----------------------------------------------------------------------------------------------


def run(input_file):

    stuff = [int(n) for n in get_input(input_file)]
    part_one(stuff)

    stuff = [int(n) for n in get_input(input_file)]
    part_two(stuff)
