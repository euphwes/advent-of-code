from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 14
YEAR = 2018

PART_ONE_DESCRIPTION = "next 10 recipes after target number of recipes found"
PART_ONE_ANSWER = "5115114101"

PART_TWO_DESCRIPTION = "how many recipes until the target value appears in the recipes"
PART_TWO_ANSWER = 20310465


def _stringify(values):
    """Turn a list of integers into a string containing those digits."""

    return "".join(str(digit) for digit in values)


def _extend_recipes(recipes, elf1_ix, elf2_ix):
    """Given a current recipe set and indices where elf #1 and #2 are, extend the recipes by
    finding the sum of the current elves' recipes, adding those digits to the end of the
    recipes, and then moving the elves to their next indices."""

    recipe_sum = recipes[elf1_ix] + recipes[elf2_ix]

    new_recipe_digits = [int(digit) for digit in str(recipe_sum)]
    recipes.extend(new_recipe_digits)

    elf1_ix = (elf1_ix + recipes[elf1_ix] + 1) % len(recipes)
    elf2_ix = (elf2_ix + recipes[elf2_ix] + 1) % len(recipes)

    return recipes, elf1_ix, elf2_ix


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(num_recipes):

    recipes = [3, 7]

    elf1_ix = 0
    elf2_ix = 1

    while len(recipes) < (num_recipes + 10):
        recipes, elf1_ix, elf2_ix = _extend_recipes(recipes, elf1_ix, elf2_ix)

    # Remove `num_recipes` from the front and then return the stringified next 10 recipes.
    trimmed_recipes = recipes[num_recipes:]

    return _stringify(trimmed_recipes[:10])


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(search_value):

    recipes = [3, 7]

    elf1_ix = 0
    elf2_ix = 1

    # However long the search value is, we only need to search that many digits at the end of
    # the recipes list, plus one. Plus one because we could be adding 2 more digits each time we
    # extend the recipes, but the first of those digits is the one that completes the search
    # value we're looking for.
    search_len = len(search_value) + 1

    while True:
        recipes, elf1_ix, elf2_ix = _extend_recipes(recipes, elf1_ix, elf2_ix)

        try:
            # Check to see if the search value is in the last N+1 digits of the recipes.
            recipe_str = _stringify(recipes[-1 * search_len :])

            # If it is, extract the index of that search string in the full thing. The index is
            # also how many elements precede it in the string (aka the number of recipes before)
            if search_value in recipe_str:
                full_recipe_str = _stringify(recipes)
                return full_recipe_str.index(search_value)
        except ValueError:
            pass


# ----------------------------------------------------------------------------------------------


def run(input_file):

    num_recipes = get_input(input_file)[0]

    part_one(int(num_recipes))
    part_two(str(num_recipes))
