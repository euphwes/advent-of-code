from collections import defaultdict
from itertools import combinations
from math import atan2, pi

from util.decorators import aoc_output_formatter
from util.input import get_input
from util.algs import manhattan_distance

DAY = 10
YEAR = 2019

PART_ONE_DESCRIPTION = "number of asteroids visible from the best location"
PART_ONE_ANSWER = 267

PART_TWO_DESCRIPTION = "(100x + y) of the 200th asteroid to be vaporized"
PART_TWO_ANSWER = 1309


def _angle_between(asteroid1: tuple[int, int], asteroid2: tuple[int, int]) -> float:
    x1, y1 = asteroid1
    x2, y2 = asteroid2
    theta = atan2((y2 - y1), (x2 - x1))
    return ((theta) * (180 / pi) + 360) % 360


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(asteroid_map):
    asteroids_locations = []
    for y, line in enumerate(asteroid_map):
        for x, char in enumerate(line):
            if char == "#":
                asteroids_locations.append((x, y))

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


    ordered_angles = sorted(asteroid_angles[best_asteroid].keys())
    num_angles = len(ordered_angles)
    i = ordered_angles.index(270)

    num_asteroids_vaporized = 0
    while True:
        asteroids_at_angle = asteroid_angles[best_asteroid][ordered_angles[i]]
        if asteroids_at_angle:
            closest_asteroids = sorted(asteroids_at_angle, key=lambda other: manhattan_distance(best_asteroid, other))
            to_vaporize = closest_asteroids.pop(0)
            num_asteroids_vaporized += 1
            if num_asteroids_vaporized == 200:
                x, y = to_vaporize
                return x*100 + y

        i = (i + 1) % num_angles

    return best_asteroid

# ----------------------------------------------------------------------------------------------


def run(input_file):
    asteroid_map = get_input(input_file)
    part_one(asteroid_map)

    asteroid_map = get_input(input_file)
    part_two(asteroid_map)
