from collections import defaultdict
from itertools import combinations
from math import inf, atan

from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 10
YEAR = 2019

PART_ONE_DESCRIPTION = ""
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = ""
PART_TWO_ANSWER = None


def _slope_between(ast1, ast2):
    x1, y1 = ast1
    x2, y2 = ast2

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        return inf
    else:
        return dy / dx


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
        slope = _slope_between(ast1, ast2)
        asteroid_angles[ast1][slope].append(ast2)
        asteroid_angles[ast2][slope].append(ast1)

    best_count = 0
    for asteroid, angle_dict in asteroid_angles.items():

        ax, ay = asteroid

        curr_count = 0

        for angle, other_asts in angle_dict.items():
            if angle == 0:
                if any(bx > ax for bx, _ in other_asts):
                    curr_count += 1
                if any(bx < ax for bx, _ in other_asts):
                    curr_count += 1
            elif angle == inf:
                if any(by > ay for _, by in other_asts):
                    curr_count += 1
                if any(by < ay for _, by in other_asts):
                    curr_count += 1
            else:
                if any(bx > ax for bx, _ in other_asts):
                    curr_count += 1
                if any(bx < ax for bx, _ in other_asts):
                    curr_count += 1

        print(curr_count)
        if curr_count > best_count:
            best_count = curr_count

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
