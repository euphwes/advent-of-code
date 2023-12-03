from util.decorators import aoc_output_formatter
from util.input import get_input
from math import prod

DAY = 6
YEAR = 2023

PART_ONE_DESCRIPTION = "product of num of ways to win smaller races"
PART_ONE_ANSWER = None

PART_TWO_DESCRIPTION = "how many ways you can win the longer race"
PART_TWO_ANSWER = 42515755


@aoc_output_formatter(YEAR, DAY, 1, PART_ONE_DESCRIPTION, assert_answer=PART_ONE_ANSWER)
def part_one(stuff):
    raw_t = [int(n) for n in stuff[0].replace("Time: ", "").split()]
    raw_s = [int(n) for n in stuff[1].replace("Distance: ", "").split()]
    tds = list(zip(raw_t, raw_s))

    ways_to_win = list()

    for t, d in tds:
        w = 0
        for speed in range(t + 1):
            distance = (t - speed) * speed
            if distance > d:
                w += 1
        ways_to_win.append(w)

    return prod(ways_to_win)


@aoc_output_formatter(YEAR, DAY, 2, PART_TWO_DESCRIPTION, assert_answer=PART_TWO_ANSWER)
def part_two(stuff):
    raw_t = int("".join([n for n in stuff[0].replace("Time: ", "").split()]))
    raw_d = int("".join([n for n in stuff[1].replace("Distance: ", "").split()]))

    w = 0
    for speed in range(raw_t + 1):
        distance = (raw_t - speed) * speed
        if distance > raw_d:
            w += 1
        else:
            if w > 1:
                break

    return w


# ----------------------------------------------------------------------------------------------


def run(input_file):
    stuff = get_input(input_file)

    # not 27131650
    part_one(stuff)
    part_two(stuff)
