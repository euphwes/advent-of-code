from collections import defaultdict
from itertools import combinations
from typing import cast

from util.algs import angle_between, manhattan_distance
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 10
YEAR = 2019

PART_ONE_DESCRIPTION = "Number of asteroids visible from the best location"
PART_ONE_ANSWER = 267

PART_TWO_DESCRIPTION = "X*100 + Y, for (X,Y) of the 200th asteroid to be destroyed"
PART_TWO_ANSWER = 1309

Coord = tuple[int, int]
MapOfCoordToOtherCoordsByAngle = dict[Coord, dict[float, list[Coord]]]


def _build_asteroid_angle_map(
    asteroid_map,
) -> MapOfCoordToOtherCoordsByAngle:
    asteroids_locations: list[Coord] = []
    for y, line in enumerate(asteroid_map):
        for x, char in enumerate(line):
            if char == "#":
                asteroids_locations.append((x, y))

    asteroid_angles = defaultdict(lambda: defaultdict(list))

    for asteroid_1, asteroid_2 in combinations(asteroids_locations, 2):
        if asteroid_1 == asteroid_2:
            continue
        asteroid_angles[asteroid_1][angle_between(asteroid_1, asteroid_2)].append(
            asteroid_2,
        )
        asteroid_angles[asteroid_2][angle_between(asteroid_2, asteroid_1)].append(
            asteroid_1,
        )

    return cast("MapOfCoordToOtherCoordsByAngle", asteroid_angles)


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(asteroid_map):
    asteroid_angles = _build_asteroid_angle_map(asteroid_map)

    best_count = 0

    for angle_dict in asteroid_angles.values():
        curr_count = 0
        for _, other_asts in angle_dict.items():
            if other_asts:
                curr_count += 1

        best_count = max(best_count, curr_count)

    return best_count


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(asteroid_map):
    asteroid_angles = _build_asteroid_angle_map(asteroid_map)

    best_count = 0
    best_asteroid: Coord | None = None

    for asteroid, angle_dict in asteroid_angles.items():
        curr_count = 0
        for _, other_asts in angle_dict.items():
            if other_asts:
                curr_count += 1

        if curr_count > best_count:
            best_count = curr_count
            best_asteroid = asteroid

    assert best_asteroid is not None

    visible_asteroids_by_angle = asteroid_angles[best_asteroid]
    angles_visible_from_asteroid = sorted(list(asteroid_angles[best_asteroid].keys()))

    # start at 270 degrees which is UP
    angle_ix = angles_visible_from_asteroid.index(270)

    exploded_count = 0
    while exploded_count < 200:
        # get visible asteroids at this angle
        angle = angles_visible_from_asteroid[angle_ix]
        asts = visible_asteroids_by_angle[angle]

        asts = sorted(asts, key=lambda x: manhattan_distance(x, best_asteroid))

        exploded = asts.pop(0)
        visible_asteroids_by_angle[angle] = asts

        exploded_count += 1
        if exploded_count == 200:
            return 100 * exploded[0] + exploded[1]

        angle_ix = (angle_ix + 1) % len(angles_visible_from_asteroid)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    asteroid_map = get_input(input_file)
    part_one(asteroid_map)

    asteroid_map = get_input(input_file)
    part_two(asteroid_map)
