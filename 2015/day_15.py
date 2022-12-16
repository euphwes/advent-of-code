from itertools import product

from util.decorators import aoc_output_formatter
from util.input import get_tokenized_input

DAY = 15
YEAR = 2015

PART_ONE_DESCRIPTION = "Best cookie score"
PART_ONE_ANSWER = 21367368

PART_TWO_DESCRIPTION = "Best 500 calorie cookie score"
PART_TWO_ANSWER = 1766400


class Ingredient:
    """Represents an ingredient for a cookie, with a variety of properties."""

    def __init__(self, input_tokens):
        # Tokens ex: `Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8`
        self.name = input_tokens[0][0:-1]
        self.capacity = int(input_tokens[2][0:-1])
        self.durability = int(input_tokens[4][0:-1])
        self.flavor = int(input_tokens[6][0:-1])
        self.texture = int(input_tokens[8][0:-1])
        self.calories = int(input_tokens[10])


class Cookie:
    """A cookie baked from a set of Ingredients (num of tbps of each Ingredient)."""

    def __init__(self, recipe, ingredients):
        flavor = 0
        texture = 0
        capacity = 0
        durability = 0
        self.calories = 0

        for amount, ingredient in zip(recipe, ingredients):
            flavor += amount * ingredient.flavor
            texture += amount * ingredient.texture
            capacity += amount * ingredient.capacity
            durability += amount * ingredient.durability
            self.calories += amount * ingredient.calories

        flavor = 0 if flavor < 0 else flavor
        texture = 0 if texture < 0 else texture
        capacity = 0 if capacity < 0 else capacity
        durability = 0 if durability < 0 else durability

        self.score = flavor * texture * capacity * durability


def _ingredient_breakdown_options(target_tbps, num_ingredients):
    """A generator which yields tuples of the number of tbsps of each ingredient, for a target
    number of ingredients.

    Ex: 100 tbsps of 4 ingredients: (25, 25, 25, 25), (10, 10, 10, 70), (0, 100, 0, 0), etc."""

    for p in product(range(target_tbps + 1), repeat=num_ingredients):
        if sum(p) == target_tbps:
            yield p


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(ingredients):
    cookies_score = list()
    for recipe in _ingredient_breakdown_options(100, len(ingredients)):
        cookies_score.append(Cookie(recipe, ingredients).score)
    return max(cookies_score)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(ingredients):
    cookies_score = list()
    for recipe in _ingredient_breakdown_options(100, len(ingredients)):
        cookie = Cookie(recipe, ingredients)
        if cookie.calories == 500:
            cookies_score.append(cookie.score)
    return max(cookies_score)


# ----------------------------------------------------------------------------------------------


def run(input_file):

    ingredients = [
        Ingredient(tokens) for tokens in get_tokenized_input(input_file, " ")
    ]

    part_one(ingredients)
    part_two(ingredients)
