from util.decorators import aoc_output_formatter
from util.input import get_input

from functools import lru_cache

DAY = 11
YEAR = 2024

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = 199753

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


@lru_cache(maxsize=10000)
def _replace_stone(stone):
    if stone == 0:
        return [1]

    if len(str(stone)) % 2 == 0:
        s = str(stone)
        ls = len(s)
        a, b = int(s[:ls//2]), int(s[ls//2:])
        return [a, b]

    return [stone*2024]




@lru_cache(maxsize=None)
def _blink_stone_count(orig_stone, times):
    if times == 1:
        return len(_replace_stone(orig_stone))

    stones = _replace_stone(orig_stone)
    return sum(_blink_stone_count(ns, times-1) for ns in stones)

    # if times == 15:
    #     stones = [orig_stone]
    #     for _ in range(times):
    #         new_stones = []
    #         for stone in stones:
    #             new_stones.extend(_replace_stone(stone))
    #         stones = new_stones
    #     return len(new_stones)
    #
    # new_stones = _replace_stone(orig_stone)
    #
    # return sum(_blink_stone_count(ns, times-1) for ns in new_stones)

    # for _ in range(times):
    #     new_stones = []
    #     for stone in stones:
    #         new_stones.extend(_replace_stone(stone))
    #     stones = new_stones
    #
    # return len(stones)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stones):

    return sum(_blink_stone_count(stone, 25) for stone in stones)

    # -----------

    # for _ in range(25):
    #     new_stones = []
    #     for stone in stones:
    #         new_stones.extend(_replace_stone(stone))
    #     stones = new_stones
    #
    # return len(stones)




@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stones):

    return sum(_blink_stone_count(stone, 75) for stone in stones)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)
    stones = [int(s) for s in stuff[0].split()]
    part_one(stones)

    stuff = get_input(input_file)
    stones = [int(s) for s in stuff[0].split()]
    part_two(stones)
