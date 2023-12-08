from util.decorators import aoc_output_formatter
from util.input import get_input
from util.iter import repeat_forever

from collections import defaultdict
from math import lcm

DAY = 8
YEAR = 2023

PART_ONE_DESCRIPTION = "steps between AAA and ZZZ"
PART_ONE_ANSWER = 16409

PART_TWO_DESCRIPTION = "steps when all -A starts land on -Z at the same time"
PART_TWO_ANSWER = 11795205644011


def _get_directions(puzzle_input):
    return puzzle_input[0]


def _get_network_map(puzzle_input):
    # The first 2 lines are the directions and an empty spacer line. We can ignore.
    only_map_info = puzzle_input[2:]

    network_map = defaultdict(dict)

    for line in only_map_info:
        line = line.replace("(", "").replace(")", "")

        start, destination = line.split(" = ")
        destination_left, destination_right = destination.split(", ")
        network_map[start] = {"L": destination_left, "R": destination_right}

    return network_map


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(puzzle_input):
    directions = _get_directions(puzzle_input)
    network_map = _get_network_map(puzzle_input)

    steps = 0
    curr_loc = "AAA"

    for direction in repeat_forever(directions):
        steps += 1
        curr_loc = network_map[curr_loc][direction]

        if curr_loc == "ZZZ":
            return steps


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(puzzle_input):
    directions = _get_directions(puzzle_input)
    network_map = _get_network_map(puzzle_input)

    start_locations = list(start for start in network_map.keys() if start.endswith("A"))

    all_steps = list()

    # For each starting location (a location that ends with "A"), count the steps until we
    # arrive at an ending location (a location that ends with "Z"). Add the step count required
    # to reach that to the list.
    for curr_loc in start_locations:
        steps = 0

        for direction in repeat_forever(directions):
            steps += 1
            curr_loc = network_map[curr_loc][direction]

            if curr_loc.endswith("Z"):
                all_steps.append(steps)
                break

    # If everybody starts on an A-location at the same time, the first time they'll all arrive
    # on their ending location at the same is at a time which is the lowest common multiple of
    # all the steps required for each individual starting location to reach their destination.
    #
    # Eg: A takes 7 steps to reach Z
    #     AA takes 3 steps to reach ZZ.
    #
    # 2 separate people starting on A and AA will reach Z and ZZ at the same time after
    # 3 * 7 = 21 steps.
    #
    # This isn't guaranteed in the general case, but the problem input here guarantees it
    # because the following conditions hold true:
    #
    # 1. Each starting position only has *one* ending position (-Z) it can reach.
    # 2. Each starting position takes the same amount of time to reach the end from the start,
    #    as it does to cycle back to the end from the end again.
    return lcm(*all_steps)


# ----------------------------------------------------------------------------------------------


def run(input_file):
    puzzle_input = get_input(input_file)
    part_one(puzzle_input)
    part_two(puzzle_input)
