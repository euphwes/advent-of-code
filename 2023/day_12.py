from functools import lru_cache
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 12
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of possible arrangements of springs"
PART_ONE_ANSWER = 7236

PART_TWO_DESCRIPTION = "sum of possible arrangements of springs from unfolded input"
PART_TWO_ANSWER = 11607695322318


@lru_cache(maxsize=None)
def _count_solutions(config, nums):
    # Base case, an empty config is valid only if we're not expecting any more blocks of springs
    if config == "":
        return 1 if not nums else 0

    # Other base case, no more blocks of springs is only valid if no more springs left
    if nums == ():
        return 0 if "#" in config else 1

    result = 0
    curr_block_size = nums[0]

    # Case 1, consider the first character of the string we're looking at to be a dot, which
    # doesn't contribute towards a block of springs. Count the solutions to the remainder of
    # the string with the same block numbers.
    if config[0] in ".?":
        result += _count_solutions(config[1:], nums)

    # Case 2, try to consider the first character of the string we're looking at to be the
    # start of a block of springs.
    if config[0] in "#?":
        # Are there enough remaining characters to finish the block size we're looking at?
        enough_remaining = curr_block_size <= len(config)
        # Do the next N characters (for the block size we're looking at) not contain any dots?
        # If they do, we're actually looking at 2+ blocks, not just 1.
        no_dots_in_block = "." not in config[:curr_block_size]
        # The tentative block that we're looking at can't end with a spring, because then it's
        # actually just a longer block. We need to go up to the end of the whole config, or at
        # least not end with a spring.
        terminates_correctly = enough_remaining and (
            curr_block_size == len(config) or config[curr_block_size] != "#"
        )

        # If the current character can be the start of a block of the appropriate size,
        # add how many solutions the remainder has -- the config string starting after the
        # current block, with the remaining numbers of blocks
        if enough_remaining and no_dots_in_block and terminates_correctly:
            result += _count_solutions(config[curr_block_size + 1 :], nums[1:])

    return result


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(spring_info):
    total_ways_to_solve = 0

    for line in spring_info:
        config, raw_nums = line.split(" ")
        nums = tuple(int(n) for n in raw_nums.split(","))

        total_ways_to_solve += _count_solutions(config, nums)

    return total_ways_to_solve


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(spring_info):
    total_ways_to_solve = 0

    for line in spring_info:
        config, raw_nums = line.split(" ")
        nums = tuple(int(n) for n in raw_nums.split(","))

        # "Unfold" the config by expand it by 5x. For the config line itself, join each of the
        # 5 instances of the config with a "?"
        config = "?".join([config] * 5)
        nums = nums * 5

        total_ways_to_solve += _count_solutions(config, nums)

    return total_ways_to_solve


# ----------------------------------------------------------------------------------------------


def run(input_file):
    spring_info = get_input(input_file)
    part_one(spring_info)
    part_two(spring_info)
