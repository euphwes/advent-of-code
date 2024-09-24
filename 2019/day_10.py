from collections import defaultdict
from itertools import combinations
from math import atan2, pi

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 10
YEAR = 2019

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _angle_between(ast1, ast2):
    x1, y1 = ast1
    x2, y2 = ast2

    dx = x2 - x1
    dy = y2 - y1

    theta = atan2(dy, dx)
    angle = ((theta) * (180 / pi) + 360) % 360

    return angle


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(asteroid_map):
    asteroids_locations = []
    for y, line in enumerate(asteroid_map):
        for x, char in enumerate(line):
            if char == "#":
                asteroids_locations.append((x, y))
    # print(asteroids_locations)

    get_angles_to_asts_dict = lambda: defaultdict(list)
    asteroid_angles = defaultdict(get_angles_to_asts_dict)

    for ast1, ast2 in combinations(asteroids_locations, 2):
        if ast1 == ast2:
            continue
        asteroid_angles[ast1][_angle_between(ast1, ast2)].append(ast2)
        asteroid_angles[ast2][_angle_between(ast2, ast1)].append(ast1)

    from pprint import pprint

    best_count = 0
    best_asteroid = None

    for asteroid, angle_dict in asteroid_angles.items():
        if asteroid == (2, 2):
            print(f"\nlooking at {asteroid}\n")
            pprint(dict(angle_dict))

        ax, ay = asteroid

        curr_count = 0

        for _, other_asts in angle_dict.items():
            if other_asts:
                curr_count += 1

        if curr_count > best_count:
            best_asteroid = asteroid
            best_count = curr_count

        if asteroid == (2, 2):
            print(f"found {curr_count}")

    return best_count


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(asteroid_map):
    pass


# ----------------------------------------------------------------------------------------------


def run(input_file):
    asteroid_map = get_input(input_file)
    part_one(asteroid_map)

    asteroid_map = get_input(input_file)
    part_two(asteroid_map)
