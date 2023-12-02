from util.decorators import aoc_output_formatter
from util.input import get_input

from math import prod

DAY = 2
YEAR = 2023

PART_ONE_DESCRIPTION = "sum of possible game IDs"
PART_ONE_ANSWER = 2810

PART_TWO_DESCRIPTION = "sum of powers of min cubes needed to make each game possible"
PART_TWO_ANSWER = 69110


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(cube_game_info):
    # A map that specifies how many of each color block we have available to us.
    counts_by_block_color = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    possible_game_ids = list()

    # Assume each game is possible until we prove otherwise.
    for game_line in cube_game_info:
        is_possible = True

        # Split the line into halves; the first contains the game ID, the second contains
        # the info about the number of colored blocks pulled during each round.
        game_id, block_pulls = game_line.split(": ")
        id = int(game_id.replace("Game ", ""))

        for pull in block_pulls.split("; "):
            block_counts = pull.split(", ")
            for d in block_counts:
                num, color = d.split(" ")
                num = int(num)
                if num > counts_by_block_color[color]:
                    is_possible = False
                    break
            if not is_possible:
                break

        if is_possible:
            possible_game_ids.append(id)

    return sum(possible_game_ids)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(cube_game_info):
    powers = list()

    # For each game, start by assuming 0 blocks of each color is sufficient
    for line in cube_game_info:
        lower_limits = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }

        _, block_pulls = line.split(": ")

        for pull in block_pulls.split("; "):
            block_counts = pull.split(", ")
            for d in block_counts:
                num, color = d.split(" ")
                num = int(num)
                if num > lower_limits[color]:
                    lower_limits[color] = num

        powers.append(prod(lower_limits.values()))

    return sum(powers)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    cube_game_info = get_input(input_file)

    part_one(cube_game_info)
    part_two(cube_game_info)
