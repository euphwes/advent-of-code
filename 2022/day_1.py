from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 1
YEAR = 2022

PART_ONE_DESCRIPTION = "Most calories"
PART_ONE_ANSWER = 72478

PART_TWO_DESCRIPTION = "Sum of top 3 most calories"
PART_TWO_ANSWER = 210367


def _get_calories_list(snack_calories_list):
    """Parses the problem input and return a list of calorie amounts being carried by each elf.
    Each line is a snack with the specified calorie amount, and empty lines indicate the groups
    of snacks carried by different elves."""

    elf_calories = list()
    elf = 0

    for snack in snack_calories_list:
        if snack:
            elf += int(snack)
        else:
            elf_calories.append(elf)
            elf = 0

    return elf_calories


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(snacks):
    return max(_get_calories_list(snacks))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(snacks):
    sorted_calories = sorted(_get_calories_list(snacks))
    return sum(sorted_calories[-3:])


# ----------------------------------------------------------------------------------------------


def run(input_file):

    snacks = get_input(input_file)

    part_one(snacks)
    part_two(snacks)
