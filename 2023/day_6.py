from math import ceil, sqrt
from util.decorators import aoc_output_formatter
from util.input import get_input

DAY = 6
YEAR = 2023

PART_ONE_DESCRIPTION = "product of num of ways to win smaller races"
PART_ONE_ANSWER = 500346

PART_TWO_DESCRIPTION = "how many ways you can win the longer race"
PART_TWO_ANSWER = 42515755


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(race_info):
    race_times = [int(n) for n in race_info[0].replace("Time: ", "").split()]
    race_distances = [int(n) for n in race_info[1].replace("Distance: ", "").split()]

    ways_to_win_product = 1

    for t, d in zip(race_times, race_distances):
        ways_to_win = 0
        for speed in range(t + 1):
            distance = (t - speed) * speed
            if distance > d:
                ways_to_win += 1
        ways_to_win_product *= ways_to_win

    return ways_to_win_product


@aoc_output_formatter(
    YEAR,
    DAY,
    "2 via brute force",
    PART_TWO_DESCRIPTION,
    assert_answer=PART_TWO_ANSWER,
)
def part_two(race_info):
    time = int("".join([n for n in race_info[0].replace("Time: ", "").split()]))
    target_distance = int(
        "".join([n for n in race_info[1].replace("Distance: ", "").split()])
    )

    ways_to_win = 0
    for speed in range(time + 1):
        distance = (time - speed) * speed
        if distance > target_distance:
            ways_to_win += 1

    return ways_to_win


@aoc_output_formatter(
    YEAR,
    DAY,
    "2 via quadratic formula",
    PART_TWO_DESCRIPTION,
    assert_answer=PART_TWO_ANSWER,
)
def part_two_quadratic(race_info):
    time = int("".join([n for n in race_info[0].replace("Time: ", "").split()]))
    target_distance = int(
        "".join([n for n in race_info[1].replace("Distance: ", "").split()])
    )

    # So the speed is found by the amount of time holding the button down.
    # The distance is found by the remaining amount of time * speed.
    # We are looking for the traveled distance to be greater than the target distance.
    #
    # if "D" is target distance and "B" is the amount of time we hold the button...
    #
    # traveled_distance > D
    # -->
    # (B * (time - B)) > D
    # -->
    # time*B - B^2 > D
    # -->
    # -B^2 + time*B - D > 0
    #
    # This is a quadratic equation! We can use the quadratic formula to solve. The two zeros
    # this parabola indicate the minimum and maximum values for B (the time we# hold the button
    # for) which allow us to win.
    #
    #    (-time +- sqrt( (time^2 + 4*D) )) / (-2)

    maximum_button_time = ceil(
        (-time - sqrt(((time**2) - (4 * target_distance)))) / (-2)
    )
    minimum_button_time = ceil(
        (-time + sqrt(((time**2) - (4 * target_distance)))) / (-2)
    )

    return maximum_button_time - minimum_button_time


# ----------------------------------------------------------------------------------------------


def run(input_file):
    race_info = get_input(input_file)

    part_one(race_info)
    part_two(race_info)
    part_two_quadratic(race_info)
