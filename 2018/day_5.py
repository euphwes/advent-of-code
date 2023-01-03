from copy import copy
from string import ascii_lowercase, ascii_uppercase

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 5
YEAR = 2018

PART_ONE_DESCRIPTION = "units remaining after fully reacting the polymer"
PART_ONE_ANSWER = 11636

PART_TWO_DESCRIPTION = "length of shortest polymer if all of one letter are removed"
PART_TWO_ANSWER = 5302


_PAIRS_LU = {f"{l}{u}" for l, u in zip(ascii_lowercase, ascii_uppercase)}
_PAIRS_UL = {f"{u}{l}" for l, u in zip(ascii_lowercase, ascii_uppercase)}

PAIRS = _PAIRS_LU | _PAIRS_UL


def _fully_react_polymer(polymer):
    """Fully react a given polymer by continuing to remove all adjacent upper/lowercase letter
    pairs until none remain."""

    while True:
        did_reaction = False
        for pair in PAIRS:
            if pair in polymer:
                polymer = polymer.replace(pair, "")
                did_reaction = True
        if not did_reaction:
            return polymer


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(polymer):
    return len(_fully_react_polymer(polymer))


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(original_polymer):

    polymer_reaction_results = list()

    for lower, upper in zip(ascii_lowercase, ascii_uppercase):
        polymer_copy = copy(original_polymer)
        polymer_copy = polymer_copy.replace(lower, "")
        polymer_copy = polymer_copy.replace(upper, "")

        polymer_reaction_results.append(len(_fully_react_polymer(polymer_copy)))

    return min(polymer_reaction_results)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    polymer = get_input(input_file)[0]
    part_one(polymer)

    polymer = get_input(input_file)[0]
    part_two(polymer)
